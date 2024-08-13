<template>
  <v-app>
    <!-- Barre de navigation -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Profil de l'Atelier</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/ateliers/dashbord')">Tableau de bord</v-btn>
      <v-btn text @click="$router.push('/ateliers/services')">Services</v-btn>
      <v-btn text @click="$router.push('/ateliers/rendezvous')">Rendez-vous</v-btn>
      <v-btn text @click="$router.push('/ateliers/stats')">Statistiques</v-btn>
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

         <!-- Gestion des Photos -->
         <v-row>
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Gestion des Photos</v-card-title>
              <v-card-text>
                <v-file-input
                  v-model="photoFiles"
                  label="Ajouter ou Modifier les Photos"
                  multiple
                  accept="image/*"
                  @change="handleFileChange"
                />
                <v-btn @click="uploadImage" color="primary">Télécharger</v-btn>
                <v-row class="mt-4">
                  <v-col
                    v-for="(photo, index) in profile.photos"
                    :key="index"
                    cols="12"
                    md="4"
                  >
                    <v-img :src="photo" class="mb-2" />
                    <v-btn @click="removePhoto(index)" color="red">Supprimer</v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const specificId = ref('')
const image = ref(null)
const imagePreview = ref(null)
const images = ref([])

const previewImage = () => {
  if (image.value) {
    imagePreview.value = URL.createObjectURL(image.value)
  }
}

// Définition du profil de l'atelier
const profile = ref({
  name: '',
  address: '',
  phone: '',
  email: '',
  website: '',
  photos: []
});

// Variables pour les fichiers photo
const photoFiles = ref([]);
const userData = ref(null);

// Fonction pour gérer les changements de fichier
function handleFileChange(event) {
  // Convertir les fichiers en URL pour les prévisualiser
  photoFiles.value = Array.from(event.target.files).map(file => URL.createObjectURL(file));
}

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
      userData.value = response.data;

      // Mise à jour des informations de profil
      profile.value.name = response.data.name;
      profile.value.email = response.data.email;
      profile.value.phone = response.data.phone_number;
      profile.value.address = response.data.adresse;
      profile.value.website = response.data.website;

      // Récupérer les photos de profil
      fetchProfilePhotos();
    } catch (error) {
      console.error('Erreur lors de la récupération des données de l\'utilisateur:', error);
      userData.value = null;
    }
  }
}

// Fonction pour mettre à jour le profil
async function updateProfile() {
  try {
    await axios.put(`http://localhost:8080/api/atelier/${userData.value.id}`, {
      name: profile.value.name,
      email: profile.value.email,
      phone: profile.value.phone,
      address: profile.value.address,
      website: profile.value.website
    });
    console.log('Informations mises à jour', profile.value);
  } catch (error) {
    console.error('Erreur lors de la mise à jour du profil', error);
  }
}

// Fonction pour télécharger les photos
function uploadPhotos() {
  profile.value.photos.push(...photoFiles.value);
  photoFiles.value = [];
  console.log('Photos téléchargées', profile.value.photos);
}

// Fonction pour récupérer les photos de profil
async function fetchProfilePhotos() {
  const token = process.client ? localStorage.getItem('token') : null;
  try {
    const response = await axios.get(`http://localhost:8080/api/user/${userData.value.id}/profile-picture`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    profile.value.photos = [response.data.profilePictureUrl];
  } catch (error) {
    console.error('Erreur lors de la récupération des photos de profil', error);
  }
}

const uploadImage = async () => {
  if (image.value && userData.value.id) {
    const reader = new FileReader()
    reader.readAsDataURL(image.value)
    reader.onload = async () => {
      const base64Image = reader.result.split(',')[1]
      try {
        await axios.post(`http://localhost:8080/upload/${userData.value.id}`, {
          image_data: base64Image,
        })
        alert('Image uploaded successfully!')
        image.value = null
        imagePreview.value = null
        specificId.value = ''
        fetchImages() // Refresh images after upload
      } catch (error) {
        console.error(error)
        alert('Failed to upload image.')
      }
    }
  } else {
    alert('Please provide a specific ID and select an image.')
  }
}

// Fonction pour supprimer une photo
function removePhoto(index) {
  profile.value.photos.splice(index, 1);
  console.log('Photo supprimée', profile.value.photos);
}

// Initialisation des données au montage du composant
onMounted(() => {
  fetchUserData();
});
</script>

<style scoped>
.pa-4 {
  padding: 16px;
}
.mb-4 {
  margin-bottom: 16px;
}
</style>
