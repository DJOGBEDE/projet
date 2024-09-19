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
                          <v-btn color="primary"   height="50px" @click="contactByPhone" class="d-flex align-center">
                            <v-icon left>mdi-phone</v-icon>
                            Contacter par Téléphone
                          </v-btn>
                        </v-col>
                        <v-col cols="12" md="6" class="mb-3">
                          <v-btn color="green"   height="50px" @click="contactByWatsap" class="d-flex align-center">
                            <v-icon left>mdi-phone</v-icon>
                            Contacter WhatsApp
                          </v-btn>
                       
              </v-col>

                <v-col cols="12" md="6" class="mb-3">
                  <v-btn color="primary"   height="50px" @click="contactByEmail" class="d-flex align-center">
                    <v-icon left>mdi-email</v-icon>
                    Contacter par Email
                  </v-btn>
                </v-col>

                <button @click="showPaymentForm = true" class="pay-button">Payer</button>
                 
              </v-row>

                <!-- v-card pour entrer le montant et procéder au paiement -->
              <div v-if="showPaymentForm" class="payment-card">
                <div class="card-content">
                  <h3>Entrer le montant</h3>
                  <input v-model="amount" type="number" placeholder="Montant en CFA" class="amount-input" />

                  <button @click="open" class="proceed-button">Passer au paiement</button>
                  <button @click="closeForm" class="cancel-button">Annuler</button>
                </div>
              </div>
              
                      

              <v-divider class="my-4"></v-divider>

          

              <v-divider class="my-4"></v-divider>

                              <v-carousel cycle show-arrows>
                  <v-carousel-item
                    v-for="photo in photos"
                    :key="photo.id"
                    :src="`/uploads/${photo.file_path.split('/').pop()}`"
                  >
                    <v-img
                      :src="`/uploads/${photo.file_path.split('/').pop()}`"
                      height="200"
                      contain
                    ></v-img>
                  </v-carousel-item>
                </v-carousel>

              <v-divider class="my-4"></v-divider>


         
              <v-btn color="error"  height="50px" @click="openReservationDialog" class="mt-4" style="width: 100%;">
                Réserver
              </v-btn>
            </div>
          </v-card-text>
          <v-row>
                <v-col cols="12">
                  <h4 class="font-weight-bold">Avis des Clients</h4>
                  <v-rating v-model="rating" color="amber" half-increments></v-rating>
                  <v-textarea v-model="clientReview" label="Donnez votre avis" outlined></v-textarea>
                  <v-btn color="success" @click="submitReview" class="mt-2">Soumettre l'Avis</v-btn>
                </v-col>
              </v-row>
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
     <!-- Ajouter le bouton de paiement MTN MoMo -->
     
<!-- V-dialog pour la réservation -->
<v-dialog v-model="reservationDialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 font-weight-bold">
          Réservation
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Date"
                  type="date"
                  v-model="reservationDate"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="Heure"
                  type="time"
                  v-model="reservationTime"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-autocomplete
                  v-model="selectedServices"
                  :items="serviceNames"
                  label="Services"
                  multiple
                  required
                  clearable
                ></v-autocomplete>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="reservationMessage"
                  label="Message"
                  outlined
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="submitReservation">Envoyer</v-btn>
          <v-btn text @click="reservationDialog = false">Annuler</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    

  </v-container>
 
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
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

const reservationDialog = ref(false);
const reservationDate = ref('');
const reservationTime = ref('');
const selectedServices = ref([]);
const reservationMessage = ref('');
const ateliers = ref({ id: null, services: [] });
const serviceNames = ref([]);

const userData = ref(null); 
// Variables pour les fichiers photo
const photos = ref([]);
const profilePicture = ref(null);

// Récupérer l'atelier en fonction de l'ID passé dans l'URL
const route = useRoute();

const amount = ref(0); // Montant par défaut
const showPaymentForm = ref(false); // Contrôle de l'affichage de la v-card
const openKkiapayWidget = ref(null);
const removeKkiapayListener = ref(null);

// Fonction pour ouvrir le widget de paiement
const open = () => {
  if (openKkiapayWidget.value && amount.value > 0) {
    openKkiapayWidget.value({
      amount: amount.value, // Utiliser le montant entré par l'utilisateur
      api_key: 'a4d592906e9411ef94e0cb57a5c3525f', // Clé publique API
      sandbox: true, // Activer le mode test
      phone: '97000000', // Numéro de téléphone du client
    });
    // Fermer le formulaire une fois le paiement ouvert
    showPaymentForm.value = false;
  } else {
    alert('Veuillez entrer un montant valide');
  }
};

// Fonction pour fermer la carte de paiement
const closeForm = () => {
  showPaymentForm.value = false;
};

// Fonction de gestion du succès
const successHandler = (response) => {
  console.log('Paiement réussi :', response);
};

// Charger le widget au montage du composant
onMounted(async () => {
  const { openKkiapayWidget: openWidget, addKkiapayListener, removeKkiapayListener: removeListener } = await import('kkiapay');
  
  openKkiapayWidget.value = openWidget;
  removeKkiapayListener.value = removeListener;
  
  // Ajouter un listener pour le succès des transactions
  addKkiapayListener('success', successHandler);
});

// Nettoyage avant la destruction du composant
onBeforeUnmount(() => {
  if (removeKkiapayListener.value) {
    removeKkiapayListener.value('success', successHandler);
  }
});

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


function contactByWatsap() {
  const phoneNumber = atelier.value.phone_number;
  const url = `https://wa.me/${phoneNumber}`;
  
  // Détection si l'utilisateur est sur mobile ou ordinateur
  const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

  // Si mobile, tente d'ouvrir l'application WhatsApp
  if (isMobile) {
    window.open(url, '_blank');
  } else {
    // Sinon, redirige directement vers WhatsApp Web
    window.open(`https://web.whatsapp.com/send?phone=${phoneNumber}`, '_blank');
  }
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



const fetchUserData = async () => {
  // Vérifiez si vous êtes dans le client
  const token = process.client ? localStorage.getItem('token') : null; 
  if (token) {
    try {
      // Appel de l'API pour récupérer les données de l'utilisateur
      const response = await axios.get('http://localhost:8080/api/user', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      userData.value = response.data; // Stocker les données de l'utilisateur
    } catch (error) {
      console.error('Erreur lors de la récupération des données de l\'utilisateur:', error);
      userData.value = null; // Réinitialiser en cas d'erreur
    }
  }
};



const fetchAtelierId = () => {
  ateliers.value.id = route.params.id; // Récupérer l'ID de l'atelier à partir des paramètres de la route
};

const fetchServices = async () => {
  if (!ateliers.value.id) return; // Vérifier si l'ID de l'atelier est disponible

  try {
    const response = await axios.get(`http://localhost:8080/api/services?workshop_id=${ateliers.value.id}`);
    ateliers.value.services = response.data; // Assigner les services récupérés
    serviceNames.value = response.data.map(service => service.name); // Récupérer seulement les noms des services
  } catch (error) {
    console.error("Erreur lors de la récupération des services:", error);
  }
};

// Fonction pour soumettre une réservation
const submitReservation = async () => {
  const atelier_id = parseInt(ateliers.value.id, 10);
  const reservationData = {
    user_id: userData.value.id,
    atelier_id: atelier_id,
    date: reservationDate.value,
    time: reservationTime.value,
    services: selectedServices.value,
    message: reservationMessage.value,
  };

  try {
    const response = await axios.post('http://localhost:8080/api/reservations', reservationData);
    console.log('Réservation créée:', response.data);
    alert('Votre réservation a été effectuée avec succès !');
    reservationDialog.value = false;
    resetForm();
  } catch (error) {
    console.error('Erreur lors de la création de la réservation:', error);
    alert('Une erreur est survenue lors de la réservation. Veuillez réessayer.');
  }
};

onMounted(async () => {
  await fetchUserData();
  fetchAtelierId();
  await fetchServices();

  // Votre code précédent pour l'initialisation de la carte et autres éléments continue ici
});


const resetForm = () => {
  reservationDate.value = '';
  reservationTime.value = '';
  selectedServices.value = [];
  reservationMessage.value = '';
};

// Appels de fonction lors de l'initialisation
onMounted(async () => {
  await fetchUserData();
  fetchAtelierId();
  await fetchServices();
  fetchPhotos()
});

// Ouvrir le dialogue de réservation
const openReservationDialog = () => {
  reservationDialog.value = true;
};

// Fonction pour récupérer les photos
async function fetchPhotos() {
  const token = process.client ? localStorage.getItem('token') : null;
  if (token) {
    try {
      const response = await axios.get(`http://localhost:8080/api/atelier/photos/${ateliers.value.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      photos.value = response.data;
      console.log(photos)
    } catch (error) {
      console.error('Erreur lors de la récupération des photos:', error);
    }
  }
}



</script>

<style scoped>
.bouncing-marker {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-30px);
  }
  60% {
    transform: translateY(-15px);
  }
}

.info-text {
  display: flex;
  align-items: center;
  font-size: 1rem;
}

#map {
  height: 500px;
  width: 100%;
}
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f4f4;
}

/* Bouton principal pour déclencher le formulaire de paiement */
.pay-button {
 width: 250px;
 height: 50px;
  background-color: #0095ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

.pay-button:hover {
  background-color: #007acc;
}

/* Styles pour la v-card */
.payment-card {
  background-color: white;
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  padding: 20px;
  max-width: 900px;
  width: 100%;
  margin-top: 50px;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

h3 {
  margin-bottom: 15px;
  font-size: 22px;
  color: #333;
}

.amount-input {
  padding: 10px;
  font-size: 16px;
  width: 100%;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

/* Boutons dans la v-card */
.proceed-button {
  padding: 12px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 10px;
}

.proceed-button:hover {
  background-color: #218838;
}

.cancel-button {
  padding: 12px 20px;
  background-color: #ff3860;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.cancel-button:hover {
  background-color: #e01e37;
}
</style>
