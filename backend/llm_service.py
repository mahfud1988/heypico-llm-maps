import requests
import re
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def ask_llm(prompt: str, model: str = "mistral") -> str:
    """
    Kirim prompt ke Ollama LLM dan kembalikan query singkat untuk Google Maps.
    - Output maksimal 5 kata
    - Tanpa penjelasan tambahan, simbol aneh, atau karakter escape
    - Ada fallback jika kosong atau koneksi gagal
    """
    payload = {"model": model, "prompt": prompt}

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
        response.raise_for_status()
    except requests.RequestException:
        return "query not available"

    result_text = ""
    for line in response.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line.decode("utf-8"))
        except json.JSONDecodeError:
            continue

        if "response" in data:
            result_text += data["response"]

    # --- Cleanup ---
    # Hilangkan newline, tab, backslash, dan spasi ganda
    cleaned = re.sub(r"[\n\r\t\\]+", " ", result_text).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)

    # Ambil maksimal 5 kata
    words = cleaned.split()
    cleaned = " ".join(words[:5])

    # Fallback jika kosong
    if not cleaned:
        cleaned = "query not available"

    return cleaned
