"""Test for the GeoNet NZ Volcanic Alert Level GeoJSON feed."""
import asyncio
from http import HTTPStatus

import aiohttp
import pytest
from aio_geojson_client.consts import UPDATE_OK

from aio_geojson_geonetnz_volcano.consts import ATTRIBUTION
from aio_geojson_geonetnz_volcano.feed import GeonetnzVolcanoFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_update_ok(mock_aioresponse):
    """Test updating feed is ok."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://api.geonet.org.nz/volcano/val",
        status=HTTPStatus.OK,
        body=load_fixture("val-1.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = GeonetnzVolcanoFeed(websession, home_coordinates)
        assert (
            repr(feed) == "<GeonetnzVolcanoFeed(home=(-41.2, 174.7), "
            "url=https://api.geonet.org.nz/volcano/val, "
            "radius=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 3

        feed_entry = entries[0]
        assert feed_entry is not None
        assert feed_entry.title == "Volcano 1"
        assert feed_entry.external_id == "volcano1"
        assert feed_entry.coordinates[0] == pytest.approx(-38.784)
        assert feed_entry.coordinates[1] == pytest.approx(175.896)
        assert round(abs(feed_entry.distance_to_home - 287.3), 1) == 0
        assert repr(feed_entry) == "<GeonetnzVolcanoFeedEntry(id=volcano1)>"
        assert feed_entry.attribution == ATTRIBUTION
        assert feed_entry.alert_level == 0
        assert feed_entry.activity == "No volcanic unrest."
        assert feed_entry.hazards == "Volcanic environment hazards."

        feed_entry = entries[1]
        assert feed_entry is not None
        assert feed_entry.title == "Volcano 2"
        assert feed_entry.external_id == "volcano2"

        feed_entry = entries[2]
        assert feed_entry is not None


@pytest.mark.asyncio
async def test_empty_feed(mock_aioresponse):
    """Test updating feed is ok when feed does not contain any entries."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://api.geonet.org.nz/volcano/val",
        status=HTTPStatus.OK,
        body=load_fixture("val-2.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = GeonetnzVolcanoFeed(websession, home_coordinates)
        assert (
            repr(feed) == "<GeonetnzVolcanoFeed(home=(-41.2, 174.7), "
            "url=https://api.geonet.org.nz/volcano/val, "
            "radius=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 0
        assert feed.last_timestamp is None
