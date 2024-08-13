<template>
    <v-container>
      <v-card>
        <v-card-title>Support Client</v-card-title>
        <v-card-text>
          <!-- Liste des demandes de support -->
          <v-list>
            <v-list-item v-for="ticket in supportTickets" :key="ticket.id">
              <v-list-item-content>
                <v-list-item-title>{{ ticket.subject }}</v-list-item-title>
                <v-list-item-subtitle>{{ ticket.user }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn color="primary" @click="respondToTicket(ticket)">Répondre</v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const supportTickets = ref([
    { id: 1, subject: "Problème de connexion", user: "Jean Dupont" },
    { id: 2, subject: "Erreur lors de la réservation", user: "Marie Durand" },
  ])
  
  function respondToTicket(ticket) {
    console.log("Répondre au ticket:", ticket)
  }
  </script>
  