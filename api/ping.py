import json

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600"
}

def handler(request):
    """Ping endpoint para verificar que la API está viva"""
    
    if request.method == "OPTIONS":
        return ("", 204, CORS_HEADERS)
    
    return (
        "pong",
        200,
        {**CORS_HEADERS, "Content-Type": "text/plain"}
    )
