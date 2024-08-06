<template>
  <div>
    <h1>Informations sur la Localité</h1>
    <input v-model="location" placeholder="Entrez une localité" />
    <button @click="fetchLocationData">Obtenir des informations</button>

    <div v-if="loading">Chargement des données...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div id="map" style="height: 400px;"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import L from 'leaflet'; // Importer Leaflet

const location = ref('');
const coordinates = ref([]);
const loading = ref(false);
const error = ref(null);
let map = null; // Référence à la carte

onMounted(() => {
  initMap(); // Initialiser la carte uniquement une fois le composant monté
});

const fetchLocationData = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${location.value}`);

    if (!response.ok) {
      throw new Error("Erreur de réseau");
    }

    const data = await response.json();

    if (data && data.length > 0) {
      const { lat, lon } = data[0];
      coordinates.value.push({ lat, lon }); // Ajouter les coordonnées à la liste
      updateMap(lat, lon); // Mettre à jour la carte avec les nouvelles coordonnées
    } else {
      error.value = "Aucune donnée trouvée pour cette localité.";
    }
  } catch (err) {
    error.value = "Erreur lors de la récupération des données : " + err.message;
  } finally {
    loading.value = false;
  }
};

const initMap = () => {
  // Vérifier si la carte est déjà initialisée
  if (!map) {
    map = L.map('map').setView([51.505, -0.09], 2); // Vue par défaut sur le monde

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap',
    }).addTo(map);
  }
};

const updateMap = (lat, lon) => {
  // Ajouter un marqueur pour le nouveau lieu
  L.marker([lat, lon]).addTo(map)
    .bindPopup('Localité: ' + location.value)
    .openPopup();

  // Ajouter un cercle bleu autour du lieu trouvé
  L.circle([lat, lon], {
    color: 'blue',
    radius: 500, // Rayon en mètres
    fillOpacity: 0.5
  }).addTo(map);

  // Centrer la carte sur le dernier lieu ajouté
  map.setView([lat, lon], 13);
};
</script>

<style>
#map {
  width: 100%;
  height: 400px;
}
.error {
  color: red;
}
</style>
