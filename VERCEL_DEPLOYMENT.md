# 🚀 Deployment Guide - Vercel Serverless

This backend is configured for **Vercel serverless functions**. The structure supports both local development and cloud deployment.

## 📁 Project Structure

```
backend2/
├── api/                          # Serverless functions
│   ├── __init__.py
│   ├── index.py                 # GET / endpoint
│   ├── ping.py                  # GET /api/ping health check
│   ├── predict.py               # POST /api/predict (main ML endpoint)
│   └── model_loader.py          # Shared model/scaler loading
├── modelo_anticonceptivo.keras  # ML model file
├── scaler.npy                   # Feature scaler
├── requirements.txt             # Python dependencies
├── vercel.json                  # Vercel configuration
├── app.py                       # OLD: Legacy Flask app (for local dev reference)
└── Procfile                     # OLD: Render-specific config
```

## 🔄 How It Works

### Serverless Functions
- **`/api/`** → `api/index.py` (health check)
- **`/api/ping`** → `api/ping.py` (ping endpoint)
- **`/api/predict`** → `api/predict.py` (ML predictions)

### Model Caching
The `api/model_loader.py` module caches the model and scaler in memory during execution to avoid reloading them on every request (improves cold start performance).

## 📝 Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Migrate to Vercel serverless"
git push origin main
```

### 2. Deploy to Vercel
**Option A: Vercel CLI**
```bash
npm install -g vercel
vercel --prod
```

**Option B: Vercel Dashboard**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Vercel auto-detects Python and deploys

### 3. Environment Variables (Optional)
No special env vars needed for this project.

## 🧪 Testing the API

After deployment, test with:

```bash
# Health check
curl https://your-project.vercel.app/api/

# Ping endpoint
curl https://your-project.vercel.app/api/ping

# Predict endpoint
curl -X POST https://your-project.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 25,
    "educacion_mujer": 3,
    "educacion_esposo": 2,
    "numero_hijos": 2,
    "religion": 1,
    "trabaja_esposa": 1,
    "ocupacion_esposo": 2,
    "nivel_vida": 3,
    "exposicion_medios": 2
  }'
```

## ✅ Differences from Render

| Aspect | Render | Vercel |
|--------|--------|--------|
| Architecture | Long-running Flask app | Serverless functions |
| Cold start | ~5-10s | ~2-3s |
| Memory | Fixed allocation | Per-function allocation |
| Cost | Always running | Pay per execution |
| File size | 250MB+ OK | 250MB total+ (fine for ML model) |

## 🐛 Troubleshooting

**"ModuleNotFoundError: No module named 'api'"**
- Ensure `/api/__init__.py` exists
- Check `vercel.json` is at project root

**"Model loading fails"**
- Verify `modelo_anticonceptivo.keras` and `scaler.npy` are committed to git
- Check file paths in `api/model_loader.py`

**"CORS errors"**
- Responses include `Access-Control-Allow-Origin: *`
- Update `vercel.json` if additional CORS headers needed

## 📚 References
- [Vercel Python Docs](https://vercel.com/docs/functions/quickstart/python)
- [Flask on Vercel](https://vercel.com/docs/concepts/functions/serverless-functions/python)
