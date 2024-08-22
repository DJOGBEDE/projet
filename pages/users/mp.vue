<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card class="pa-4">
          <v-card-title>Heure d'ouverture</v-card-title>
          <v-card-text>
            <p v-if="openingTime">Heure d'ouverture : {{ openingTime }}</p>
            <v-alert v-if="error" type="error" dismissible>{{ error }}</v-alert>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Variables pour l'heure d'ouverture et les erreurs
const openingTime = ref('');
const error = ref('');

// Fonction pour récupérer l'heure d'ouverture depuis l'API
const fetchOpeningTime = async () => {
  try {
    const token = process.client ? localStorage.getItem('token') : null;
    if (token) {
      const response = await axios.get('http://localhost:8080/api/atelier/opening-time', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      openingTime.value = response.data.opening_time; // Assurez-vous que le champ est correct
    }
  } catch (err) {
    error.value = 'Erreur lors de la récupération de l\'heure d\'ouverture : ' + err.message;
  }
};

// Appeler la fonction pour récupérer les données lors du montage du composant
onMounted(() => {
  fetchOpeningTime();
});
</script>

<style scoped>
.pa-4 {
  padding: 16px;
}
</style>
