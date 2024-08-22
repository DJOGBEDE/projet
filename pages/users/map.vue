<template>
  <v-app>
    <!-- Barre d'Outils -->
    <v-app-bar app color="primary" dark v-if="userData">
  <v-avatar class="ml-4 square-avatar custom-avata">
    <img :src="`../upload/user_${userData.id}_profile.jpg`" alt="Photo de profil" />

  </v-avatar>


      <span class="ml-2">{{ userData.name }}</span>
      <span class="ml-2">{{ userData.email }}</span>
     
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Accueil</v-btn>
      <v-btn text @click="$router.push('/users/profil')">Profil</v-btn>
      <v-btn text @click="showLogoutDialog">Déconnexion</v-btn>
      <!-- <v-btn icon @click="showMessages">
        <v-icon>mdi-email</v-icon>
      </v-btn> -->
   
  
        <v-btn icon @click="dialog = true" >
          <v-icon>mdi-bell</v-icon>
          <div v-if="unviewedCount > 0" class="notification-dot"></div>
        </v-btn>
      
       <!-- Dialogue pour afficher les notifications -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Notifications</span>
        </v-card-title>
        <v-card-text>
          <p>Nombre de notifications non consultées : {{ unviewedCount }}</p>
          <ul v-if="notifications.length > 0" class="notifications-list">
            <li 
              v-for="notification in notifications" 
              :key="notification.id" 
              class="notification-item"
              @click="toggleNotification(notification.id)"
            >
              <div class="notification-summary">
                <strong>Message:</strong> {{ notification.message }}<br />
                <strong>Type:</strong> {{ notification.type }}<br />
                <strong>Date:</strong> {{ new Date(notification.date).toLocaleString() }}<br />
                <strong>Vient de:</strong> {{ notification.workshopName }}
              </div>
              <div v-if="notification.showDetails" class="notification-details">
                <p>Contenu complet de la notification...</p>
              </div>
            </li>
          </ul>
          <p v-else>Aucune notification disponible.</p>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="dialog = false">Fermer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  
     
    </v-app-bar>
    <v-card-text v-else>
        <p>Aucune donnée disponible.</p>
    </v-card-text>

    <!-- Dialog de Déconnexion -->
    <v-dialog v-model="logoutDialog" max-width="350">
      <v-card>
        <v-card-title class="headline">Déconnexion</v-card-title>
        <v-card-text>Voulez-vous vraiment vous déconnecter ?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="logout">Oui</v-btn>
          <v-btn color="primary" text @click="hideLogoutDialog">Annuler</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Interface de Messages -->
    <v-dialog v-model="messagesDialog" max-width="600">
      <v-card>
        <v-card-title class="headline">Messages</v-card-title>
        <v-card-text>
          <div>
            <v-text-field label="Écrire un message" v-model="newMessage"></v-text-field>
            <v-btn color="primary" @click="sendMessage">Envoyer</v-btn>
            <v-list>
              <v-list-item v-for="(message, index) in messages" :key="index">
                <v-list-item-content>{{ message }}</v-list-item-content>
              </v-list-item>
            </v-list>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" text @click="hideMessagesDialog">Fermer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Interface de Notifications -->
    <v-dialog v-model="notificationsDialog" max-width="400">
      <v-card>
        <v-card-title class="headline">Notifications</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item v-for="(notification, index) in notifications" :key="index">
              <v-list-item-content>{{ notification }}</v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" text @click="hideNotificationsDialog">Fermer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-main>
      <v-container fluid>
        <v-row class="mb-4">
  <v-col cols="12">
    <v-card class="pa-4" outlined>
      <v-tabs v-model="tab" background-color="primary" dark>
        <v-tab>
          <v-icon left>mdi-map-marker</v-icon>
          Recherche par Localisation
        </v-tab>

        <v-tab>
          <v-icon left>mdi-wrench</v-icon>
          Recherche par Services
        </v-tab>
      </v-tabs>

      <!-- Recherche par Localisation -->
      <v-tab-item v-if="tab === 0">
        <v-text-field
         v-model="location"
          label="Entrez une adresse ou utilisez votre localisation actuelle"
          prepend-icon="mdi-map-marker"
         
          class="mt-6"
        />
        <div v-if="loading">Chargement des données...</div>
        <div v-if="error" class="error">{{ error }}</div>
        <v-btn  @click="fetchLocationData" class="ml-10 mb-10" color="primary">
          Rechercher...
        </v-btn>
        <v-btn  @click="getLocation" class="ml-1 mb-10" color="primary">
          Utiliser ma localisation
        </v-btn>
        <div class="mb-4">
     
      <v-btn class="ml-9" color="green" @click="setDistanceRange(0, 5)">0-5 km</v-btn>
      <v-btn class="ml-2" color="pink" @click="setDistanceRange(0, 10)">0-10 km</v-btn>
      <v-btn class="ml-2" color="red" @click="setDistanceRange(4, null)">10 km et plus</v-btn>
    </div>

        <!-- Carte Interactive et Liste des Ateliers -->
        <v-row>
          <!-- Carte Interactive -->
          <v-col cols="12" md="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Carte des Ateliers</v-card-title>
              <v-card-text>
               <div id="map" style="width: 100%; height: 500px;"></div>

              </v-card-text>
            </v-card>
          </v-col>
          

          <v-col cols="12" md="12">
      <v-card class="pa-4" outlined>
        <v-card-title>Liste des Ateliers</v-card-title>
        <v-container>
          <v-row>
            <v-col v-for="atelier in paginatedAteliersL" :key="atelier.id" cols="12" sm="6" md="4">
              <v-card @click="goToAtelier(atelier.id)" width="350px" class="d-flex flex-column ml-14">
                <v-img 
                :src="`/46371688-factory-vector-icon-style-is-bicolor-flat-symbol-blue-and-gray-colors-rounded-angles-white.jpg`" 
                  alt="Photo de l'atelier" 
                  height="200px" 
                  class="mb-3"
                ></v-img>
                <v-card-title>{{ atelier.name }}</v-card-title>
                <v-card-subtitle>{{ atelier.address }}</v-card-subtitle>
                <v-card-subtitle>{{ atelier.opening_hours }}</v-card-subtitle>
              </v-card>
            </v-col>
                </v-row>
              </v-container>
              <v-pagination
                v-model="currentPage"
                :length="pageCount"
                total-visible="5"
                @input="updatePage"
              ></v-pagination>
            </v-card>
          </v-col>
        </v-row>

        <!-- V-Card pour afficher les services sélectionnés -->
        <v-row>
          <v-col cols="12">
            <v-card class="mt-4" v-if="selectedServices.length > 0">
              <v-card-title>Services Sélectionnés</v-card-title>
              <v-card-text>
                <div v-for="(service, index) in selectedServices" :key="index">
                  {{ service }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-tab-item>

       <!-- Recherche par Services -->
    <v-tab-item v-if="tab === 1">
      <v-text-field
        v-model="search"
        density="comfortable"
        placeholder="Rechercher un service"
        prepend-inner-icon="mdi-magnify"
        style="max-width: 900px;"
        variant="solo"
        clearable
        hide-details
        class="mb-4 ml-4"
      />
      <!-- Liste des Ateliers pour Recherche par Services -->
      <v-card class="pa-4" outlined>
        <v-card-title>Liste des Ateliers</v-card-title>
        <v-container>
          <v-row>
            <v-col v-for="service in paginatedFilteredServices" :key="service.id" cols="12" sm="6" md="6">
              <v-card @click="goToAtelier(service.workshop_id)" class="mb-4" outlined>
                <v-img 
                :src="`/46371688-factory-vector-icon-style-is-bicolor-flat-symbol-blue-and-gray-colors-rounded-angles-white.jpg`" 
                  alt="Photo de l'atelier" 
                  height="200px" 
                  class="mb-3"
                ></v-img>
                <v-card-title>{{ service.name }}</v-card-title>
                <v-card-subtitle>{{ service.description }}</v-card-subtitle>
                <v-card-text>
                  <div v-if="getAtelierById(service.workshop_id)">
                    
                    <v-list dense>
                      <!-- Afficher les détails de l'atelier ici -->
                      <!-- Vous pouvez ajouter plus de détails sur l'atelier ici -->
                    </v-list>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <v-pagination
            v-model="currentPage"
            :length="pageCountS"
            class="mt-4"
            color="primary"
          ></v-pagination>
        </v-container>
      </v-card>
    </v-tab-item>
    </v-card>
  </v-col>
</v-row>

      </v-container>
      
  
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const tab = ref(0);
const locationQuery = ref('');
const search = ref('');
const selectedServices = ref([]);
const workshopName = ref('');

const services = ref([]);

// Variables pour la gestion de la déconnexion et des messages
const logoutDialog = ref(false);
const messagesDialog = ref(false);
const notificationsDialog = ref(false);
const messages = ref([]);
const newMessage = ref([]);
const notifications = ref([]);
//Variables pour stocker la latitude et la longitude
let latitude = ref(null);
let longitude = ref(null);

// Fonction pour récupérer les notifications
const fetchNotifications = async () => {
  try {
    const response = await axios.get(`http://localhost:8080/api/notifications/${workshopId}`);
    const data = response.data;
    
    // Associer les notifications avec le nom de l'atelier récupéré et trier par date
    notifications.value = data.map(notification => ({
      id: notification[0],
      message: notification[1],
      type: notification[2],
      date: notification[3], // Assurez-vous que la date est bien dans la 4e colonne
      workshopName: workshopName.value, // Utilise le nom de l'atelier récupéré
      showDetails: false // Par défaut, les détails sont masqués
    })).sort((a, b) => new Date(b.date) - new Date(a.date)); // Tri décroissant par date
    
    unviewedCount.value = notifications.value.length; // Compte les notifications non consultées
  } catch (error) {
    console.error('Erreur lors de la récupération des notifications:', error);
  }
};

// Utilisation de router
const router = useRouter();

// Récupération des ateliers
const ateliers = ref([]);


const fetchServices = async () => {
  try {
    const response = await axios.get('http://localhost:8080/api/services');
    services.value = response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des services:', error);
  }
};

const filteredServices = computed(() => {
  if (search.value) {
    return services.value.filter(service =>
      service.name.toLowerCase().includes(search.value.toLowerCase()) ||
      service.description.toLowerCase().includes(search.value.toLowerCase())
    );
  } else {
    return services.value;
  }
});

const paginatedFilteredServices = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredServices.value.slice(start, end);
});

const pageCountS = computed(() => Math.ceil(filteredServices.value.length / itemsPerPage.value));

// Récupérer les détails de l'atelier par ID
const getAtelierById = (id) => {
  return ateliers.value.find(atelier => atelier.id === id);
};

// Rediriger vers la page de l'atelier
const goToAtelier = (id) => {
  router.push(`/users/${id}`);
};



onMounted(() => {
  fetchServices(); // Appel initial pour récupérer les services lors du chargement du composant
});


/// Récupérer les services et les ateliers lorsque le composant est monté
onMounted(async () => {
  try {
    const responseServices = await axios.get('http://localhost:8080/api/services'); // Remplacer par votre API
    services.value = responseServices.data;
    console.log(services)
    
    const responseAteliers = await axios.get('http://localhost:8080/api/ateliers'); // Remplacer par votre API
    ateliers.value = responseAteliers.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des services ou des ateliers:', error);
  }
});

// Fonction pour filtrer les services en fonction de la recherche
const filterServices = () => {
  return services.value.filter(service =>
    service.name.toLowerCase().includes(search.value.toLowerCase()) ||
    service.description.toLowerCase().includes(search.value.toLowerCase())
  );
};

// Utiliser une propriété calculée pour obtenir les services filtrés

// Obtenir les ateliers filtrés par recherche
const filteredAteliers = computed(() => {
  const searchLower = search.value.toLowerCase();
  return ateliers.value.filter(atelier => {
    return atelier.name.toLowerCase().includes(searchLower);
  });
});

const paginatedAteliers = computed(() => {
  if (!filteredServices.value) {
    return [];
  }
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredServices.value.slice(start, end);
});

// Référence pour stocker les données de l'utilisateur
const userData = ref(null); 

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

// Récupérer les données de l'utilisateur lorsque le composant est monté
onMounted(() => {
  fetchUserData();
});
// Fonction pour afficher le dialog de déconnexion
const showLogoutDialog = () => {
  logoutDialog.value = true;
};

// Fonction pour cacher le dialog de déconnexion
const hideLogoutDialog = () => {
  logoutDialog.value = false;
};

// Fonction de déconnexion
const logout = () => {
  // Logique de déconnexion
  router.push('/login');
};

// Fonction pour afficher les messages
const showMessages = () => {
  messagesDialog.value = true;
};

// Fonction pour cacher le dialog des messages
const hideMessagesDialog = () => {
  messagesDialog.value = false;
};

// Fonction pour envoyer un message
const sendMessage = () => {
  if (newMessage.value) {
    messages.value.push(newMessage.value);
    newMessage.value = '';
  }
};

// Fonction pour afficher les notifications
const showNotifications = () => {
  notificationsDialog.value = true;
};

// Fonction pour cacher le dialog des notifications
const hideNotificationsDialog = () => {
  notificationsDialog.value = false;
};


// Pagination des services filtrés
const paginatedServices = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredServices.value.slice(start, end);
});

const unviewedCount = ref(0);
const dialog = ref(false);
const selectedNotification = ref(null);
const workshopId = 47; // Remplace par l'ID de l'atelier

// Marquer les notifications comme consultées
const markAsViewed = async () => {
  if (unviewedCount.value > 0) {
    try {
      await axios.post(`http://localhost:8080/api/notifications/viewed/${workshopId}`);
      notifications.value = []; // Vider les notifications après consultation
      unviewedCount.value = 0; // Réinitialiser le compteur
    } catch (error) {
      console.error('Erreur lors de la mise à jour des notifications:', error);
    }
  }
};

// Ouvre le dialogue avec les détails de la notification
const openDialog = (notification) => {
  selectedNotification.value = notification;
  dialog.value = true;
};

// Formater la date
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString(); // Formate selon vos besoins
};

onMounted(fetchNotifications);

const location = ref('')
const coordinates = ref([])
const map = ref(null)
const loading = ref(false)
const error = ref(null)
const nearestLocations = ref([])
const distanceRange = ref({ min: 0, max: 5 })
const distanceRangeLabel = ref('0-5 km')
const currentPage = ref(1)
const itemsPerPage = ref(6)

const { data: localisationsData, error: localisationsError } = useFetch('http://localhost:8080/localisations')
const { data: workshopsData, error: workshopsError } = useFetch('http://localhost:8080/workshops')

const paginatedAteliersL = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return nearestLocations.value.slice(start, end)
})

const pageCount = computed(() => Math.ceil(nearestLocations.value.length / itemsPerPage.value))

const initMap = async (L) => {
  if (!map.value) {
    map.value = L.map('map').setView([51.505, -0.09], 2)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap',
    }).addTo(map.value)
  }
}

const updateMap = async (lat, lon) => {
  const L = (await import('leaflet')).default
  if (!map.value) await initMap(L)

  L.marker([lat, lon]).addTo(map.value)
    .bindPopup('Localité: ' + location.value)
    .openPopup()

  L.circle([lat, lon], {
    color: 'blue',
    radius: distanceRange.value.max * 1000 || 15000,
    fillOpacity: 0.5
  }).addTo(map.value)

  map.value.setView([lat, lon], 13)
}

const haversine = (lat1, lon1, lat2, lon2) => {
  const R = 6371 // Rayon de la Terre en kilomètres

  lat1 = lat1 * Math.PI / 180
  lon1 = lon1 * Math.PI / 180
  lat2 = lat2 * Math.PI / 180
  lon2 = lon2 * Math.PI / 180

  const dlat = lat2 - lat1
  const dlon = lon2 - lon1

  const a = Math.sin(dlat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlon / 2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

const findNearestLocations = (lat, lon, locations) => {
  const ids = locations
    .map(loc => {
      const distance = haversine(lat, lon, loc.lat, loc.lon)
      return { ...loc, distance }
    })
    .filter(loc => 
      (loc.distance >= distanceRange.value.min && (distanceRange.value.max === null || loc.distance < distanceRange.value.max))
    )
    .sort((a, b) => a.distance - b.distance)
    .map(loc => loc.id) // Récupère uniquement les IDs

  if (ids.length > 0) {
    fetchWorkshopDetails(ids)
  } else {
    nearestLocations.value = []
  }
}

const fetchLocationData = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${location.value}`)
    if (!response.ok) {
      throw new Error('Erreur de réseau')
    }

    const data = await response.json()
    console.log(data)

    if (data && data.length > 0) {
      const { lat, lon } = data[0]
      coordinates.value.push({ lat, lon })
      await updateMap(lat, lon)
      await fetchLocalisations(lat, lon)
    } else {
      error.value = 'Aucune donnée trouvée pour cette localité.'
    }
  } catch (err) {
    error.value = 'Erreur lors de la récupération des données : ' + err.message
  } finally {
    loading.value = false
  }
}

const fetchLocalisations = async (lat, lon) => {
  try {
    const localisations = localisationsData.value
    findNearestLocations(lat, lon, localisations)
  } catch (err) {
    error.value = 'Erreur lors de la récupération des localisations : ' + err.message
  }
}

const fetchWorkshopDetails = async (ids) => {
  loading.value = true
  error.value = null

  try {
    const response = await fetch(`http://localhost:8080/workshops?ids=${ids.join(',')}`)
    if (!response.ok) {
      throw new Error('Erreur de réseau avec l\'API des ateliers')
    }

    const workshops = await response.json()
    nearestLocations.value = workshops
  } catch (err) {
    error.value = 'Erreur lors de la récupération des ateliers : ' + err.message
  } finally {
    loading.value = false
  }
}

const setDistanceRange = (min, max) => {
  distanceRange.value = { min, max }
  distanceRangeLabel.value = max ? `${min}-${max} km` : `${min} km et plus`

  if (coordinates.value.length > 0) {
    const { lat, lon } = coordinates.value[coordinates.value.length - 1]
    fetchLocalisations(lat, lon)
    updateMap(lat, lon)
  }
}


const updatePage = (page) => {
  currentPage.value = page
}

// Initialisation de la carte lorsque le composant est monté
onMounted(async () => {
  const L = (await import('leaflet')).default
  initMap(L)
})

const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords
        // Appeler la fonction qui utilise latitude et longitude
        fetchLocalisations(latitude, longitude)
        updateMap(latitude, longitude)
      },
      (error) => {
        console.error('Erreur de localisation:', error)
      }
    )
  } else {
    alert('La géolocalisation n\'est pas supportée par ce navigateur.')
  }
}

const handleLocation = (lat, lon) => {
  // Ici vous pouvez faire ce que vous voulez avec la latitude et la longitude
  console.log(`Latitude: ${lat}, Longitude: ${lon}`)
  // Par exemple, vous pouvez émettre un événement ou appeler une API
}

// Fonction pour récupérer le nom de l'atelier
const fetchWorkshopName = async () => {
  try {
    const response = await axios.get(`http://localhost:8080/workshop/${workshopId}`);
    const data = response.data;
    workshopName.value = data.name;
  } catch (error) {
    console.error('Erreur lors de la récupération du nom de l\'atelier:', error);
  }
};



// Fonction pour basculer l'affichage des détails de la notification
const toggleNotification = (id) => {
  const notification = notifications.value.find(n => n.id === id);
  if (notification) {
    notification.showDetails = !notification.showDetails;
  }
};

// Fonction appelée lors du montage du composant
onMounted(async () => {
  await fetchWorkshopName(); // Récupère d'abord le nom de l'atelier
  await fetchNotifications(); // Ensuite, récupère les notifications
});

</script>

<style scoped>
/* Styles personnalisés pour le tableau de bord */
.dashboard-content {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.welcome-text {
  margin-bottom: 30px;
  font-size: 22px;
  color: #424242;
}

.clickable-card {
  cursor: pointer;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 15px;
  padding: 20px;
}

.clickable-card:hover {
  transform: scale(1.1);
  box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.2);
}

.v-card-title {
  display: flex;
  justify-content: center;
  font-size: 30px;
}

.v-card-subtitle {
  text-align: center;
  font-size: 20px;
  font-weight: 700;
  color: #424242;
}

.notification-icon {
  position: relative;
}

.notification-dot {
  position: absolute;
  top: 0; /* Ajustez pour positionner le point légèrement sur l'icône */
  right: -5px; /* Ajustez pour positionner le point à droite de l'icône */
  width: 12px; /* Taille du point */
  height: 12px; /* Taille du point */
  background-color: red; /* Couleur du point */
  border-radius: 50%; /* Pour un point circulaire */
}

.square-avatar {
  width: 100px; /* Vous pouvez ajuster la largeur */
  height: 100px; /* Vous pouvez ajuster la hauteur */
  border-radius: 0; /* Supprimez le bord arrondi pour obtenir une forme carrée */
}
.square-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ajuste l'image pour couvrir entièrement le conteneur */
}
.notifications-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.notifications-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notification-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  border-left: 4px solid #007bff;
  overflow: hidden;
}

.notification-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.notification-summary {
  font-size: 16px;
  color: #333;
}

.notification-details {
  margin-top: 10px;
  font-size: 14px;
  color: #555;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
