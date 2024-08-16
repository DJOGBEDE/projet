<template>
    <v-container class="fill-height d-flex align-center justify-center" fluid>
      <v-card class="pa-5" min-width="800">
        <v-card-title class="headline text-center">Inscription Admin</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submitForm">
            <v-text-field
              v-model="nom"
              label="Nom d'utilisateur"
              required
              :rules="[rules.required]"
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
            <v-text-field
              v-model="role"
              label="Rôle"
              required
              :rules="[rules.required]"
            ></v-text-field>
            <v-btn color="primary" class="white--text" type="submit" block>S'inscrire</v-btn>
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
        nom: '',
        password: '',
        role: '',
        showPassword: false,
        error: '',
        success: '',
        rules: {
          required: (value) => !!value || 'Ce champ est requis'
        }
      };
    },
    methods: {
      async submitForm() {
        this.error = '';
        this.success = '';
  
        try {
          const response = await axios.post('http://localhost:8080/register/admin', {
            nom: this.nom,
            mot_de_passe: this.password,
            role: this.role,
          });
  
          // Afficher un message de succès
          this.success = 'Inscription réussie !';
          
          // Redirection après inscription réussie
          this.$router.push('/admin/connection');
        } catch (error) {
          this.error = error.response ? error.response.data.message : 'Erreur lors de l\'inscription.';
        }
      }
    }
  };
  </script>
  
  <style>
  /* Style optionnel */
  </style>
  