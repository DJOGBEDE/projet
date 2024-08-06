<template>
  <v-container>
    <v-card class="pa-5">
      <v-card-title class="headline">Informations de l'utilisateur</v-card-title>
      <v-card-text>
        <v-alert v-if="error" type="error">{{ error }}</v-alert>
        <v-alert v-if="success" type="success">{{ success }}</v-alert>

        <div v-if="userData">
          <p><strong>Email :</strong> {{ userData.email }}</p>
          <p><strong>Nom :</strong> {{ userData.name }}</p>
          <p><strong>Autres informations :</strong> {{ userData.otherInfo }}</p>
          <!-- Ajoutez d'autres champs en fonction des données de l'utilisateur -->
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userData: null,
      error: '',
      success: ''
    };
  },
  async mounted() {
    await this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      const token = localStorage.getItem('token'); // Récupérer le token

      try {
        // Envoi de la requête pour récupérer les données de l'utilisateur
        const response = await axios.get('http://localhost:8080/api/userdata', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        this.userData = response.data; // Stocker les données de l'utilisateur
        this.success = 'Données récupérées avec succès !';
      } catch (error) {
        this.error = error.response ? error.response.data.message : 'Erreur lors de la récupération des données.';
      }
    }
  }
};
</script>

<style>
/* Style optionnel */
</style>
