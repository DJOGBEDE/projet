<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <v-row>
            <v-col cols="12" md="3">
              <v-card class="pa-4" outlined>
                <v-card-title>Administration</v-card-title>
                <v-list dense>
                  <v-list-item :to="{ path: '/admin/manage-users' }">
                    <v-list-item-content>Gestion des Utilisateurs</v-list-item-content>
                  </v-list-item>
                  <v-list-item :to="{ path: '/admin/app-settings' }">
                    <v-list-item-content>Paramètres de l'Application</v-list-item-content>
                  </v-list-item>
                  <!-- Ajoute d'autres éléments de menu selon les besoins -->
                </v-list>
              </v-card>
            </v-col>
  
            <v-col cols="12" md="9">
              <v-card class="pa-4" outlined>
                <NuxtPage />
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script setup>
  </script>
  
  <style scoped>
  /* Styles personnalisés pour l'interface d'administration */
  </style>
  