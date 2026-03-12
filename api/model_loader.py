import os
import numpy as np
from tensorflow.keras.models import load_model

# Global variables for caching (serverless cold start optimization)
_model = None
_scaler = None

CLASES = {
    0: "No utilizó ningún método anticonceptivo",
    1: "Sí utilizó un método anticonceptivo a corto plazo",
    2: "Sí utilizó un método anticonceptivo a largo plazo",
}

def get_model():
    """Load model with caching for serverless"""
    global _model
    if _model is None:
        try:
            model_path = os.path.join(os.path.dirname(__file__), "..", "modelo_anticonceptivo.keras")
            _model = load_model(model_path)
            print("✅ Modelo cargado correctamente")
        except Exception as e:
            print(f"❌ ERROR al cargar modelo: {str(e)}")
            _model = None
    return _model

def get_scaler():
    """Load scaler with caching for serverless"""
    global _scaler
    if _scaler is None:
        try:
            scaler_path = os.path.join(os.path.dirname(__file__), "..", "scaler.npy")
            _scaler = np.load(scaler_path, allow_pickle=True).item()
            print("✅ Scaler cargado correctamente")
        except Exception as e:
            print(f"❌ ERROR al cargar scaler: {str(e)}")
            _scaler = None
    return _scaler
