import json
import numpy as np
import os
from api.model_loader import get_model, get_scaler, CLASES

# CORS headers for all responses
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS, GET",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "3600",
}

def handler(request):
    """Serverless predict endpoint - Vercel Python Functions"""
    
    # Handle preflight CORS request
    if request.method == "OPTIONS":
        return ("", 204, CORS_HEADERS)
    
    if request.method != "POST":
        return (
            json.dumps({"error": "Method not allowed. Use POST."}),
            405,
            {**CORS_HEADERS, "Content-Type": "application/json"}
        )

    try:
        # Parse JSON body
        datos = request.get_json()
        if not datos:
            return (
                json.dumps({"error": "Empty request body"}),
                400,
                {**CORS_HEADERS, "Content-Type": "application/json"}
            )
        
        print("📨 Datos recibidos:", datos)
        
        # Load model and scaler
        model = get_model()
        scaler = get_scaler()
        
        if model is None or scaler is None:
            return (
                json.dumps({"error": "Modelo o scaler no disponible"}),
                503,
                {**CORS_HEADERS, "Content-Type": "application/json"}
            )

        # Required fields
        campos = [
            "edad", "educacion_mujer", "educacion_esposo", "numero_hijos",
            "religion", "trabaja_esposa", "ocupacion_esposo", "nivel_vida",
            "exposicion_medios"
        ]

        # Validate all fields exist
        missing = [c for c in campos if c not in datos]
        if missing:
            return (
                json.dumps({"error": f"Campos faltantes: {missing}"}),
                400,
                {**CORS_HEADERS, "Content-Type": "application/json"}
            )

        # Convert to float array
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
            print("✅ Array de entrada creado:", entrada)
        except (ValueError, TypeError, KeyError) as e:
            return (
                json.dumps({"error": f"Valor inválido: {str(e)}"}),
                400,
                {**CORS_HEADERS, "Content-Type": "application/json"}
            )

        # Scale input
        try:
            entrada_escalada = scaler.transform(entrada)
            print("✅ Input escalado")
        except Exception as e:
            return (
                json.dumps({"error": f"Error escalando: {str(e)}"}),
                500,
                {**CORS_HEADERS, "Content-Type": "application/json"}
            )

        # Make prediction
        try:
            prediccion = model.predict(entrada_escalada, verbose=0)
            print("✅ Predicción realizada:", prediccion)
        except Exception as e:
            return (
                json.dumps({"error": f"Error en predicción: {str(e)}"}),
                500,
                {**CORS_HEADERS, "Content-Type": "application/json"}
            )

        # Extract class and probabilities
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
        
        print("✅ Respuesta:", respuesta)
        
        return (
            json.dumps(respuesta),
            200,
            {**CORS_HEADERS, "Content-Type": "application/json"}
        )

    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return (
            json.dumps({"error": f"Error interno: {str(e)}"}),
            500,
            {**CORS_HEADERS, "Content-Type": "application/json"}
        )
