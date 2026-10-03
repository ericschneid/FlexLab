"""PVGIS weather data: typical meteorological year (TMY) for a location."""

from pathlib import Path

import pandas as pd
from pvlib.iotools import get_pvgis_tmy

# Cache folder in the project root (src/flexlab/data/pvgis.py -> parents[3])
DEFAULT_CACHE_DIR = Path(__file__).resolve().parents[3] / "data_cache"
# PVGIS builds the TMY from months of different years.
# All timestamps are moved into one non-leap reference year.
REFERENCE_YEAR = 2001


def _normalize_index(data: pd.DataFrame) -> pd.DataFrame:
    """Put all rows into the reference year, drop Feb 29, sort by time."""
    data = data[~((data.index.month == 2) & (data.index.day == 29))].copy()
    data.index = pd.DatetimeIndex(
        [ts.replace(year=REFERENCE_YEAR) for ts in data.index]
    )
    return data.sort_index()


def get_tmy(latitude: float, longitude: float, cache_dir=DEFAULT_CACHE_DIR) -> pd.DataFrame:
    """Return hourly typical-year weather data for a location.

    Index: hourly timestamps (UTC) in the reference year.
    Columns: as delivered by PVGIS via pvlib (e.g. ghi, dni, dhi, temp_air, wind_speed).
    The result is cached locally, so PVGIS is queried only once per location.
    """
    cache_dir = Path(cache_dir)
    cache_file = cache_dir / f"tmy_{latitude:.3f}_{longitude:.3f}.csv"

    if cache_file.exists():
        data = pd.read_csv(cache_file, index_col=0)
        data.index = pd.to_datetime(data.index, utc=True)
        return data

    result = get_pvgis_tmy(latitude, longitude, map_variables=True)
    data = _normalize_index(result[0])  # first element is the hourly data
    cache_dir.mkdir(parents=True, exist_ok=True)
    data.to_csv(cache_file)
    return data