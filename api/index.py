import os
import json

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "3600"
}

def handler(request):
    """Root endpoint for health checks"""
    
    if request.method == "OPTIONS":
        return ("", 204, CORS_HEADERS)
    
    response_data = {
        "mensaje": "API Anticonceptivos funcionando en Vercel",
        "estado": "activo",
        "version": "1.0",
        "endpoints": ["/api/ping", "/api/predict"]
    }
    
    return (
        json.dumps(response_data),
        200,
        {**CORS_HEADERS, "Content-Type": "application/json"}
    )
