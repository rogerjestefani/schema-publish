# encoding: utf-8
"""
Core
"""
import json
import pytz

from typing import Any, Dict
from base64 import b64decode
from datetime import datetime
from google.cloud import datastore
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

import config
import log


def current_datetime():
    return datetime.now(pytz.timezone("America/Sao_Paulo")).isoformat()


def validate_schema(doc_value: json, schema_properties: json) -> bool:
    """
        Parameters
        ----------
        doc_value : json
            The document json to validate
        schema_properties : json
            Json schema with properties to validate doc_value
    import datetime
        Returns
        -------
        Boolean
            Return with the boolean value

    """
    try:
        validate(instance=doc_value, schema=schema_properties)
    except (ValidationError, SchemaError):
        return False
    return True


def validate_manifest(pubsub_message: Any) -> Dict[str, Any]:
    """
    Parameters
    ----------
    pubsub_message : str
        Pub/Sub Message to Validate
    Returns
    -------
    JSON Manifest, Dict
        Return JSON dict with Manifest Config

    """
    json_manifest = json.loads(b64decode(pubsub_message).decode("utf-8"))
    print(json_manifest)
    try:
        result = validate_schema(json_manifest, config.MANIFEST_SCHEMA)
        if result:
            return json_manifest
        return None
    except ValueError:  # Invalid JSON
        return None


def datastore_publish(json_manifest: json, id: str):
    """
    Parameters
    ----------
    json_manifest : json
        JSON with Manifest contract
    id : str
        Id of Manifest
    Returns
    -------
    None
    """
    # Instantiates a client
    datastore_client = datastore.Client()

    # The kind for the new entity
    kind = "schema-repository"
    # The Cloud Datastore key for the new entity
    task_key = datastore_client.key(kind, id)

    # Verify if Document Alredy Exists and
    # update `version`` and `last_update`` values
    #
    task_result = datastore_client.get(task_key)
    version = (
        int(task_result["manifest"]["meta"]["version"]) + 1
        if task_result is not None
        else 1
    )

    json_manifest["meta"]["version"] = version
    json_manifest["meta"]["last_update"] = current_datetime()

    # Prepares the new entity
    task = datastore.Entity(key=task_key)
    task["manifest"] = json_manifest

    # Saves the entity
    datastore_client.put(task)

    log.info(f"Saved {task.key.name}: {task['manifest']}")
