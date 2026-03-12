import json
from flask import Request, Response

def handler(request: Request):
    """Ping endpoint para verificar que la API está viva"""
    return Response(
        "pong",
        status=200,
        mimetype='text/plain',
        headers={"Access-Control-Allow-Origin": "*"}
    )
