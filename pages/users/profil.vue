<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Tableau de bord</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Accueil</v-btn>
      <v-btn text @click="$router.push('/users/dashbord')">Tableau de bord</v-btn>
      <!-- <v-btn icon @click="$router.push('/users/messages')">
        <v-icon>mdi-email</v-icon>
      </v-btn> -->
      <v-btn icon @click="$router.push('/users/notifications')">
        <v-icon>mdi-bell</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <!-- Informations Personnelles -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Informations Personnelles</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="updateProfile">
                  <v-text-field v-model="profile.name" label="Nom" required />
                  <v-text-field v-model="profile.email" label="Email" type="email" required />
                  <v-text-field v-model="profile.phone" label="Numéro de Téléphone" />
                  <v-btn type="submit" color="primary">Mettre à jour</v-btn>
                </v-form>
              </v-card-text>

             
            </v-card>

            <v-container class="ml-10 mt-4 mb-4">
    <v-img v-if="profilePictureUrl" :src="profilePictureUrl" class="profile-picture" />
    <v-btn @click="fetchProfilePicture">Charger la photo de profil</v-btn>
  </v-container>
            <v-card class="pa-4" outlined>
    <v-card-title>Changer la photo de profil</v-card-title>
    <v-card-text>
      <!-- Afficher la photo de profil actuelle -->
      <v-img 
        :src="currentProfilePicture"
        alt="Photo de profil actuelle"
        max-height="150"
        max-width="150"
        class="mb-4"
      />
      
      <!-- Prévisualisation de la nouvelle photo de profil -->
      <v-img 
        v-if="profilePicturePreview"
        :src="profilePicturePreview"
        alt="Prévisualisation de la nouvelle photo"
        max-height="150"
        max-width="150"
        class="mb-4"
      />

      <v-form @submit.prevent="uploadProfilePicture">
        <v-file-input 
          v-model="profilePicture"
          label="Télécharger une nouvelle photo de profil"
          accept="image/*"
          prepend-icon="mdi-camera"
          @change="previewProfilePicture"
          required
        />
        <v-btn type="submit" color="primary">Mettre à jour la photo</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
          </v-col>
        </v-row>

        <!-- Historique des Rendez-vous -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Historique des Rendez-vous</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item-group v-if="resultats">
                    <v-list-item v-for="resultat in resultats" :key="resultat.id">
                      <v-list-item-content>
                        <v-list-item-title>
                          {{ resultat.date }} à {{ resultat.time }}
                        </v-list-item-title>
                        <v-list-item-subtitle>
                          {{ resultat.details }}
                        </v-list-item-subtitle>
                        <v-btn small class="mr-4 mt-4" color="info" @click="viewDetails(resultat.id)">
                          Voir détails
                        </v-btn>
                        <v-btn small class="mt-4" color="error" @click="cancelAppointment(resultat.id)">
                          Annuler
                        </v-btn>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                  <v-list-item v-else>
                    <v-list-item-content>
                      <v-list-item-title>Aucun rendez-vous trouvé.</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Préférences -->
        <v-row>
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Préférences</v-card-title>
              <v-card-text>
                <v-form>
                  <v-switch v-model="preferences.notifications" label="Notifications par email" />
                  <v-switch v-model="preferences.messages" label="Messages" />
                  <v-btn @click="updatePreferences" color="primary">Enregistrer les préférences</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <!-- Dialogue pour afficher les détails de la réservation -->
    <v-dialog v-model="detailsDialog" max-width="500px">
      <v-card>
        <v-card-title>Détails du Rendez-vous</v-card-title>
        <v-card-text>
          <p><strong>Date :</strong> {{ selectedAppointment.date }}</p>
          <p><strong>Heure :</strong> {{ selectedAppointment.time }}</p>
          <p><strong>Détails :</strong> {{ selectedAppointment.details }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="detailsDialog = false">Fermer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Données pour le profil de l'utilisateur
const profile = ref({
  name: '',
  email: '',
  phone: ''
});

const userData = ref(null); 

// Données pour les rendez-vous
const appointments = ref([]);
const resultats = ref({});

// Préférences
const preferences = ref({
  notifications: true,
  messages: false
});

// Dialogues et sélection de réservation
const detailsDialog = ref(false);
const selectedAppointment = ref({});

const profilePicture = ref(null);
const profilePicturePreview = ref(null);
const currentProfilePicture = ref('');  // URL de la photo de profil actuelle


const profilePictureUrl = ref('');

// Appel de la fonction pour charger l'image au démarrage



// Fonction pour récupérer la photo de profil actuelle
async function fetchProfilePicture() {
  const token = process.client ? localStorage.getItem('token') : null; 
  try {
    const response = await axios.get(`http://localhost:8080/api/user/${userData.value.id}/profile-picture`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    currentProfilePicture.value = response.data.profilePictureUrl;
  } catch (error) {
    console.error('Erreur lors de la récupération de la photo de profil', error);
  }
}

fetchProfilePicture();


// Fonction pour prévisualiser la nouvelle photo de profil
function previewProfilePicture() {
  const file = profilePicture.value;
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      profilePicturePreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
}


async function uploadProfilePicture() {
  const formData = new FormData();
  formData.append('profile_picture', profilePicture.value);

  const token = localStorage.getItem('token'); // Récupérer le token d'authentification si nécessaire

  try {
    const response = await axios.put(`http://localhost:8080/api/user/${userData.value.id}/profile-picture`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,  // Ajoutez le token si nécessaire
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log('Photo de profil mise à jour', response.data);
  } catch (error) {
    console.error('Erreur lors de la mise à jour de la photo de profil', error);
  }
}

// Fonction pour récupérer les données de l'utilisateur
const fetchUserData = async () => {
  const token = process.client ? localStorage.getItem('token') : null; 
  if (token) {
    try {
      const response = await axios.get('http://localhost:8080/api/user', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      userData.value = response.data; // Stocker les données de l'utilisateur
      
      // Mettez à jour le profil avec les données récupérées
      profile.value.name = response.data.name;
      profile.value.email = response.data.email;
      profile.value.phone = response.data.phone;
      
    } catch (error) {
      console.error('Erreur lors de la récupération des données de l\'utilisateur:', error);
      userData.value = null; 
    }
  }
};



// Fonction pour récupérer les rendez-vous
async function fetchAppointments() {
  if (userData.value) {
    const userId = parseInt(userData.value.id, 10);
    try {
      const response = await axios.get(`http://localhost:8080/api/reservations/${userId}`);
      resultats.value = response.data; // Stockez les résultats dans resultats
      console.log(resultats.value);
    } catch (error) {
      console.error('Erreur lors de la récupération des rendez-vous', error);
    }
  }
}

// Fonction pour mettre à jour le profil
async function updateProfile() {
  try {
    await axios.put(`http://localhost:8080/api/user/${ userData.value.id}`, {
      name: profile.value.name,
      email: profile.value.email,
      phone: profile.value.phone
    });
    console.log('Informations mises à jour', profile.value);
  } catch (error) {
    console.error('Erreur lors de la mise à jour du profil', error);
  }
}

// Fonction pour afficher les détails du rendez-vous
function viewDetails(id) {
  const appointment = resultats.value.find(r => r.id === id);
  if (appointment) {
    selectedAppointment.value = appointment;
    detailsDialog.value = true;
  }
}

// Fonction pour annuler le rendez-vous
async function cancelAppointment(id) {
  try {
    await axios.delete(`http://localhost:8080/api/reservations/${id}`);
    resultats.value = resultats.value.filter(appointment => appointment.id !== id);
    console.log('Rendez-vous annulé', id);
  } catch (error) {
    console.error('Erreur lors de l\'annulation du rendez-vous', error);
  }
}

// Fonction pour mettre à jour les préférences
async function updatePreferences(id) {
  try {
    await axios.put(`http://localhost:8080/api/user/${id}`);
    console.log('Préférences mises à jour', preferences.value);
  } catch (error) {
    console.error('Erreur lors de la mise à jour des préférences', error);
  }
}

// Récupérer les données lors du chargement du composant
onMounted(() => {
  fetchUserData().then(() => {
    fetchAppointments(); // Appel des rendez-vous après que l'utilisateur a été récupéré
  });
});
</script>
