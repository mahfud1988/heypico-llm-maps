import axios, { AxiosError } from "axios";

// Gunakan environment variable agar gampang switch dev/prod
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// ---- Types ----
export interface PlaceResult {
  query: string;
  embed_url: string;
  maps_url: string;
}

export interface SearchResponse {
  original_query: string;
  llm_query: string;
  results: PlaceResult[];
}

// ---- API call ----
export async function searchPlaces(query: string): Promise<SearchResponse | null> {
  try {
    const response = await axios.post<SearchResponse>(`${API_BASE}/search`, { query });
    return response.data;
  } catch (err) {
    const error = err as AxiosError;
    console.error("Error calling backend:", error.message);
    return null;
  }
}
