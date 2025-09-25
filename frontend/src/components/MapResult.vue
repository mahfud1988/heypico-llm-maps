<template>
  <div>
    <!-- Form input -->
    <form @submit.prevent="search">
      <input
        v-model="query"
        type="text"
        placeholder="Cari tempat..."
        required
      />
      <button type="submit" :disabled="loading">
        {{ loading ? "Searching..." : "Search" }}
      </button>
    </form>

    <!-- Skeleton saat loading -->
    <div v-if="loading" class="skeleton-container">
      <div class="skeleton skeleton-text"></div>
      <div class="skeleton skeleton-iframe"></div>
      <div class="skeleton skeleton-link"></div>
    </div>

    <!-- Hasil pencarian -->
    <div v-else-if="result">
      <h3>Query LLM: {{ result.llm_query }}</h3>

      <iframe
        v-if="result.embed_url"
        :src="result.embed_url"
        width="600"
        height="450"
        style="border:0;"
        allowfullscreen
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
      ></iframe>

      <p v-if="result.maps_url">
        <a :href="result.maps_url" target="_blank" rel="noopener noreferrer">
          Open in Google Maps
        </a>
      </p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";

interface Result {
  llm_query: string;
  embed_url: string;
  maps_url: string;
}

const query = ref("");
const result = ref<Result | null>(null);
const loading = ref(false);

const search = () => {
  if (!query.value) return;

  loading.value = true;
  result.value = null;

  fetch("http://127.0.0.1:8000/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: query.value }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.results && data.results.length) {
        const placeName = data.results[0].name || data.llm_query;
        result.value = {
          llm_query: data.llm_query,
          embed_url: `https://www.google.com/maps?q=${encodeURIComponent(
            placeName
          )}&output=embed`,
          maps_url: `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
            placeName
          )}`,
        };
      }
    })
    .catch((err) => console.error("Error fetching search:", err))
    .finally(() => {
      loading.value = false;
    });
};
</script>

<style scoped>
form {
  margin-bottom: 1rem;
}

input {
  padding: 0.5rem;
  margin-right: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  background-color: #0078ff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #005fcc;
}

/* Skeleton */
.skeleton-container {
  margin-top: 1rem;
}

.skeleton {
  background: linear-gradient(90deg, #eee 25%, #ddd 50%, #eee 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 0.75rem;
}

.skeleton-text {
  width: 200px;
  height: 20px;
}

.skeleton-iframe {
  width: 600px;
  height: 450px;
}

.skeleton-link {
  width: 150px;
  height: 16px;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}
</style>
