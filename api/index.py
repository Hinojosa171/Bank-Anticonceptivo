import os
import json
from flask import Request, Response

CLASES = {
    0: "No utilizó ningún método anticonceptivo",
    1: "Sí utilizó un método anticonceptivo a corto plazo",
    2: "Sí utilizó un método anticonceptivo a largo plazo",
}

def handler(request: Request):
    """Root endpoint for health checks"""
    response_data = {
        "mensaje": "API Anticonceptivos funcionando en Vercel",
        "estado": "activo",
        "version": "1.0",
        "endpoints": ["/api/ping", "/api/predict"]
    }
    return Response(
        json.dumps(response_data),
        status=200,
        mimetype='application/json',
        headers={"Access-Control-Allow-Origin": "*"}
    )
