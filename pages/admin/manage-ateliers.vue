<template>
    <v-container>
      <v-card>
        <v-card-title>Gestion des Ateliers</v-card-title>
        <v-card-text>
          <!-- Liste des ateliers avec options d'ajout, modification, suppression -->
          <v-list>
            <v-list-item v-for="atelier in ateliers" :key="atelier.id">
              <v-list-item-content>
                <v-list-item-title>{{ atelier.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ atelier.email }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn icon @click="editAtelier(atelier)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deleteAtelier(atelier.id)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
          <v-btn color="primary" @click="addAtelier">Ajouter un Atelier</v-btn>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const ateliers = ref([
    { id: 1, name: "Atelier Mécanique", email: "atelier@example.com" },
    { id: 2, name: "Garage Auto", email: "garage@example.com" },
  ])
  
  function addAtelier() {
    console.log("Ajouter un nouvel atelier.")
  }
  
  function editAtelier(atelier) {
    console.log("Modifier l'atelier:", atelier)
  }
  
  function deleteAtelier(atelierId) {
    console.log("Supprimer l'atelier avec l'ID:", atelierId)
  }
  </script>
  