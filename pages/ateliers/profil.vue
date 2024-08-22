<template>
  <v-app>
    <!-- Barre de navigation -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Profil de l'Atelier</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/ateliers/dashbord')">Tableau de bord</v-btn>
      <v-btn text @click="$router.push('/ateliers/services')">Services</v-btn>
      <v-btn text @click="$router.push('/ateliers/rendezvous')">Rendez-vous</v-btn>
     
      <v-btn text @click="$router.push('/ateliers/paramettres')">Paramètres</v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <!-- Informations de Profil -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Informations de Profil</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="updateProfile">
                  <v-text-field v-model="profile.name" label="Nom de l'atelier" required />
                  <v-text-field v-model="profile.address" label="Adresse" required />
                  <v-text-field v-model="profile.phone" label="Numéro de téléphone" required />
                  <v-text-field v-model="profile.email" label="Adresse e-mail" type="email" required />
                  <v-text-field v-model="profile.website" label="Site web" />
                  <v-btn type="submit" color="primary">Mettre à jour</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        
    <!-- Carte pour l'enregistrement de la position -->
    <v-card class="mb-4">
      <v-card-title>Enregistrer votre position</v-card-title>
      <v-card-text>
        <v-btn color="primary" @click="getLocation">Enregistrer la position actuelle</v-btn>
        <p v-if="location">Position enregistrée : {{ location.latitude }}, {{ location.longitude }}</p>
        <v-alert v-if="locationError" type="error" dismissible>{{ locationError }}</v-alert>
      </v-card-text>
    </v-card>

    <!-- Formulaire pour enregistrer/modifier l'heure d'ouverture -->
    <v-card class="mb-4">
      <v-card-title>Enregistrer / Modifier l'heure d'ouverture</v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="openingTime"
                label="Heure d'ouverture"
                type="time"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-btn color="success" :disabled="!valid" @click="saveOpeningTime">
            Enregistrer l'heure
          </v-btn>
          <p v-if="savedOpeningTime">Heure d'ouverture enregistrée : {{ savedOpeningTime }}</p>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Carte pour modifier l'heure d'ouverture -->
    <v-card>
      <v-card-title>Modifier l'heure d'ouverture</v-card-title>
      <v-card-text>
        <v-form ref="modifyForm" v-model="validModify" lazy-validation>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="newOpeningTime"
                label="Nouvelle heure d'ouverture"
                type="time"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-btn color="warning" :disabled="!validModify" @click="modifyOpeningTime">
            Modifier l'heure
          </v-btn>
          <p v-if="modifiedOpeningTime">Nouvelle heure d'ouverture : {{ modifiedOpeningTime }}</p>
        </v-form>
      </v-card-text>
    </v-card>


        <v-row>
          <!-- Formulaire pour ajouter une photo de profil -->
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Gestion des Photos</v-card-title>
              <v-card-text>
                <v-file-input v-model="profilePicture" label="Choisir une photo de profil" accept="image/*" @change="previewImage"></v-file-input>
                <v-btn @click="uploadProfilePicture" color="primary">Ajouter la photo de profil</v-btn>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
    
        <v-row>
          <!-- Afficher les photos -->
          <v-col cols="12" v-for="photo in photos" :key="photo.id">
            <v-img :src="`/uploads/${photo.file_path.split('/').pop()}`" height="200" contain></v-img>
            <v-btn @click="deletePhoto(photo.id)" color="red">Supprimer</v-btn>
          </v-col>
        </v-row>
      </v-container>
      
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useGeolocation } from '@vueuse/core'

// Définition du profil de l'atelier
const profile = ref({
  name: '',
  address: '',
  phone: '',
  email: '',
  website: '',
  heures: '',
});

// Variables pour les fichiers photo
const photos = ref([]);
const profilePicture = ref(null);

const userData = ref(null); 

const fetchUserData1 = async () => {
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
  fetchUserData1();
})

// Fonction pour récupérer les données de l'utilisateur
async function fetchUserData() {
  const token = process.client ? localStorage.getItem('token') : null;
  if (token) {
    try {
      const response = await axios.get('http://localhost:8080/api/atelier', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      // Mise à jour des informations de profil
      Object.assign(profile.value, {
        name: response.data.name,
        email: response.data.email,
        phone: response.data.phone_number,
        address: response.data.adresse,
        website: response.data.website,
        heures: response.data.opening_hours
      });

      // Récupérer les photos de profil
      fetchPhotos();
    } catch (error) {
      console.error('Erreur lors de la récupération des données de l\'utilisateur:', error);
    }
  }
}

// Fonction pour mettre à jour le profil
async function updateProfile() {
  try {
    const token = process.client ? localStorage.getItem('token') : null;
    const userId = await axios.get('http://localhost:8080/api/atelier', {
      headers: { Authorization: `Bearer ${token}` }
    });

    await axios.put(`http://localhost:8080/api/atelier/${userId.data.id}`, profile.value);
    console.log('Informations mises à jour', profile.value);
  } catch (error) {
    console.error('Erreur lors de la mise à jour du profil', error);
  }
}

// Fonction pour récupérer les photos
async function fetchPhotos() {
  const token = process.client ? localStorage.getItem('token') : null;
  if (token) {
    try {
      const response = await axios.get(`http://localhost:8080/api/atelier/photos/${userData.value.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      photos.value = response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des photos:', error);
    }
  }
}

const uploadProfilePicture = async () => {
    if (!profilePicture.value) return;
  
    const formData = new FormData();
    formData.append('profile_picture', profilePicture.value);
    formData.append('workshop_id', userData.value.id); // Inclure l'ID de l'atelier dans la requête
  
    try {
      await axios.post('http://localhost:8080/api/atelier/profile-picture', formData);
      fetchPhotos(); // Met à jour la liste des photos après l'ajout
    } catch (error) {
      console.error('Erreur lors de l\'ajout de la photo:', error);
    }
  };

// Fonction pour supprimer une photo
async function deletePhoto(photoId) {
  try {
    const token = process.client ? localStorage.getItem('token') : null;
    const userId = await axios.get('http://localhost:8080/api/atelier', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    await axios.delete(`http://localhost:8080/api/atelier/photos/${photoId}/${userId.data.id}`);
    await fetchPhotos(); // Met à jour la liste des photos après la suppression
  } catch (error) {
    console.error('Erreur lors de la suppression de la photo:', error);
  }
}

// Fonction pour prévisualiser l'image sélectionnée
function previewImage() {
  if (profilePicture.value) {
    const reader = new FileReader();
    reader.onload = (e) => {
      // Vous pouvez ajouter ici une logique pour afficher l'aperçu de l'image
    };
    reader.readAsDataURL(profilePicture.value);
  }
}

// Initialisation des données au montage du composant
onMounted(() => {
  fetchUserData();
});

;

const location = ref(null);
const locationError = ref(null);
const openingTime = ref('');
const newOpeningTime = ref('');
const savedOpeningTime = ref('');
const modifiedOpeningTime = ref('');

const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        location.value = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };
        savePositionAndTime(); // Enregistrer la position et l'heure d'ouverture dans la base de données
      },
      (error) => {
        locationError.value = error.message;
      }
    );
  } else {
    locationError.value = "La géolocalisation n'est pas supportée par votre navigateur.";
  }
};

const savePositionAndTime = async () => {
  try {
    const response = await axios.post('http://localhost:8080/save-workshop', {
      id: userData.value.id, // Remplacez par l'ID de l'atelier à enregistrer
      latitude: location.value.latitude,
      longitude: location.value.longitude,
      openingTime: openingTime.value,
    });
    savedOpeningTime.value = response.data.opening_hours;
  } catch (error) {
    console.error('Erreur lors de l\'enregistrement de la position et de l\'heure d\'ouverture :', error);
  }
};

const modifyOpeningTime = async () => {
  try {
    const response = await axios.post('http://localhost:8080/save-workshop', {
      id: userData.value.id, // Remplacez par l'ID de l'atelier à modifier
      openingTime: newOpeningTime.value,
    });
    modifiedOpeningTime.value = response.data.opening_hours;
  } catch (error) {
    console.error('Erreur lors de la modification de l\'heure d\'ouverture :', error);
  }
};

</script>

<style scoped>
.pa-4 {
  padding: 16px;
}
.mb-4 {
  margin-bottom: 16px;
}

.position-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.v-card {
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.v-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.v-btn {
  transition: background-color 0.3s ease;
}

.v-btn:hover {
  background-color: #004d40;
}
</style>
