"""Test for the GeoNet NZ Volcanic Alert Level GeoJSON feed manager."""

import asyncio
from http import HTTPStatus
from unittest import mock as async_mock

from aio_geojson_client.consts import UPDATE_ERROR, UPDATE_OK_NO_DATA
import aiohttp
import pytest

from aio_geojson_geonetnz_volcano.feed_manager import GeonetnzVolcanoFeedManager
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_feed_manager(mock_aioresponse):
    """Test the feed manager."""
    home_coordinates = (-41.2, 174.7)
    mock_aioresponse.get(
        "https://api.geonet.org.nz/volcano/val",
        status=HTTPStatus.OK,
        body=load_fixture("val-1.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        async def _generate_entity(external_id):
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        async def _update_entity(external_id):
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        async def _remove_entity(external_id):
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        feed_manager = GeonetnzVolcanoFeedManager(
            websession,
            _generate_entity,
            _update_entity,
            _remove_entity,
            home_coordinates,
        )
        assert (
            repr(feed_manager) == "<GeonetnzVolcanoFeedManager("
            "feed=<GeonetnzVolcanoFeed("
            "home=(-41.2, 174.7), url=https://"
            "api.geonet.org.nz/volcano/val, "
            "radius=None)>)>"
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 3
        assert feed_manager.last_timestamp is None
        assert len(generated_entity_external_ids) == 3
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0

        # Simulate an update with empty result.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_aioresponse.get(
            "https://api.geonet.org.nz/volcano/val",
            status=HTTPStatus.OK,
            body=load_fixture("val-2.json"),
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 3
        assert len(generated_entity_external_ids) == 0
        # Instead of removing entities, we're just updating existing ones.
        assert len(updated_entity_external_ids) == 3
        assert len(removed_entity_external_ids) == 0

        # Simulate an update with result.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_aioresponse.get(
            "https://api.geonet.org.nz/volcano/val",
            status=HTTPStatus.OK,
            body=load_fixture("val-1.json"),
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 3
        assert len(generated_entity_external_ids) == 0
        assert len(updated_entity_external_ids) == 3
        assert len(removed_entity_external_ids) == 0
        assert entries["volcano2"].title == "Volcano 2"
        last_update = feed_manager.last_update
        last_update_successful = feed_manager.last_update_successful

        # Simulate an update with empty result.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        with async_mock.patch(
            "aio_geojson_client.feed.GeoJsonFeed._fetch",
            new_callable=async_mock.AsyncMock,
        ) as mock_fetch:
            mock_fetch.return_value = (UPDATE_OK_NO_DATA, None)

            await feed_manager.update()
            entries = feed_manager.feed_entries

            assert len(entries) == 3
            assert len(generated_entity_external_ids) == 0
            # Instead of removing entities, we're just updating existing ones.
            assert len(updated_entity_external_ids) == 3
            assert len(removed_entity_external_ids) == 0
            assert feed_manager.last_update is not last_update
            assert feed_manager.last_update_successful is not last_update_successful
            last_update = feed_manager.last_update
            last_update_successful = feed_manager.last_update_successful

        # Simulate an update with error result.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        with async_mock.patch(
            "aio_geojson_client.feed.GeoJsonFeed._fetch",
            new_callable=async_mock.AsyncMock,
        ) as mock_fetch:
            mock_fetch.return_value = (UPDATE_ERROR, None)

            await feed_manager.update()
            entries = feed_manager.feed_entries

            assert len(entries) == 3
            assert len(generated_entity_external_ids) == 0
            # Instead of removing entities, we're just updating existing ones.
            assert len(updated_entity_external_ids) == 3
            assert len(removed_entity_external_ids) == 0
            assert feed_manager.last_update is not last_update
            assert feed_manager.last_update_successful == last_update_successful
            last_update = feed_manager.last_update
            last_update_successful = feed_manager.last_update_successful

        # Simulate an update with result.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_aioresponse.get(
            "https://api.geonet.org.nz/volcano/val",
            status=HTTPStatus.OK,
            body=load_fixture("val-3.json"),
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 4
        assert len(generated_entity_external_ids) == 1
        assert len(updated_entity_external_ids) == 2
        assert len(removed_entity_external_ids) == 0
        assert entries["volcano2"].title == "Volcano 2 UPDATED"
        assert feed_manager.last_update is not last_update
        assert feed_manager.last_update_successful is not last_update_successful
