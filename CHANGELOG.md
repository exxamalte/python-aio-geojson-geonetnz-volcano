# Changes

## 0.10 (07/10/2024)
* Bump aio_geojson_client to 0.21.
* Removed Python 3.8 support.
* Code quality improvements.

## 0.9 (22/01/2024)
* Bumped version of upstream aio_geojson_client library to 0.20.
* Improved JSON parsing error handling, especially when not using Python's built-in JSON parsing library.
* Code quality improvements.
* Added Python 3.12 support.
* Removed Python 3.7 support.
* Bumped library versions: black, flake8, isort.
* Migrated to pytest.

## 0.8 (23/01/2023)
* Added Python 3.11 support (thanks @fabaff).
* Removed deprecated asynctest dependency (thanks @fabaff).
* Bumped version of upstream aio_geojson_client library to 0.18.

## 0.7 (18/02/2022)
* No functional changes.
* Added Python 3.10 support.
* Removed Python 3.6 support.
* Bumped version of upstream aio_geojson_client library to 0.16.
* Bumped library versions: black, flake8, isort.
* Migrated to github actions.

## 0.6 (08/06/2021)
* Python 3.9 compatibility.
* Add license tag.
* Bump aio_geojson_client to v0.14.
* Set aiohttp to a release 3.7.4 or later (thanks @fabaff).
* General code improvements.

## 0.5 (07/11/2019)
* Python 3.8 compatibility.

## 0.4 (24/09/2019)
* Bumped version of upstream GeoJSON library.

## 0.3 (20/09/2019)
* Call update entities callback in the case where the feed update did not 
  fetch any data

## 0.2 (19/09/2019)
* Feed manager keeps all entries instead of removing them if the feed 
  update is empty or fails intermittently.

## 0.1 (21/08/2019)
* Initial release with support for GeoNet NZ Volcanic Alert Level feed.
* Calculating distance to home coordinates.
* Support for filtering by distance.
* Filter out entries without any geo location data.
* Simple Feed Manager.
