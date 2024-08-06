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

    <!-- Affichage des données utilisateur -->
    <v-card v-if="user" class="mt-5 pa-5">
      <v-card-title class="headline">Bienvenue, {{ user.name }}</v-card-title>
      <v-card-text>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Téléphone:</strong> {{ user.phone }}</p>
        <p><strong>Rôle:</strong> {{ user.role }}</p>
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
      user: null, // Stocker les données de l'utilisateur
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

        const { access_token, refresh_token, user } = response.data; // Récupérer le token et les données utilisateur
        console.log('Token:', access_token); // Afficher le token dans la console
        localStorage.setItem('token', access_token); // Stocker le token

        // Afficher les données de l'utilisateur
        console.log('Données utilisateur:', user);
        this.user = user; // Stocker les données de l'utilisateur dans le data

        // Optionnel : Vous pouvez afficher un message de succès
        this.success = 'Connexion réussie !';

        // Redirection après connexion réussie
        this.$router.push('/users/dashbord');
      } catch (error) {
        this.error = error.response ? error.response.data.message : 'Erreur lors de la connexion.';
      }
    }
  }
};
</script>

<style>
/* Style optionnel */
</style>
