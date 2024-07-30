<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <v-card class="pa-4" outlined>
            <v-card-title>Paramètres de l'Application</v-card-title>
            <v-card-text>
              <v-form>
                <!-- Exemple de paramètres -->
                <v-text-field label="Nom de l'application" v-model="appName" />
                <v-switch label="Mode Maintenance" v-model="maintenanceMode" />
                <v-btn color="primary" @click="saveSettings">Sauvegarder</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const appName = ref('Mon Application')
  const maintenanceMode = ref(false)
  
  function saveSettings() {
    // Logique pour sauvegarder les paramètres de l'application
    console.log('Paramètres sauvegardés:', { appName: appName.value, maintenanceMode: maintenanceMode.value })
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour les paramètres de l'application */
  </style>
  