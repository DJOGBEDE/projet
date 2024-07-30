<template>
  <v-app>
    <!-- Barre d'Outils -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Tableau de Bord - Atelier</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text  @click="$router.push('/acceuil')">Accueil</v-btn>
      <v-btn text @click="goToProfile">Profil</v-btn>
      <v-btn icon @click="goToMessages">
        <v-icon>mdi-email</v-icon>
      </v-btn>
      <v-btn icon @click="goToNotifications">
        <v-icon>mdi-bell</v-icon>
      </v-btn>
      <v-btn text @click="showLogoutDialog">Déconnexion</v-btn>
    </v-app-bar>

    <!-- Dialog de Déconnexion -->
    <v-dialog v-model="logoutDialog" max-width="350">
      <v-card min-width="350">
        <v-card-title class="headline">Déconnexion</v-card-title>
        <v-card-text>Voulez-vous vraiment vous déconnecter ?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="logout">Oui</v-btn>
          <v-btn color="primary" text @click="hideLogoutDialog">Annuler</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Contenu Principal -->
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const logoutDialog = ref(false)

function goToHome() {
  router.push('/atelier/home')
}

function goToProfile() {
  router.push('/ateliers/profil')
}

function goToMessages() {
  router.push('/ateliers/messages')
}

function goToNotifications() {
  router.push('/ateliers/notifications')
}

function showLogoutDialog() {
  logoutDialog.value = true
}

function hideLogoutDialog() {
  logoutDialog.value = false
}

function logout() {
  // Logique pour la déconnexion
  console.log('Déconnecté')
  hideLogoutDialog()
}
</script>

<style scoped>
/* Styles personnalisés pour le tableau de bord */
</style>
