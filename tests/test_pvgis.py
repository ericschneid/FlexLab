from unittest.mock import MagicMock, patch

import pandas as pd

from flexlab.data.pvgis import REFERENCE_YEAR, get_tmy


def _fake_tmy() -> pd.DataFrame:
    """8760 hourly rows: January from 2012, the rest from 2005 (mixed years like PVGIS)."""
    january = pd.date_range("2012-01-01", periods=31 * 24, freq="h", tz="UTC")
    rest = pd.date_range("2005-02-01", "2005-12-31 23:00", freq="h", tz="UTC")
    return pd.DataFrame(
        0.0,
        index=january.append(rest),
        columns=["ghi", "dni", "dhi", "temp_air", "wind_speed"],
    )


def test_tmy_uses_one_reference_year(tmp_path):
    fake = (_fake_tmy(), None, None, None)
    with patch("flexlab.data.pvgis.get_pvgis_tmy", return_value=fake):
        data = get_tmy(49.55, 8.24, cache_dir=tmp_path)
    assert len(data) == 8760
    assert set(data.index.year) == {REFERENCE_YEAR}
    assert data.index.is_unique
    assert data.index.is_monotonic_increasing


def test_second_call_uses_cache(tmp_path):
    mock = MagicMock(return_value=(_fake_tmy(), None, None, None))
    with patch("flexlab.data.pvgis.get_pvgis_tmy", mock):
        get_tmy(49.55, 8.24, cache_dir=tmp_path)
        second = get_tmy(49.55, 8.24, cache_dir=tmp_path)
    assert mock.call_count == 1
    assert len(second) == 8760