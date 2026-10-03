"""PV yield model: hourly AC power of a PV system from weather data (pvlib, PVWatts approach)."""

from dataclasses import dataclass

import pandas as pd
from pvlib import inverter, irradiance, pvsystem, temperature
from pvlib.location import Location

# Compass direction -> azimuth in degrees (pvlib: 0 = north, 90 = east, 180 = south, 270 = west)
DIRECTIONS = {
    "N": 0.0, "NO": 45.0, "O": 90.0, "SO": 135.0,
    "S": 180.0, "SW": 225.0, "W": 270.0, "NW": 315.0,
}

# Placeholder assumptions, to be documented in ASSUMPTIONS.md:
# - power temperature coefficient (crystalline silicon, typical value)
# - roof-mounted module temperature model (sapm, close_mount_glass_glass)
# - isotropic sky model, no reflection losses, no shading, altitude 0
# - solar position computed at the full hour of each timestamp
GAMMA_PDC = -0.004  # relative power change per Kelvin
CELL_TEMP_PARAMS = temperature.TEMPERATURE_MODEL_PARAMETERS["sapm"]["close_mount_glass_glass"]


@dataclass
class RoofSurface:
    """One roof surface: size in kWp, tilt and azimuth in degrees (180 = south)."""

    kwp: float
    tilt: float
    azimuth: float = 180.0

    def __post_init__(self):
        if self.kwp <= 0:
            raise ValueError("kwp must be positive")
        if not 0 <= self.tilt <= 90:
            raise ValueError("tilt must be between 0 and 90 degrees")
        if not 0 <= self.azimuth <= 360:
            raise ValueError("azimuth must be between 0 and 360 degrees")


@dataclass
class PVSystem:
    """PV system with one or more roof surfaces and one shared inverter."""

    surfaces: list[RoofSurface]
    system_loss_pct: float = 10.0          # placeholder, see ASSUMPTIONS.md
    inverter_efficiency: float = 0.96      # placeholder, see ASSUMPTIONS.md
    inverter_dc_kw: float | None = None    # None -> inverter sized to total kWp

    def __post_init__(self):
        if not self.surfaces:
            raise ValueError("at least one roof surface is required")
        if not 0 <= self.system_loss_pct < 100:
            raise ValueError("system_loss_pct must be between 0 and 100")
        if not 0 < self.inverter_efficiency <= 1:
            raise ValueError("inverter_efficiency must be between 0 and 1")

    @property
    def total_kwp(self) -> float:
        return sum(s.kwp for s in self.surfaces)


def simulate_pv(weather: pd.DataFrame, latitude: float, longitude: float,
                system: PVSystem, sky_model: str = "isotropic") -> pd.Series:
    """Return hourly AC power in kW (equals kWh per hour) for the given weather data.

    weather needs the columns ghi, dni, dhi, temp_air, wind_speed and a
    timezone-aware hourly index.
    sky_model: diffuse sky model, 'isotropic', 'haydavies' or 'perez'.
    """
    location = Location(latitude, longitude)
    solar = location.get_solarposition(weather.index)

    extra = {}
    if sky_model in ("haydavies", "perez"):
        extra["dni_extra"] = irradiance.get_extra_radiation(weather.index)
    if sky_model == "perez":
        extra["airmass"] = location.get_airmass(solar_position=solar)["airmass_relative"]

    dc_total = pd.Series(0.0, index=weather.index)
    for surface in system.surfaces:
        poa = irradiance.get_total_irradiance(
            surface_tilt=surface.tilt,
            surface_azimuth=surface.azimuth,
            solar_zenith=solar["apparent_zenith"],
            solar_azimuth=solar["azimuth"],
            dni=weather["dni"],
            ghi=weather["ghi"],
            dhi=weather["dhi"],
            model=sky_model,
            **extra,
        )
        cell_temp = temperature.sapm_cell(
            poa["poa_global"], weather["temp_air"], weather["wind_speed"], **CELL_TEMP_PARAMS
        )
        dc_total = dc_total + pvsystem.pvwatts_dc(
            poa["poa_global"], cell_temp, surface.kwp, GAMMA_PDC
        )

    dc_total = dc_total * (1 - system.system_loss_pct / 100)
    inverter_dc_kw = system.inverter_dc_kw or system.total_kwp
    ac = inverter.pvwatts(dc_total, inverter_dc_kw, eta_inv_nom=system.inverter_efficiency)
    ac = ac.fillna(0.0).clip(lower=0.0)
    ac.name = "ac_kw"
    return ac