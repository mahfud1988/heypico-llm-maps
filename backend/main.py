from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from maps_service import search_places
from llm_service import ask_llm

app = FastAPI()

# --- CORS setup untuk frontend ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ganti sesuai alamat frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    """Health check / home endpoint"""
    return {"message": "LLM + Google Maps API backend is running!"}

# --- Endpoint lama: langsung ke Google Maps ---
@app.get("/places")
def get_places(query: str = Query(..., description="What place to search")):
    results = search_places(query)
    return {"query": query, "results": results}

# --- Endpoint baru: user prompt → LLM → Google Maps ---
class QueryRequest(BaseModel):
    query: str

@app.post("/search")
def search_with_llm(request: QueryRequest):
    # 1. Kirim prompt ke LLM
    prompt = (
        f"Convert the following user request into a Google Maps search query. "
        f"Output must be AT MOST 5 words, no explanations, no extra text. "
        f"User request: {request.query}"
    )
    llm_query = ask_llm(prompt)

    # fallback jika kosong
    if not llm_query:
        llm_query = "query not available"

    # 2. Dapatkan hasil URL dari maps_service
    results = search_places(llm_query)

    return {
        "original_query": request.query,
        "llm_query": llm_query,
        "results": results
    }
