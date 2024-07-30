<template>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Tableau de Bord</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn :to="{ name: 'dashboard' }" text>Accueil</v-btn>
      <v-btn :to="{ name: 'profile' }" text>Profil</v-btn>
      <v-btn :to="{ name: 'messages' }" text>
        Messages
        <v-badge :content="messageCount" color="red" dot />
      </v-btn>
      <v-btn :to="{ name: 'notifications' }" text>
        Notifications
        <v-badge :content="notificationCount" color="red" dot />
      </v-btn>
      <v-btn @click="logout" text>Déconnexion</v-btn>
    </v-app-bar>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  // Simule le nombre de messages et notifications
  const messageCount = ref(5)
  const notificationCount = ref(3)
  
  // Fonction de déconnexion
  function logout() {
    // Ajoute ici la logique de déconnexion
    console.log('Déconnexion')
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la barre de navigation */
  </style>
  