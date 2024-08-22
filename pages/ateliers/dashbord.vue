<template>
  <v-app>
    <!-- Barre d'Outils -->
    <v-app-bar app color="primary" dark v-if="userData">
    
      <span class="ml-2">{{ userData.name }}</span>
      <span class="ml-2">{{ userData.email }}</span>
      
      <v-spacer></v-spacer>
     
      <v-btn text  @click="$router.push('/acceuil')">Accueil</v-btn>
      <v-btn text @click="goToProfile">Profil</v-btn>
      
      <v-btn text @click="showLogoutDialog">Déconnexion</v-btn>
      <!-- <v-btn icon @click="goToMessages">
        <v-icon>mdi-email</v-icon>
      </v-btn> -->
    

    <v-dialog v-model="dialog" max-width="800px" width="100%" height="400px">
  <v-card>
    <v-card-title min-width="800px"  >{{ selectedNotification?.message }}</v-card-title>
    <v-card-subtitle>{{ formatDate(selectedNotification?.created_at) }}</v-card-subtitle>
    <v-card-text>
      <p>Détails de la notification ici...</p>
      <p>{{ selectedNotification?.workshop_messages }}</p>
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
      <v-card min-width="350">
        <v-card-title class="headline">Déconnexion</v-card-title>
        <v-card-text>Voulez-vous vraiment vous déconnecter ?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="logout">Oui</v-btn>
          <v-btn color="primary" text @click="hideLogoutDialog">Annuler</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Contenu Principal -->
    <v-main class="dashboard-content">
      <!-- Texte de Bienvenue -->
      <div class="welcome-text">
        <h1>Bienvenue sur votre interface d'accueil</h1>
        <p>Vous pouvez ici gérer vos actions telles que vos rendez-vous, services, paramètres, et plus encore.</p>
      </div>

      <!-- Cartes d'Actions -->
      <v-container fluid>
        <v-row justify="center" align="center">
          <!-- Carte Vos Rendez-vous -->
          <v-col cols="12" md="3">
            <v-card @click="goToAppointments" class="clickable-card" color="blue lighten-4">
              <v-card-title>
                <v-icon x-large color="primary">mdi-calendar</v-icon>
              </v-card-title>
              <v-card-subtitle>Vos Rendez-vous</v-card-subtitle>
            </v-card>
          </v-col>

          <!-- Carte Vos Services -->
          <v-col cols="12" md="3">
            <v-card @click="goToServices" class="clickable-card" color="green lighten-4">
              <v-card-title>
                <v-icon x-large color="primary">mdi-wrench</v-icon>
              </v-card-title>
              <v-card-subtitle>Vos Services</v-card-subtitle>
            </v-card>
          </v-col>

          <!-- Carte Vos Paramètres -->
          <v-col cols="12" md="3">
            <v-card @click="goToSettings" class="clickable-card" color="red lighten-4">
              <v-card-title>
                <v-icon x-large color="primary">mdi-cog</v-icon>
              </v-card-title>
              <v-card-subtitle>Vos Paramètres</v-card-subtitle>
            </v-card>
          </v-col>

          <!-- Carte Votre Profil -->
          <v-col cols="12" md="3">
            <v-card @click="goToProfile" class="clickable-card" color="purple lighten-4">
              <v-card-title>
                <v-icon x-large color="primary">mdi-account</v-icon>
              </v-card-title>
              <v-card-subtitle>Votre Profil</v-card-subtitle>
            </v-card>
          </v-col>

          <!-- Carte Vos Statistiques -->
        
          <v-col cols="12" md="3">
            <v-card @click="goToAcceuil" class="clickable-card" color="white lighten-1">
              <v-card-title>
                <v-icon x-large color="primary">mdi-home</v-icon>
              </v-card-title>
              <v-card-subtitle>Acceuil</v-card-subtitle>
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

const router = useRouter()

const logoutDialog = ref(false)

function goToProfile() {
  router.push('/ateliers/profil')
}

function goToMessages() {
  router.push('/ateliers/messages')
}

function goToNotifications() {
  router.push('/ateliers/notifications')
}

function showLogoutDialog() {
  logoutDialog.value = true
}

function hideLogoutDialog() {
  logoutDialog.value = false
}

function logout() {
  // Logique pour la déconnexion
  router.push('/acceuil')
  hideLogoutDialog()
}

function goToAppointments() {
  router.push('/ateliers/rendezvous')
}

function goToServices() {
  router.push('/ateliers/services')
}

function goToSettings() {
  router.push('/ateliers/paramettres')
}

function goToStats() {
  router.push('/ateliers/stats')
}
function goToAcceuil() {
  router.push('/acceuil')
}
const userData = ref(null); 

const fetchUserData = async () => {
  // Vérifiez si vous êtes dans le client
  const token = process.client ? localStorage.getItem('token') : null; 
  if (token) {
    try {
      // Appel de l'API pour récupérer les données de l'utilisateur
      const response = await axios.get('http://localhost:8080/api/atelier', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      userData.value = response.data; // Stocker les données de l'utilisateur
      console.log(userData)
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

const notifications = ref([]);
const unviewedCount = ref(0);
const dialog = ref(false);
const selectedNotification = ref(null);
const workshopId = 47; // Remplace par l'ID de l'atelier

// Récupère les notifications
const fetchNotifications = async () => {
  try {
    const response = await axios.get(`http://localhost:8080/api/notifications/${workshopId}`);
    
    notifications.value = response.data;
    
    unviewedCount.value = notifications.value.length; // Compte les notifications non consultées
  } catch (error) {
    console.error('Erreur lors de la récupération des notifications:', error);
  }
};

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
  font-size: 40px;
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
</style>
