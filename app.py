import os
import traceback
import numpy as np
import tensorflow as tf

# ------------------------------------------------------------
# CONFIGURACIÓN EXTREMA PARA MEMORIA LIMITADA (RENDER)
# ------------------------------------------------------------
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.optimizer.set_jit(False)
tf.config.set_visible_devices([], 'GPU')

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from tensorflow.keras.models import load_model

# ------------------------------------------------------------
# 1. RUTAS DE ARCHIVOS
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "modelo_anticonceptivo.keras")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.npy")

print("Iniciando aplicación...")
print(f"Ruta del modelo: {MODEL_PATH}")
print(f"Ruta del scaler: {SCALER_PATH}")

# ------------------------------------------------------------
# 2. CARGA DEL MODELO Y SCALER
# ------------------------------------------------------------
try:
    model = load_model(MODEL_PATH)
    print("Modelo cargado correctamente.")
except Exception as e:
    print(f"ERROR al cargar el modelo: {str(e)}")
    traceback.print_exc()
    # No relanzamos la excepción para que la app pueda arrancar
    model = None

try:
    scaler = np.load(SCALER_PATH, allow_pickle=True).item()
    print("Scaler cargado correctamente. Tipo:", type(scaler))
except Exception as e:
    print(f"ERROR al cargar el scaler: {str(e)}")
    traceback.print_exc()
    scaler = None

# ------------------------------------------------------------
# 3. DEFINICIÓN DE CLASES Y APLICACIÓN FLASK
# ------------------------------------------------------------
CLASES = {
    0: "No utilizó ningún método anticonceptivo",
    1: "Sí utilizó un método anticonceptivo a corto plazo",
    2: "Sí utilizó un método anticonceptivo a largo plazo",
}

app = Flask(__name__)

# Configuración CORS simple y robusta (eliminamos duplicados)
CORS(app, origins="*", allow_headers=["Content-Type"], methods=["GET", "POST", "OPTIONS"])

# Manejador global de excepciones (solo para errores no controlados)
@app.errorhandler(Exception)
def handle_exception(e):
    error_detalle = traceback.format_exc()
    print("Excepción no capturada:", str(e))
    print(error_detalle)
    response = jsonify({
        "error": "Error interno del servidor",
        "detalle": str(e) if app.debug else None
    })
    response.status_code = 500
    return response

# Manejador específico para 404 (rutas no encontradas)
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

# ------------------------------------------------------------
# 4. ENDPOINTS
# ------------------------------------------------------------
@app.route('/', methods=['GET', 'HEAD'])
def home():
    """Endpoint raíz para health checks de Render y acceso directo."""
    return jsonify({
        "mensaje": "API Anticonceptivos funcionando",
        "estado": "activo",
        "version": "1.0",
        "endpoints": ["/ping", "/predict"]
    })

@app.route('/ping', methods=['GET'])
def ping():
    """Endpoint de prueba para verificar que la app está viva."""
    return "pong"

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    # Verificar que el modelo y scaler estén disponibles
    if model is None or scaler is None:
        return jsonify({"error": "Modelo no disponible (error en carga)"}), 503

    print("Solicitud POST a /predict recibida")

    # Obtener datos JSON
    try:
        datos = request.get_json()
        print("Datos recibidos:", datos)
    except Exception as e:
        print("Error al parsear JSON:", str(e))
        return jsonify({"error": "JSON inválido"}), 400

    # Lista de campos requeridos
    campos = [
        "edad", "educacion_mujer", "educacion_esposo", "numero_hijos",
        "religion", "trabaja_esposa", "ocupacion_esposo", "nivel_vida",
        "exposicion_medios"
    ]

    # Verificar que todos los campos existen
    for campo in campos:
        if campo not in datos:
            print(f"Falta el campo: {campo}")
            return jsonify({"error": f"Falta el campo: {campo}"}), 400

    # Convertir a float con validación
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
        print("Array de entrada creado:", entrada)
    except (ValueError, TypeError) as e:
        print(f"Error de conversión: {str(e)}")
        return jsonify({"error": f"Valor inválido: {str(e)}"}), 400

    # Escalar
    try:
        entrada_escalada = scaler.transform(entrada)
        print("Entrada escalada:", entrada_escalada)
    except Exception as e:
        print(f"Error en scaler.transform: {str(e)}")
        return jsonify({"error": f"Error al escalar: {str(e)}"}), 500

    # Predecir
    try:
        prediccion = model.predict(entrada_escalada)
        print("Predicción cruda:", prediccion)
    except Exception as e:
        print(f"Error en model.predict: {str(e)}")
        return jsonify({"error": f"Error en la predicción: {str(e)}"}), 500

    # Obtener clase y probabilidades
    clase = int(np.argmax(prediccion[0]))
    probabilidades = {
        CLASES[i]: round(float(prediccion[0][i]) * 100, 2)
        for i in range(3)
    }
    print(f"Clase predicha: {clase} -> {CLASES[clase]}")
    print("Probabilidades:", probabilidades)

    # Respuesta
    respuesta = {
        "clase": clase,
        "resultado": CLASES[clase],
        "probabilidades": probabilidades
    }
    return jsonify(respuesta)

# ------------------------------------------------------------
# 5. ARRANQUE (para ejecución local, no usado por Gunicorn)
# ------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)