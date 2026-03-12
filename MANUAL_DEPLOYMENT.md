# 🚀 Manual Deployment Guide - Vercel Backend

## ✅ Files Ready to Deploy

Your backend is now configured with the **corrected Vercel setup**. Here's what you need to do:

---

## 📝 Step 1: Manual Upload to Vercel

Since you're uploading manually, follow these steps in the Vercel dashboard:

### Option A: Git Import (Recommended)
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"New Project"**
3. Select **"Import Git Repository"**
4. Paste: `https://github.com/Hinojosa171/Bank-Anticonceptivo`
5. Choose branch: **`main`**
6. Configure:
   - **Framework Preset**: Select **"Other"** (not Flask - we're using serverless)
   - **Root Directory**: Leave as `./` (or `./backend2` if separating)
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: Leave blank

7. Click **"Deploy"**

### Option B: Manual File Upload
If you want to upload files directly:
1. In Vercel dashboard, click **"New Project"**
2. Upload your files directly
3. Make sure these files are in the root:
   - `vercel.json`
   - `requirements.txt`
   - `modelo_anticonceptivo.keras`
   - `scaler.npy`
4. Make sure `api/` folder contains:
   - `index.py`
   - `ping.py`
   - `predict.py`
   - `model_loader.py`
   - `__init__.py`

---

## ✅ What's Fixed Now

| Issue | Solution |
|-------|----------|
| "Pattern doesn't match" error | Removed `functions` config from `vercel.json` |
| CORS errors | Added global CORS headers in `vercel.json` |
| Import errors | Fixed `sys.path` in `predict.py` |
| Ignored files | Updated `.vercelignore` to keep necessary files |

---

## 📋 Project Structure (What Vercel Expects)

```
your-project/
├── api/                          ← Vercel auto-detects this folder
│   ├── __init__.py              ← Makes it a Python package
│   ├── index.py                 ← Creates /api endpoint
│   ├── ping.py                  ← Creates /api/ping endpoint
│   ├── predict.py               ← Creates /api/predict endpoint
│   └── model_loader.py          ← Shared utilities
├── modelo_anticonceptivo.keras  ← ML model file
├── scaler.npy                   ← Feature scaler
├── requirements.txt             ← Python dependencies
├── vercel.json                  ← Vercel configuration ✅ FIXED
├── .vercelignore               ← Files to exclude
└── README.md
```

---

## 🔍 Verification After Deployment

Once Vercel finishes deploying (usually 2-3 minutes):

### 1. Test Health Check
```
curl https://your-project.vercel.app/api/
```
Should return:
```json
{
  "mensaje": "✅ API Anticonceptivos en Vercel funcionando",
  "estado": "activo",
  "version": "1.0",
  "endpoints": { ... }
}
```

### 2. Test Ping
```
curl https://your-project.vercel.app/api/ping
```
Should return: `pong`

### 3. Test Predict
```bash
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

---

## 🔗 Update Frontend URL

After deployment, you'll get a URL like:
```
https://bank-anticonceptivo-xyz123.vercel.app
```

Update your **frontend** `index.html`:
```javascript
// Line ~340 in index.html
const BACKEND_URL = "https://bank-anticonceptivo-xyz123.vercel.app/api/predict";
```

Then commit and push:
```bash
git add index.html
git commit -m "Update backend URL"
git push
```

---

## ⚙️ Configuration Files Explained

### `vercel.json`
- **buildCommand**: Installs Python dependencies
- **headers**: Adds CORS headers globally for `/api/` routes

### `requirements.txt`
- **tensorflow-cpu==2.13.1**: Lightweight TensorFlow
- **keras==2.13.1**: Locked to Keras 2.x (compatible with model)
- **numpy==1.24.3**: Compatible with scaler pickle

### `model_loader.py`
- Caches model/scaler in memory during execution
- Avoids reloading on every request (cold start optimization)

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| 404 on `/api/predict` | Clear browser cache (Ctrl+Shift+Del) |
| CORS still blocked | Check Vercel deployment completed ✅ |
| Model fails to load | Ensure `modelo_anticonceptivo.keras` is committed to git |
| Scaler fails to load | Ensure `scaler.npy` is committed to git |
| Slow first request | Normal - first request (cold start) takes ~3-5s |

---

## 📚 Resources

- [Vercel Python Functions Docs](https://vercel.com/docs/functions/quickstart/python)
- [Vercel Configuration Reference](https://vercel.com/docs/projects/project-configuration)
- [CORS Policy Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

---

## ✨ Summary

Your backend is **ready to deploy**. Just:
1. Import repo from GitHub in Vercel
2. Let it auto-detect and deploy
3. Get your URL
4. Update frontend with that URL
5. Done! 🎉

Good luck! 🚀
