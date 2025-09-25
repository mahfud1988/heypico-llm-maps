# HeyPico LLM + Google Maps Demo

This project demonstrates the integration of LLM (via Ollama) with Google Maps using a FastAPI backend and Vue 3 frontend.

---

## 📂 Project Structure

```
heypico-llm-maps/
├── backend/    # FastAPI backend + LLM service
└── frontend/   # Vue 3 + Vite frontend
```

---

## 🚀 How to Run

### 1. Backend
```
cd backend
python -m venv venv
source venv/Scripts/activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend
```
cd frontend
npm install
npm run dev
```
