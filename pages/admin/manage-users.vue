<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <v-card class="pa-4" outlined>
            <v-card-title>Gestion des Utilisateurs</v-card-title>
            <v-card-text>
              <v-data-table :headers="headers" :items="users" item-key="id">
                <template v-slot:top>
                  <v-toolbar flat>
                    <v-toolbar-title>Utilisateurs</v-toolbar-title>
                  </v-toolbar>
                </template>
                <template v-slot:item.action="{ item }">
                  <v-btn @click="editUser(item)" color="primary">Modifier</v-btn>
                  <v-btn @click="deleteUser(item.id)" color="red">Supprimer</v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const headers = ref([
    { text: 'Nom', value: 'name' },
    { text: 'Email', value: 'email' },
    { text: 'Actions', value: 'action', sortable: false },
  ])
  
  const users = ref([
    { id: 1, name: 'Utilisateur 1', email: 'user1@example.com' },
    { id: 2, name: 'Utilisateur 2', email: 'user2@example.com' },
    // Ajoute des données d'exemple ou connecte une API pour récupérer les utilisateurs
  ])
  
  function editUser(user) {
    // Logique pour éditer un utilisateur
  }
  
  function deleteUser(userId) {
    // Logique pour supprimer un utilisateur
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la gestion des utilisateurs */
  </style>
  