# encoding: utf-8
"""
Config and Constants
"""
# PUBSUB MESSAGE
NO_PUBSUB_MESSAGE_RECEIVED = "No Pub/Sub message received!"
INVALID_PUBSUB_MESSAGE_FORMAT = "invalid Pub/Sub message format!"

# JSON VALIDATE MESSAGE
VALIDATE_JSON_SCHEMA = "The JSON is Validate!!!!"
NO_VALIDATE_JSON_SCHEMA = "The JSON no Validate!!!!"

# MANIFEST SCHEMA
MANIFEST_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Model Schema Manifest Data Platform",
    "required": ["id", "meta", "schema_contract", "title", "description"],
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "meta": {
            "type": "object",
            "properties": {
                "source_host": {
                    "type": "string",
                    "description": "Local of the source data",
                },
                "source_format": {
                    "type": "string",
                    "description": "Format of the source data \
                        (Database, CSV, Parquet)",
                },
                "source_holder": {
                    "type": "string",
                    "description": "Holder or Owner of the source data",
                },
                "source_db": {
                    "type": "string",
                    "description": "Name of database of Source data \
                        (Case Database Origin)",
                },
                "source_table": {
                    "type": "string",
                    "description": "Name of table of Source data \
                        (Case Database Origin)",
                },
                "ingestion_type": {
                    "type": "string",
                    "description": "Type of ingestion (Incremental, Compĺete)",
                },
                "ingestion_frequency": {
                    "type": "integer",
                    "description": "Frequency of update data into platform \
                        (seconds)",
                },
                "activated_data": {
                    "type": "boolean",
                    "description": "The data is activate or not (true/false)",
                },
                "restricted_data": {
                    "type": "boolean",
                    "description": "Contain restricted data (true/false)",
                },
                "topic_name": {
                    "type": "string",
                    "description": "Topic Name of Kafka",
                },
                "topic_env": {
                    "type": "string",
                    "description": "Topic kafka Enviroment \
                        (staging, production)",
                },
            },
        },
        "schema_contract": {
            "type": "array",
            "items": {"$ref": "#/$defs/schctr"},
        },
    },
    "$defs": {
        "schctr": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "field_name": {
                    "type": "string",
                    "description": "Define Field Name",
                },
                "field_type": {
                    "type": "string",
                    "description": "Define Field Type",
                },
                "field_description": {
                    "type": "string",
                    "description": "Define Field Description",
                },
            },
        }
    },
}
