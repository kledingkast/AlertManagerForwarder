from flask import Flask, request, jsonify
import requests
import os
import logging
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtenha o URL do Alertmanager externo a partir da variável de ambiente
ALERTMANAGER_EXTERNAL_URL = os.getenv("ALERTMANAGER_EXTERNAL_URL", "http://127.0.0.1:9093/api/v1/alerts")

@app.route('/', methods=['POST'])
def redirect_alertmanager():
    try:
        data = request.get_json()
        logger.info("Recebido um alerta para redirecionamento")
        # logger.info("Conteúdo do alerta recebido: %s", data)

        # Extrai e converte o payload no formato que o Alertmanager espera
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

        # Envia o alerta formatado para o Alertmanager externo
        response = requests.post(ALERTMANAGER_EXTERNAL_URL, json=formatted_alerts)
        response.raise_for_status()

        logger.info("Alerta redirecionado com sucesso para %s", ALERTMANAGER_EXTERNAL_URL)
        return jsonify({"status": "alert sent", "alertmanager_response": response.json()}), response.status_code

    except requests.exceptions.RequestException as e:
        logger.error("Falha ao redirecionar o alerta: %s", str(e))
        return jsonify({"status": "failed to send alert", "error": str(e)}), 500