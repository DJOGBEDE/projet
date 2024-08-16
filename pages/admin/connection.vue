<template>
    <v-container class="fill-height d-flex align-center justify-center" fluid>
      <v-card class="pa-5" min-width="800">
        <v-card-title class="headline text-center">Connexion Admin</v-card-title>
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
        nom: '',
        password: '',
        showPassword: false,
        error: '',
        success: '',
        adminData: null,  // Pour stocker les données de l'admin
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
          const response = await axios.post('http://localhost:8080/login/admin', {
            nom: this.nom,
            mot_de_passe: this.password,
          });
  
          const adminId = response.data.admin_id; // Récupérer l'ID de l'admin
          localStorage.setItem('admin_id', adminId); // Stocker l'ID de l'admin
  
          // Récupérer les données de l'admin après une connexion réussie
          await this.fetchAdminData();
  
          // Afficher un message de succès
          this.success = 'Connexion réussie !';
  
          // Redirection après connexion réussie
          this.$router.push('/admin/admin');
        } catch (error) {
          this.error = error.response ? error.response.data.message : 'Erreur lors de la connexion.';
        }
      },
      async fetchAdminData() {
        const adminId = localStorage.getItem('admin_id');
        if (adminId) {
          try {
            const response = await axios.get(`http://localhost:8080/admin/${adminId}`);
            this.adminData = response.data; // Stocker les données de l'admin
            console.log('Admin data:', this.adminData); // Afficher les données de l'admin dans la console
          } catch (error) {
            console.error('Erreur lors de la récupération des données de l\'admin:', error);
          }
        }
      }
    }
  };
  </script>
  
  <style>
  /* Style optionnel */
  </style>
  