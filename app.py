"""
Flask wrapper for Vercel Deployment
Compatible with serverless functions
"""
import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import shared model loader
from api.model_loader import get_model, get_scaler, CLASES

# Initialize Flask app
app = Flask(__name__)
CORS(app)


@app.route('/api/', methods=['GET', 'HEAD', 'OPTIONS'])
def api_index():
    """Health check endpoint"""
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({
        "mensaje": "✅ API Anticonceptivos en Vercel funcionando",
        "estado": "activo",
        "version": "1.0",
        "endpoints": {
            "health": "/api/",
            "ping": "/api/ping",
            "predict": "/api/predict"
        }
    }), 200


@app.route('/api/ping', methods=['GET', 'OPTIONS'])
def api_ping():
    """Ping endpoint - simple health check"""
    if request.method == 'OPTIONS':
        return '', 204
    return "pong", 200


@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def api_predict():
    """ML prediction endpoint"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Parse request
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "Empty request body"}), 400
        
        print("📨 Datos recibidos:", datos)
        
        # Load model and scaler
        model = get_model()
        scaler = get_scaler()
        
        if model is None or scaler is None:
            return jsonify({"error": "Modelo o scaler no disponible"}), 503

        # Required fields
        campos = [
            "edad", "educacion_mujer", "educacion_esposo", "numero_hijos",
            "religion", "trabaja_esposa", "ocupacion_esposo", "nivel_vida",
            "exposicion_medios"
        ]

        # Validate all fields exist
        missing = [c for c in campos if c not in datos]
        if missing:
            return jsonify({"error": f"Campos faltantes: {missing}"}), 400

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
            print("✅ Array de entrada creado")
        except (ValueError, TypeError, KeyError) as e:
            return jsonify({"error": f"Valor inválido: {str(e)}"}), 400

        # Scale input
        try:
            entrada_escalada = scaler.transform(entrada)
            print("✅ Input escalado")
        except Exception as e:
            return jsonify({"error": f"Error escalando: {str(e)}"}), 500

        # Make prediction
        try:
            prediccion = model.predict(entrada_escalada, verbose=0)
            print("✅ Predicción realizada")
        except Exception as e:
            return jsonify({"error": f"Error en predicción: {str(e)}"}), 500

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
        return jsonify(respuesta), 200

    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)