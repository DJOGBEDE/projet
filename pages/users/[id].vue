<template>
  <v-container fluid fill-height>
    <v-row>
      <v-col cols="12" md="6">
        <v-card class="pa-4" outlined>
          <v-card-title class="text-h5 font-weight-bold">
            Détails de l'Atelier
          </v-card-title>
          <v-card-text>
            <div v-if="atelier">
              <v-row>
                <v-col cols="12" class="d-flex align-center mb-3">
                  <v-icon class="mr-2" color="primary">mdi-home-outline</v-icon>
                  <span class="font-weight-bold">{{ atelier.name }}</span>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <p class="info-text">
                    <v-icon class="mr-2" color="primary">mdi-home-outline</v-icon>
                    <strong>Adresse:</strong> {{ atelier.address }}
                  </p>
                  <p class="info-text">
                    <v-icon class="mr-2" color="primary">mdi-phone-outline</v-icon>
                    <strong>Téléphone:</strong> <a href="#" @click.prevent="contactByPhone">{{ atelier.phone_number }}</a>
                  </p>
                  <p class="info-text">
                    <v-icon class="mr-2" color="primary">mdi-web</v-icon>
                    <strong>Site Web:</strong> <a :href="atelier.website" target="_blank">{{ atelier.website }}</a>
                  </p>
                  <p class="info-text">
                    <v-icon class="mr-2" color="primary">mdi-clock-outline</v-icon>
                    <strong>Heures d'ouverture:</strong> {{ atelier.opening_hours }}
                  </p>
                  <p class="info-text">
                    <v-icon class="mr-2" color="primary">mdi-map-marker</v-icon>
                    <strong>Coordonnées:</strong> ({{ atelier.latitude }}, {{ atelier.longitude }})
                  </p>
                </v-col>
              </v-row>

              <v-divider class="my-4"></v-divider>

              <v-row>
                <v-col cols="12" md="6" class="mb-3">
                  <v-btn color="primary" @click="contactByPhone" class="d-flex align-center">
                    <v-icon left>mdi-phone</v-icon>
                    Contacter par Téléphone
                  </v-btn>
                </v-col>
                <v-col cols="12" md="6" class="mb-3">
                  <v-btn color="primary" @click="contactByEmail" class="d-flex align-center">
                    <v-icon left>mdi-email</v-icon>
                    Contacter par Email
                  </v-btn>
                </v-col>
              </v-row>

              <v-divider class="my-4"></v-divider>

              <v-row>
                <v-col cols="12">
                  <h4 class="font-weight-bold">Avis des Clients</h4>
                  <v-rating v-model="rating" color="amber" half-increments></v-rating>
                  <v-textarea v-model="clientReview" label="Donnez votre avis" outlined></v-textarea>
                  <v-btn color="success" @click="submitReview" class="mt-2">Soumettre l'Avis</v-btn>
                </v-col>
              </v-row>

              <v-divider class="my-4"></v-divider>

              <v-row>
                <v-col cols="12">
                  <h4 class="font-weight-bold">Galerie Photos</h4>
                  <v-img
                    v-for="photo in atelier.photos"
                    :key="photo"
                    :src="photo"
                    max-width="200"
                    class="ma-2"
                    transition="fade-transition"
                  />
                </v-col>
              </v-row>

              <v-divider class="my-4"></v-divider>

              <v-btn color="error" @click="reserve" class="mt-4" style="width: 100%;">
                Réserver
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="pa-4" outlined>
          <v-card-title class="text-h5 font-weight-bold">Carte des Ateliers</v-card-title>
          <v-card-text>
            <div id="map" style="height: 500px; width: 100%;"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useNuxtApp } from '#app';

// Définir des variables réactives pour stocker l'atelier et la carte
const atelier = ref(null);
const rating = ref(0);
const clientReview = ref('');
const { $leaflet } = useNuxtApp();
const map = ref(null);
const animatedMarker = ref(null);
const userCircle = ref(null);
let routeLine = null; // Pour stocker la ligne de l'itinéraire

// Récupérer l'atelier en fonction de l'ID passé dans l'URL
const route = useRoute();

onMounted(async () => {
  const atelierId = route.params.id; // Supposons que l'ID de l'atelier soit passé dans l'URL
  try {
    const response = await axios.get(`http://localhost:8080/api/ateliers/${atelierId}`);
    atelier.value = response.data;

    // Initialiser la carte Leaflet
    map.value = $leaflet.map('map').setView([6.4606, 2.4214], 13); // Centrer la carte sur Abomey-Calavi

    // Utilisation d'une couche OSM en anglais
    $leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map.value);

    // Obtenir la position de l'utilisateur (latitude et longitude)
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const userLat = position.coords.latitude;
        const userLng = position.coords.longitude;

        // Marqueur pour la position de l'utilisateur
        const userMarker = $leaflet.marker([userLat, userLng], {
          icon: $leaflet.icon({
            iconUrl: 'https://example.com/user-icon.png', // Remplacez par votre icône personnalisée
            iconSize: [25, 41],
            iconAnchor: [12, 41],
          }),
        }).addTo(map.value);
        userMarker.bindPopup('<b>Vous êtes ici!</b>').openPopup();

        // Encercle la position de l'utilisateur en rouge
        userCircle.value = $leaflet.circle([userLat, userLng], {
          color: 'red',
          radius: 100, // Rayon de 100 mètres
          fillOpacity: 0.5
        }).addTo(map.value);

        // Assurez-vous que l'atelier a des coordonnées
        if (atelier.value.latitude && atelier.value.longitude) {
          // Marqueur pour la destination de l'atelier
          const destination = [atelier.value.latitude, atelier.value.longitude];
          const destinationMarker = $leaflet.marker(destination).addTo(map.value);
          destinationMarker.bindPopup('<b>Destination: ' + atelier.value.name + '</b>').openPopup();

          // Tracer l'itinéraire entre l'utilisateur et la destination
          drawRoute([userLat, userLng], destination);

          // Animer le marqueur entre les deux points
          animateRoute([userLat, userLng], destination); // Animation modifiée

          // Ajuster la vue de la carte pour inclure les deux marqueurs
          map.value.fitBounds([userCircle.value.getLatLng(), destination]);
        } else {
          console.error('Les coordonnées de l\'atelier ne sont pas disponibles');
        }
      }, (error) => {
        console.error('Erreur de géolocalisation:', error);
      });
    }
  } catch (error) {
    console.error('Erreur lors de la récupération de l\'atelier:', error);
  }
});

// Fonction d'animation du cercle
function animateCircle() {
  let expanding = true;
  const maxRadius = 120; // Rayon maximum
  const minRadius = 100; // Rayon minimum
  const step = 0.5; // Vitesse d'animation

  function animate() {
    const currentRadius = expanding ? userCircle.value.getRadius() + step : userCircle.value.getRadius() - step;

    // Si le cercle atteint la taille maximum ou minimum, inverser la direction
    if (currentRadius >= maxRadius) expanding = false;
    if (currentRadius <= minRadius) expanding = true;

    userCircle.value.setRadius(currentRadius);
    requestAnimationFrame(animate);
  }

  animate(); // Démarrer l'animation
}

// Fonction pour tracer l'itinéraire
function drawRoute(start, end) {
  const latLngs = [start, end];
  if (routeLine) {
    map.value.removeLayer(routeLine); // Supprimer l'ancienne ligne si elle existe
  }
  routeLine = $leaflet.polyline(latLngs, { color: 'blue', weight: 4, opacity: 0.6 }).addTo(map.value);
}

// Fonction d'animation
function animateRoute(start, destination) {
  const duration = 4000; // Durée de l'animation (en ms)
  const steps = 100; // Nombre de pas d'animation
  const latStep = (destination[0] - start[0]) / steps;
  const lngStep = (destination[1] - start[1]) / steps;

  animatedMarker.value = $leaflet.marker(start).addTo(map.value);

  // Fonction d'animation
  function animate(direction) {
    for (let i = 0; i <= steps; i++) {
      setTimeout(() => {
        // Calculer la position actuelle en fonction de la direction
        const currentLat = start[0] + latStep * (direction === 'to' ? i : steps - i);
        const currentLng = start[1] + lngStep * (direction === 'to' ? i : steps - i);
        animatedMarker.value.setLatLng([currentLat, currentLng]);
      }, (duration / steps) * i);
    }

    // Après l'animation vers la destination, revenir à la position de départ
    setTimeout(() => {
      animate('from'); // Démarrer l'animation de retour
    }, duration + 100); // Pause avant de revenir
  }

  animate('to'); // Démarrer l'animation vers la destination
}

// Fonction pour contacter par téléphone
function contactByPhone() {
  window.open(`tel:${atelier.value.phone_number}`);
}

// Fonction pour contacter par email
function contactByEmail() {
  window.open(`mailto:${atelier.value.email}`);
}

// Fonction pour soumettre un avis
function submitReview() {
  // Logique pour soumettre un avis
  alert('Votre avis a été soumis avec succès!');
}

// Fonction pour réserver
function reserve() {
  // Logique pour réserver
  alert('Votre réservation a été effectuée!');
}
</script>

<style>
.info-text {
  margin: 10px 0;
}
</style>
