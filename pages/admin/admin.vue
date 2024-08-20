<template>
  <v-app>
    <v-main>
      <v-container fluid>
        <!-- Header -->
        <v-row class="align-center mb-4">
          <v-col cols="12" md="8">
            <h1 class="text-h4 font-weight-bold">Tableau de Bord Administrateur</h1>
          </v-col>
          <v-col cols="12" md="4" class="text-md-right">
            <v-btn color="primary" dark @click="goTo('/acceuil')">
              <v-icon left>mdi-logout</v-icon> Déconnexion
            </v-btn>
          </v-col>
        </v-row>

        <v-row>
          <!-- Gestion des Utilisateurs -->
          <v-col cols="12" md="4">
            <v-hover v-slot:default="{ isHovering, props }">
              <v-card class="pa-4" outlined :elevation="isHovering ? 10 : 2" v-bind="props">
                <v-card-title class="d-flex align-center">
                  <v-icon large color="primary">mdi-account-multiple</v-icon>
                  <span class="ml-3 text-h6 font-weight-bold">Gestion des Utilisateurs</span>
                </v-card-title>
                <v-card-text>Ajoutez, modifiez ou supprimez des utilisateurs.</v-card-text>
                <v-card-actions>
                  <v-btn color="primary" @click="goTo('/admin/manage-users')">Gérer</v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>

          <!-- Gestion des Ateliers -->
          <v-col cols="12" md="4">
            <v-hover v-slot:default="{ isHovering, props }">
              <v-card class="pa-4" outlined :elevation="isHovering ? 10 : 2" v-bind="props">
                <v-card-title class="d-flex align-center">
                  <v-icon large color="primary">mdi-garage</v-icon>
                  <span class="ml-3 text-h6 font-weight-bold">Gestion des Ateliers</span>
                </v-card-title>
                <v-card-text>Gérez les informations des ateliers.</v-card-text>
                <v-card-actions>
                  <v-btn color="primary" @click="goTo('/admin/manage-ateliers')">Gérer</v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>

          <!-- Support Client -->
          <v-col cols="12" md="4">
            <v-hover v-slot:default="{ isHovering, props }">
              <v-card class="pa-4" outlined :elevation="isHovering ? 10 : 2" v-bind="props">
                <v-card-title class="d-flex align-center">
                  <v-icon large color="primary">mdi-headset</v-icon>
                  <span class="ml-3 text-h6 font-weight-bold">Support Client</span>
                </v-card-title>
                <v-card-text>Répondez aux demandes des utilisateurs.</v-card-text>
                <v-card-actions>
                  <v-btn color="primary" @click="goTo('/admin/support')">Gérer</v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>

          <!-- Messages et Notifications -->
          <v-col cols="12" md="6">
            <v-hover v-slot:default="{ isHovering, props }">
              <v-card class="pa-4" outlined :elevation="isHovering ? 10 : 2" v-bind="props">
                <v-card-title class="d-flex align-center">
                  <v-icon large color="primary">mdi-email</v-icon>
                  <span class="ml-3 text-h6 font-weight-bold">Messages & Notifications</span>
                </v-card-title>
                <v-card-text>Envoyez des notifications aux utilisateurs et ateliers.</v-card-text>
                <v-card-actions>
                  <v-btn color="primary" @click="goTo('/admin/manage-notifications')">Gérer</v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>

          <!-- Blocage pour Maintenance -->
          <v-col cols="12" md="6">
            <v-hover v-slot:default="{ isHovering, props }">
              <v-card class="pa-4" outlined :elevation="isHovering ? 10 : 2" v-bind="props">
                <v-card-title class="d-flex align-center">
                  <v-icon large color="primary">mdi-lock</v-icon>
                  <span class="ml-3 text-h6 font-weight-bold">Blocage pour Maintenance</span>
                </v-card-title>
                <v-card-text>Bloquez l'accès pour effectuer une maintenance.</v-card-text>
                <v-card-actions>
                  <v-btn color="primary" @click="showMaintenanceDialog">Bloquer</v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>

      <!-- Dialog de Maintenance -->
      <v-dialog v-model="maintenanceDialog" max-width="500">
        <v-card>
          <v-card-title class="headline">Blocage pour Maintenance</v-card-title>
          <v-card-text>Voulez-vous vraiment bloquer l'accès à tous les comptes pour la maintenance ?</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="blockAllAccounts">Confirmer</v-btn>
            <v-btn text @click="hideMaintenanceDialog">Annuler</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const maintenanceDialog = ref(false)

function goTo(path) {
  router.push(path)
}

function logout() {
  console.log("Déconnexion")
  // Logique de déconnexion ici
}

function showMaintenanceDialog() {
  maintenanceDialog.value = true
}

function hideMaintenanceDialog() {
  maintenanceDialog.value = false
}

function blockAllAccounts() {
  console.log("Tous les comptes sont maintenant bloqués pour maintenance.")
  hideMaintenanceDialog()
}
</script>

<style scoped>
/* Styles personnalisés pour le tableau de bord */
h1 {
  color: #424242;
}

.v-card-title {
  color: #1976D2;
}

.v-card-text {
  color: #616161;
}

.v-btn {
  transition: transform 0.2s;
}

.v-btn:hover {
  transform: scale(1.05);
}

.v-card {
  transition: box-shadow 0.3s;
}
</style>
