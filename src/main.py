import os

import log
import core
import config

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = config.NO_PUBSUB_MESSAGE_RECEIVED
        log.error(f"{msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = config.INVALID_PUBSUB_MESSAGE_FORMAT
        log.error(f"{msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    json_data = {}
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        json_data = core.validate_manifest(pubsub_message["data"])

    if json_data is None:
        log.error(config.NO_VALIDATE_JSON_SCHEMA)
    else:
        log.info(config.VALIDATE_JSON_SCHEMA)
        core.datastore_publish(json_data, json_data["id"])

    return ("OK", 204)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
