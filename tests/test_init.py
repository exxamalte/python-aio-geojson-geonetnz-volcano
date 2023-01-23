"""Test for the GeoNet NZ Volcano GeoJSON general setup."""
from aio_geojson_geonetnz_volcano import __version__


def test_version():
    """Test for version tag."""
    assert __version__ is not None
