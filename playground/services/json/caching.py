import os

from django.core.cache import cache
from django.conf import settings as conf_settings
from playground.services.json.json_validator import get_json_if_valid


def get_cached_json(filename, schema_filename, timeout=60 * 5):
    """
    Retrieves JSON data from cache or reloads it if not cached.

    :param filename: The JSON file to load.
    :param schema_filename: The schema file for validation.
    :param timeout: Cache expiration time in seconds.
    :return: Valid JSON data or None.
    """
    json_path = conf_settings.MEDIA_ROOT / "data" / filename
    json_schema_path = conf_settings.MEDIA_ROOT / "data_schemas" / schema_filename

    file_mtime = os.path.getmtime(json_path)

    cache_key = f"cached_{filename}"
    cached_data = cache.get(cache_key)

    if cached_data and cached_data.get("mtime") == file_mtime:
        return cached_data["data"]

    json_data = get_json_if_valid(json_path, json_schema_path)

    if json_data is not None:
        cache.set(cache_key, {"data": json_data, "mtime": file_mtime}, timeout)

    return json_data
