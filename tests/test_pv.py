import pandas as pd
import pytest

from flexlab.models.pv import PVSystem, RoofSurface, simulate_pv

LAT, LON = 49.55, 8.24


def _weather() -> pd.DataFrame:
    """One summer day, constant synthetic irradiance between 6 and 16 UTC."""
    index = pd.date_range("2001-06-21", periods=24, freq="h", tz="UTC")
    day = (index.hour >= 6) & (index.hour <= 16)
    return pd.DataFrame(
        {
            "ghi": [600.0 if d else 0.0 for d in day],
            "dni": [800.0 if d else 0.0 for d in day],
            "dhi": [100.0 if d else 0.0 for d in day],
            "temp_air": 20.0,
            "wind_speed": 2.0,
        },
        index=index,
    )


def _yield(system: PVSystem, weather=None) -> float:
    weather = _weather() if weather is None else weather
    return float(simulate_pv(weather, LAT, LON, system).sum())


def test_no_irradiance_gives_zero():
    weather = _weather()
    weather[["ghi", "dni", "dhi"]] = 0.0
    ac = simulate_pv(weather, LAT, LON, PVSystem([RoofSurface(4, 30)]))
    assert ac.isna().sum() == 0
    assert ac.sum() == 0


def test_south_beats_north():
    south = _yield(PVSystem([RoofSurface(4, 30, 180)]))
    north = _yield(PVSystem([RoofSurface(4, 30, 0)]))
    assert south > north


def test_yield_scales_with_kwp():
    four = _yield(PVSystem([RoofSurface(4, 30)]))
    eight = _yield(PVSystem([RoofSurface(8, 30)]))
    assert eight / four == pytest.approx(2.0, rel=1e-6)


def test_two_surfaces_equal_one_combined():
    one = _yield(PVSystem([RoofSurface(4, 30, 180)]))
    two = _yield(PVSystem([RoofSurface(2, 30, 180), RoofSurface(2, 30, 180)]))
    assert two == pytest.approx(one, rel=1e-6)


def test_inverter_clips_output():
    system = PVSystem([RoofSurface(4, 30)], inverter_dc_kw=1.0)
    ac = simulate_pv(_weather(), LAT, LON, system)
    assert ac.max() <= 1.0 * system.inverter_efficiency + 1e-9


def test_invalid_input_rejected():
    with pytest.raises(ValueError):
        RoofSurface(kwp=-1, tilt=30)
    with pytest.raises(ValueError):
        RoofSurface(kwp=4, tilt=120)