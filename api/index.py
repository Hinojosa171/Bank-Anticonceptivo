import json

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

def handler(request):
    """Root health check endpoint"""
    
    if request.method == "OPTIONS":
        return ("", 204, CORS_HEADERS)
    
    response_data = {
        "mensaje": "✅ API Anticonceptivos en Vercel funcionando",
        "estado": "activo",
        "version": "1.0",
        "endpoints": {
            "health": "/api/",
            "ping": "/api/ping",
            "predict": "/api/predict"
        }
    }
    
    return (
        json.dumps(response_data),
        200,
        {**CORS_HEADERS, "Content-Type": "application/json"}
    )
