import json
import numpy as np
from flask import Request
from api.model_loader import get_model, get_scaler, CLASES

def handler(request: Request):
    """Serverless predict endpoint with proper CORS"""
    
    # CORS Headers to include in all responses
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS, GET",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age": "3600"
    }
    
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return ("", 204, cors_headers)
    
    if request.method != "POST":
        return (
            json.dumps({"error": "Use POST method"}),
            405,
            {**cors_headers, "Content-Type": "application/json"}
        )

    # Load model and scaler
    model = get_model()
    scaler = get_scaler()
    
    if model is None or scaler is None:
        return (
            json.dumps({"error": "Modelo o scaler no disponible"}),
            503,
            {**cors_headers, "Content-Type": "application/json"}
        )

    # Parse JSON
    try:
        datos = request.get_json()
        print("📨 Datos recibidos:", datos)
    except Exception as e:
        print(f"❌ Error al parsear JSON: {str(e)}")
        return (
            json.dumps({"error": "JSON inválido"}),
            400,
            {**cors_headers, "Content-Type": "application/json"}
        )

    # Required fields
    campos = [
        "edad", "educacion_mujer", "educacion_esposo", "numero_hijos",
        "religion", "trabaja_esposa", "ocupacion_esposo", "nivel_vida",
        "exposicion_medios"
    ]

    # Validate fields exist
    for campo in campos:
        if campo not in datos:
            return (
                json.dumps({"error": f"Falta el campo: {campo}"}),
                400,
                {**cors_headers, "Content-Type": "application/json"}
            )

    # Convert to float
    try:
        entrada = np.array([[
            float(datos["edad"]),
            float(datos["educacion_mujer"]),
            float(datos["educacion_esposo"]),
            float(datos["numero_hijos"]),
            float(datos["religion"]),
            float(datos["trabaja_esposa"]),
            float(datos["ocupacion_esposo"]),
            float(datos["nivel_vida"]),
            float(datos["exposicion_medios"]),
        ]])
        print("✅ Array de entrada creado")
    except (ValueError, TypeError) as e:
        return (
            json.dumps({"error": f"Valor inválido: {str(e)}"}),
            400,
            {**cors_headers, "Content-Type": "application/json"}
        )

    # Scale
    try:
        entrada_escalada = scaler.transform(entrada)
        print("✅ Entrada escalada")
    except Exception as e:
        return (
            json.dumps({"error": f"Error al escalar: {str(e)}"}),
            500,
            {**cors_headers, "Content-Type": "application/json"}
        )

    # Predict
    try:
        prediccion = model.predict(entrada_escalada, verbose=0)
        print("✅ Predicción realizada")
    except Exception as e:
        return (
            json.dumps({"error": f"Error en predicción: {str(e)}"}),
            500,
            {**cors_headers, "Content-Type": "application/json"}
        )

    # Get class and probabilities
    clase = int(np.argmax(prediccion[0]))
    probabilidades = {
        CLASES[i]: round(float(prediccion[0][i]) * 100, 2)
        for i in range(3)
    }

    respuesta = {
        "clase": clase,
        "resultado": CLASES[clase],
        "probabilidades": probabilidades
    }
    
    return (
        json.dumps(respuesta),
        200,
        {**cors_headers, "Content-Type": "application/json"}
    )
