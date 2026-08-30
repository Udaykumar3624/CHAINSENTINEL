# 🚀 ChainSentinel Production Deployment Guide

This guide details how to deploy **ChainSentinel (SIH26146)** to production:
- **Frontend**: [Vercel](https://vercel.com) (Single Page Application)
- **Backend**: [Render](https://render.com) (FastAPI Python Web Service)
- **Database**: Render Managed PostgreSQL or Local SQLite fallback

---

## 1. ⚙️ Backend Deployment on Render

### Step 1: Create a Web Service on Render
1. Go to [Render Dashboard](https://dashboard.render.com/) and click **New +** $\rightarrow$ **Web Service**.
2. Connect your GitHub repository: `https://github.com/Udaykumar3624/CHAINSENTINEL`.
3. Configure the service settings:
   - **Name**: `chainsentinel-backend`
   - **Root Directory**: `backend`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 2: Set Environment Variables on Render
Add the following environment variables in the Render settings:
```env
ENVIRONMENT=production
JWT_SECRET_KEY=your-secure-random-32-character-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=600
CORS_ORIGINS=https://chainsentinel.vercel.app,http://localhost:5173
DATABASE_URL=sqlite:///./chainsentinel.db
LIVE_DATA_ENABLED=false
```

*(Note: Render assigns your backend a public URL, e.g. `https://chainsentinel-backend.onrender.com`).*

---

## 2. 🌐 Frontend Deployment on Vercel

### Step 1: Import Project to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New...** $\rightarrow$ **Project**.
2. Select your repository: `Udaykumar3624/CHAINSENTINEL`.
3. Configure project settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### Step 2: Set Environment Variables on Vercel
Add the backend API base URL environment variable:
```env
VITE_API_BASE_URL=https://chainsentinel-backend.onrender.com/api/v1
```

### Step 3: Deploy
Click **Deploy**. Vercel will build the frontend assets and automatically apply `vercel.json` SPA rewrite rules.

---

## 3. 🐳 Docker Deployment (Self-Hosted)

To run the complete platform using Docker Compose:

```bash
docker-compose up --build -d
```

- **Frontend**: `http://localhost:5173`
- **Backend API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
