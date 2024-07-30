<template>
  <v-app>
    <!-- Barre d'Outils -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Mon Application</v-toolbar-title>
      <v-avatar>
        <img :src="user.profilePicture" alt="Photo de profil" />
      </v-avatar>
      <span class="ml-2">{{ user.name }}</span>
      <span class="ml-2">{{ user.email }}</span>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Accueil</v-btn>
      <v-btn text @click="$router.push('/users/profil')">Profil</v-btn>
      <v-btn text @click="showLogoutDialog">Déconnexion</v-btn>
      <v-btn icon @click="showMessages">
        <v-icon>mdi-email</v-icon>
      </v-btn>
      <v-btn icon @click="showNotifications">
        <v-icon>mdi-bell</v-icon>
      </v-btn>
    </v-app-bar>

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
        <!-- Barre de Recherche -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-tabs v-model="tab" background-color="primary" dark>
                <v-tab>Recherche par Localisation</v-tab>
                <v-tab>Recherche par Services</v-tab>
              </v-tabs>
              <v-tabs-items v-model="tab">
                <!-- Recherche par Localisation -->
                <v-tab-item>
                  <v-text-field
                    v-model="locationQuery"
                    label="Entrez une adresse ou utilisez votre localisation actuelle"
                    prepend-icon="mdi-map-marker"
                    @input="searchByLocation"
                  />
                  <v-btn @click="useCurrentLocation" class="mb-4" color="primary">Utiliser ma localisation actuelle</v-btn>
                </v-tab-item>

                <!-- Recherche par Services -->
                <v-tab-item>
                  <v-select
                    v-model="selectedServices"
                    :items="serviceOptions"
                    label="Sélectionnez les services souhaités"
                    multiple
                    @change="searchByServices"
                  />
                </v-tab-item>
              </v-tabs-items>
            </v-card>
          </v-col>
        </v-row>

        <!-- Carte Interactive et Liste des Ateliers -->
        <v-row>
          <!-- Carte Interactive -->
          <v-col cols="12" md="6">
            <v-card class="pa-4" outlined>
              <v-card-title>Carte des Ateliers</v-card-title>
              <v-card-text>
                <div id="map" style="height: 400px; width: 100%;">
                  <iframe :src="mapUrl" width="100%" height="400" frameborder="0" style="border:0" allowfullscreen></iframe>
                </div>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Liste des Ateliers -->
          <v-col cols="12" md="6">
            <v-card class="pa-4" outlined>
              <v-card-title>Liste des Ateliers</v-card-title>
              <v-list>
                <v-list-item-group v-if="ateliers.length > 0">
                  <v-list-item
                    v-for="atelier in ateliers"
                    :key="atelier.id"
                    @click="viewAtelierDetails(atelier.id)"
                  >
                    <v-list-item-content>
                      <v-list-item-title>{{ atelier.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ atelier.address }}</v-list-item-subtitle>
                      <v-list-item-subtitle>{{ atelier.phone }}</v-list-item-subtitle>
                      <v-list-item-subtitle>{{ atelier.services.join(', ') }}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-btn @click.stop="viewAtelierDetails(atelier.id)">Voir plus</v-btn>
                    </v-list-item-action>
                  </v-list-item>
                </v-list-item-group>
                <v-list-item v-else>
                  <v-list-item-content>
                    <v-list-item-title>Aucun atelier trouvé.</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios' // Assurez-vous d'avoir installé axios

// Variables réactives
const tab = ref(0)
const locationQuery = ref('')
const selectedServices = ref([])
const serviceOptions = ref(['Service 1', 'Service 2', 'Service 3']) // Remplacez par les services réels
const ateliers = ref([])
const mapUrl = ref('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3151.835434509716!2d144.95373531544786!3d-37.817209742021115!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6ad642af0f11fd81%3A0xf5772e05c3d5cdb8!2sFederation+Square!5e0!3m2!1sen!2sau!4v1515565516795')

// User info
const user = ref({
  name: '',
  email: '',
  phone: '',
  role: '',
  profilePicture: 'url_de_la_photo_de_profil', // Remplacez par l'URL par défaut
});

// Dialogs
const logoutDialog = ref(false)
const messagesDialog = ref(false)
const notificationsDialog = ref(false)
const messages = ref([])
const notifications = ref([])
const newMessage = ref('')

// Récupérer les données de l'utilisateur
onMounted(async () => {
  try {
    const token = localStorage.getItem('token'); // Assurez-vous de récupérer le token stocké lors de la connexion
    const response = await axios.get('/api/user', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    user.value = response.data // Assurez-vous que les données sont au bon format
  } catch (error) {
    console.error('Erreur lors de la récupération des données utilisateur:', error)
  }
})

// Fonctions
function searchByLocation() {
  // Logique de recherche par localisation
}

function searchByServices() {
  // Logique de recherche par services
}

function useCurrentLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      locationQuery.value = `${position.coords.latitude}, ${position.coords.longitude}`
      searchByLocation()
    }, () => {
      alert('Impossible d\'obtenir votre position.')
    });
  } else {
    alert('La géolocalisation n\'est pas supportée par ce navigateur.')
  }
}

function viewAtelierDetails(id) {
  // Logique pour afficher les détails de l'atelier
}

function showLogoutDialog() {
  logoutDialog.value = true
}

function hideLogoutDialog() {
  logoutDialog.value = false
}

function logout() {
  // Logique de déconnexion
}

function showMessages() {
  messagesDialog.value = true
}

function hideMessagesDialog() {
  messagesDialog.value = false
}

function sendMessage() {
  if (newMessage.value) {
    messages.value.push(newMessage.value)
    newMessage.value = ''
  }
}

function showNotifications() {
  notificationsDialog.value = true
}

function hideNotificationsDialog() {
  notificationsDialog.value = false
}
</script>

<style scoped>
/* Ajoutez vos styles ici */
</style>
