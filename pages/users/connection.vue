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
        console.log('Token:', token); // Afficher le token dans la console
        localStorage.setItem('token', token); // Stocker le token

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
