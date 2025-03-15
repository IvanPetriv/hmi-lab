from __future__ import annotations

import json
import jsonschema
from jsonschema.exceptions import ValidationError


def get_json_if_valid(json_path: str, json_schema_path: str) -> dict | None:
    """
    Gets a JSON object if it matches the provided schema.
    :param json_path: File path to the JSON file
    :param json_schema_path: File path to the JSON schema file for comparing to the JSON data file.
    :return: JSON data object if it matches the schema, None otherwise
    """
    try:
        with open(json_path, encoding="utf-8") as json_file, \
             open(json_schema_path, encoding="utf-8") as json_schema_file:
            played_games_json: dict = json.load(json_file)
            played_games_json_schema: dict = json.load(json_schema_file)
            jsonschema.validate(instance=played_games_json, schema=played_games_json_schema)
        return played_games_json
    except ValidationError as e:
        return None
