CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

def handler(request):
    """Ping endpoint - simple health check"""
    
    if request.method == "OPTIONS":
        return ("", 204, CORS_HEADERS)
    
    return (
        "pong",
        200,
        {**CORS_HEADERS, "Content-Type": "text/plain"}
    )
