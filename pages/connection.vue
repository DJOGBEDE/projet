<template>
    <v-container class="fill-height d-flex align-center justify-center" fluid>
      <v-card class="pa-5" min-width="900">
        <v-img src="/home/delkael/Téléchargements/projet2/mecano_project/public/v12.jpg" height="600px"></v-img>
        <v-card-title class="headline text-center">Bienvenue sur Notre Application</v-card-title>
        <v-card-subtitle class="mb-4 text-center">
          Veuillez choisir votre type de connexion
        </v-card-subtitle>
  
        <v-card-text>
          <v-row justify="center">
            <v-col cols="12" class="d-flex justify-center">
              <nuxt-link to="/users/connection">
                <v-btn color="primary" class="white--text mx-2" large>Connexion Client</v-btn>
              </nuxt-link>
            </v-col>
            <v-col cols="12" class="d-flex justify-center">
              <nuxt-link to="/ateliers/connection">
                <v-btn color="secondary" class="white--text mx-2" large>Connexion Atelier</v-btn>
              </nuxt-link>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script>
  export default {
    // Pas besoin de script pour cet exemple
  }
  </script>
  
  <style>
  .fill-height {
    min-height: 100vh; /* S'assure que le conteneur occupe toute la hauteur de la vue */
  }
  </style>
  