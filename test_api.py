#!/usr/bin/env python3
"""
Quick test script for Vercel serverless functions locally
Run: python test_api.py
"""

import json
import sys
from api.model_loader import get_model, get_scaler

def test_model_loading():
    """Test if model and scaler load correctly"""
    print("\n" + "="*60)
    print("🧪 Testing Model & Scaler Loading")
    print("="*60)
    
    model = get_model()
    scaler = get_scaler()
    
    if model is None:
        print("❌ Model failed to load")
        return False
    print("✅ Model loaded successfully")
    
    if scaler is None:
        print("❌ Scaler failed to load")
        return False
    print("✅ Scaler loaded successfully")
    
    return True

def test_predict():
    """Test prediction with sample data"""
    print("\n" + "="*60)
    print("🧪 Testing Prediction")
    print("="*60)
    
    import numpy as np
    
    model = get_model()
    scaler = get_scaler()
    
    if not model or not scaler:
        print("❌ Cannot test prediction: model or scaler not loaded")
        return False
    
    # Sample test data
    test_data = np.array([[25, 3, 2, 2, 1, 1, 2, 3, 2]])
    print(f"📥 Input data: {test_data}")
    
    try:
        scaled = scaler.transform(test_data)
        print(f"📈 Scaled data: {scaled}")
        
        prediction = model.predict(scaled, verbose=0)
        print(f"🔮 Raw prediction: {prediction}")
        
        class_idx = np.argmax(prediction[0])
        print(f"✅ Predicted class: {class_idx}")
        
        probas = [round(float(p) * 100, 2) for p in prediction[0]]
        print(f"📊 Probabilities: {probas}%")
        
        return True
    except Exception as e:
        print(f"❌ Prediction failed: {str(e)}")
        return False

def main():
    print("\n🚀 Vercel API Local Test Suite\n")
    
    # Test 1: Model loading
    if not test_model_loading():
        sys.exit(1)
    
    # Test 2: Prediction
    if not test_predict():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ All tests passed! Ready for Vercel deployment")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
