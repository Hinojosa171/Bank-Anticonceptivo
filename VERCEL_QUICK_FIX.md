# 🚀 INSTRUCCIONES FINALES PARA DESPLEGAR EN VERCEL

## ⚠️ EL PROBLEMA

Tu repo tiene esta estructura:
```
ROOT/
├── backend2/          ← AQUÍ ESTÁ TU APP
│   ├── api/
│   ├── requirements.txt
│   └── vercel.json
└── Front-Anticonceptivo-Check/
    └── index.html
```

Vercel busca `api/` en la **RAÍZ**, pero la tuya está en `backend2/`.

---

## ✅ SOLUCIÓN - SIGUE ESTOS PASOS EXACTOS

### **PASO 1: En Vercel Dashboard**

1. Ve a https://vercel.com/dashboard
2. Haz click en **"New Project"**
3. Selecciona **"Import Git Repository"**
4. Pega: `https://github.com/Hinojosa171/Bank-Anticonceptivo`

### **PASO 2: IMPORTANTE - Configura Correctamente**

Aquí es donde **falla la mayoría de gente**. Debes cambiar:

```
Root Directory: ./backend2
```

Así le dices a Vercel: "Busca los archivos Python dentro de la carpeta backend2"

### **PASO 3: Los demás campos**

- **Framework Preset**: "Other" (no Flask)
- **Build Command**: Debe estar auto-filled como `pip install -r requirements.txt`
- NO TOQUES NADA MÁS

### **PASO 4: Deploy**

1. Click en **"Deploy"**
2. Espera 2-3 minutos

---

## ✨ DESPUÉS DEL DEPLOY

Cuando termine, Vercel te dará una URL como:
```
https://bank-anticonceptivo-backend-abc123.vercel.app
```

### **Testa que funciona:**

```bash
# En tu navegador o terminal (curl)
curl https://bank-anticonceptivo-backend-abc123.vercel.app/api/
# Debe devolver JSON, no 404
```

### **Actualiza tu Frontend:**

En `Front-Anticonceptivo-Check/index.html` (línea ~340):

```javascript
const BACKEND_URL = "https://bank-anticonceptivo-backend-abc123.vercel.app/api/predict";
```

Luego:
```bash
cd Front-Anticonceptivo-Check
git add index.html
git commit -m "Update backend URL"
git push origin main
```

---

## 📋 CHECKLIST FINAL

- [ ] Root Directory set to `./backend2` en Vercel
- [ ] Framework: "Other"
- [ ] Clicked Deploy
- [ ] Esperé 2-3 minutos
- [ ] Testé `/api/` endpoint en navegador
- [ ] Actualicé frontend con nueva URL
- [ ] Committé y pushié cambios

---

## 🎯 LISTO!

Eso es todo. La clave es **Root Directory = `./backend2`**

Good luck! 🚀
