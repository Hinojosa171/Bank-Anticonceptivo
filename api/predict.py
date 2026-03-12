import json
import numpy as np
from flask import Request, Response
from api.model_loader import get_model, get_scaler, CLASES

def handler(request: Request):
    """Serverless predict endpoint"""
    
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return Response(
            status=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )
    
    if request.method != "POST":
        return Response(
            json.dumps({"error": "Use POST method"}),
            status=405,
            mimetype='application/json'
        )

    # Load model and scaler
    model = get_model()
    scaler = get_scaler()
    
    if model is None or scaler is None:
        return Response(
            json.dumps({"error": "Modelo o scaler no disponible"}),
            status=503,
            mimetype='application/json'
        )

    # Parse JSON
    try:
        datos = request.get_json()
        print("📨 Datos recibidos:", datos)
    except Exception as e:
        print(f"❌ Error al parsear JSON: {str(e)}")
        return Response(
            json.dumps({"error": "JSON inválido"}),
            status=400,
            mimetype='application/json'
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
            return Response(
                json.dumps({"error": f"Falta el campo: {campo}"}),
                status=400,
                mimetype='application/json'
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
        return Response(
            json.dumps({"error": f"Valor inválido: {str(e)}"}),
            status=400,
            mimetype='application/json'
        )

    # Scale
    try:
        entrada_escalada = scaler.transform(entrada)
        print("✅ Entrada escalada")
    except Exception as e:
        return Response(
            json.dumps({"error": f"Error al escalar: {str(e)}"}),
            status=500,
            mimetype='application/json'
        )

    # Predict
    try:
        prediccion = model.predict(entrada_escalada, verbose=0)
        print("✅ Predicción realizada")
    except Exception as e:
        return Response(
            json.dumps({"error": f"Error en predicción: {str(e)}"}),
            status=500,
            mimetype='application/json'
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
    
    return Response(
        json.dumps(respuesta),
        status=200,
        mimetype='application/json',
        headers={"Access-Control-Allow-Origin": "*"}
    )
