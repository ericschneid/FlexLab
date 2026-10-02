from unittest.mock import MagicMock, patch

import pytest

from flexlab.data.geocoding import geocode


def _fake_response(payload):
    response = MagicMock()
    response.json.return_value = payload
    response.raise_for_status.return_value = None
    return response


def test_geocode_returns_coordinates():
    payload = [{"lat": "50.0", "lon": "8.0", "display_name": "Testort"}]
    with patch("flexlab.data.geocoding.requests.get", return_value=_fake_response(payload)):
        result = geocode("Testort")
    assert result["latitude"] == 50.0
    assert result["longitude"] == 8.0


def test_geocode_unknown_place_raises():
    with patch("flexlab.data.geocoding.requests.get", return_value=_fake_response([])):
        with pytest.raises(ValueError):
            geocode("Nirgendwo")