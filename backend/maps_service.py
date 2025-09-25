import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def search_places(query: str):
    """
    Generate Google Maps embed URL + search URL dari query.
    """
    embed_url = f"https://www.google.com/maps/embed/v1/search?key={API_KEY}&q={query}"
    maps_url = f"https://www.google.com/maps/search/?api=1&query={query.replace(' ', '+')}"
    
    return [{
        "query": query,
        "embed_url": embed_url,
        "maps_url": maps_url
    }]
