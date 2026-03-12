# ✅ Pre-Deployment Checklist

Run this checklist before uploading to Vercel:

## 📂 File Structure Check

- [ ] `api/` folder exists with all these files:
  - [ ] `__init__.py` (empty file)
  - [ ] `index.py` (health check)
  - [ ] `ping.py` (ping endpoint)
  - [ ] `predict.py` (ML predictions)
  - [ ] `model_loader.py` (shared utilities)

- [ ] Root level files:
  - [ ] `vercel.json` ✅ CORRECTED
  - [ ] `.vercelignore` ✅ UPDATED
  - [ ] `requirements.txt` ✅ FIXED
  - [ ] `modelo_anticonceptivo.keras` (ML model)
  - [ ] `scaler.npy` (Feature scaler)
  - [ ] `runtime.txt` (optional, but good to have)

## 🔧 Configuration Check

- [ ] `vercel.json` contains:
  - `"buildCommand": "pip install -r requirements.txt"`
  - `"headers"` section with CORS config
  - NO `"functions"` pattern (removed)

- [ ] `requirements.txt` pins:
  - `tensorflow-cpu==2.13.1` ✅
  - `keras==2.13.1` ✅
  - `numpy==1.24.3` ✅

- [ ] All `.py` files have `def handler(request):` function

## 🔗 Git/GitHub Check

- [ ] Latest changes committed:
  ```bash
  git log --oneline | head -5
  ```
  Should show:
  - "✅ Fix Vercel.json config..."
  - "🔧 Fix Vercel serverless CORS..."

- [ ] Latest commit pushed:
  ```bash
  git push origin main
  ```

## 🧪 Local Test (Optional)

- [ ] Can you import the modules locally?
  ```bash
  python -c "from api.model_loader import get_model, get_scaler; print('Imports OK')"
  ```

## 📋 Deployment Steps

1. [ ] Go to https://vercel.com/dashboard
2. [ ] Click "New Project"
3. [ ] Select "Import Git Repository"
4. [ ] Paste: `https://github.com/Hinojosa171/Bank-Anticonceptivo`
5. [ ] Choose branch: `main`
6. [ ] Framework Preset: **"Other"** (not Flask)
7. [ ] Root Directory: `./` (root of repo)
8. [ ] Build Command: Already set to pip install
9. [ ] Click "Deploy"
10. [ ] Wait 2-3 minutes for deployment
11. [ ] Check Deployments tab for status ✅

## 🎯 Post-Deployment

- [ ] Get your Vercel URL (looks like: `https://bank-anticonceptivo-xyz.vercel.app`)
- [ ] Test: `https://your-url.vercel.app/api/` (should return JSON)
- [ ] Update frontend `index.html` with new URL
- [ ] Commit and push frontend changes
- [ ] Test the full flow on frontend

---

## 🚀 You're Ready!

All fixes are applied and pushed to GitHub. Just need to deploy in Vercel! 
