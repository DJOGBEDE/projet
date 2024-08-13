<template>
  <v-container class="fill-height d-flex align-center justify-center" fluid>
    <v-card class="pa-5" min-width="800">
      <v-card-title class="headline text-center">Connexion Client</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitForm">
          <v-text-field
            v-model="email"
            label="Email"
            required
            :rules="[rules.required, rules.email]"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Mot de passe"
            :type="showPassword ? 'text' : 'password'"
            required
            :rules="[rules.required]"
            append-icon="mdi-eye"
            @click:append="showPassword = !showPassword"
          ></v-text-field>
          <v-btn color="primary" class="white--text" type="submit" block>Se connecter</v-btn>
          <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
          <v-alert v-if="success" type="success" class="mt-4">{{ success }}</v-alert>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      showPassword: false,
      error: '',
      success: '',
      userData: null,  // Pour stocker les données de l'utilisateur
      rules: {
        required: (value) => !!value || 'Ce champ est requis',
        email: (value) => {
          const pattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
          return pattern.test(value) || 'Email invalide';
        }
      }
    };
  },
  methods: {
    async submitForm() {
      this.error = '';
      this.success = '';

      try {
        const response = await axios.post('http://localhost:8080/api/login', {
          email: this.email,
          password: this.password,
        });

        const token = response.data.token; // Récupérer le token
        localStorage.setItem('token', token); // Stocker le token

        // Récupérer les données de l'utilisateur après une connexion réussie
        await this.fetchUserData();

        // Afficher un message de succès
        this.success = 'Connexion réussie !';

        // Redirection après connexion réussie
        this.$router.push('/users/dashbord');
      } catch (error) {
        this.error = error.response ? error.response.data.message : 'Erreur lors de la connexion.';
      }
    },
    async fetchUserData() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await axios.get('http://localhost:8080/api/user', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.userData = response.data; // Stocker les données de l'utilisateur
          console.log('User data:', this.userData); // Afficher les données de l'utilisateur dans la console
        } catch (error) {
          console.error('Erreur lors de la récupération des données de l\'utilisateur:', error);
        }
      }
    }
  }
};
</script>


<style>
/* Style optionnel */
</style>
