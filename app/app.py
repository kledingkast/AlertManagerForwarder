from flask import Flask, request, jsonify
import requests
import os
import logging
from datetime import datetime, timedelta

app = Flask(__name__)

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the external Alertmanager URL from the environment variable
ALERTMANAGER_EXTERNAL_URL = os.getenv("ALERTMANAGER_EXTERNAL_URL", "http://127.0.0.1:9093/api/v1/alerts")

@app.route('/', methods=['POST'])
def redirect_alertmanager():
    try:
        data = request.get_json()
        logger.info("Received an alert for redirection")
        # logger.info("Alert content received: %s", data)

        # Extract and convert the payload to the format expected by Alertmanager
        formatted_alerts = []
        for alert in data.get("alerts", []):
            formatted_alert = {
                "labels": alert.get("labels", {}),
                "annotations": alert.get("annotations", {}),
                "startsAt": alert.get("startsAt", datetime.utcnow().isoformat() + "Z"),
                "endsAt": alert.get("endsAt", (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"),
                "generatorURL": alert.get("generatorURL", ""),
            }
            formatted_alerts.append(formatted_alert)

        # Send the formatted alert to the external Alertmanager
        response = requests.post(ALERTMANAGER_EXTERNAL_URL, json=formatted_alerts)
        response.raise_for_status()

        logger.info("Alert successfully redirected to %s", ALERTMANAGER_EXTERNAL_URL)
        return jsonify({"status": "alert sent", "alertmanager_response": response.json()}), response.status_code

    except requests.exceptions.RequestException as e:
        logger.error("Failed to redirect the alert: %s", str(e))
        return jsonify({"status": "failed to send alert", "error": str(e)}), 500
