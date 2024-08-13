<template>
    <v-container>
      <v-card>
        <v-card-title>Messages & Notifications</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field label="Destinataires (Utilisateurs ou Ateliers)" v-model="recipients"></v-text-field>
            <v-textarea label="Message ou Notification" v-model="message"></v-textarea>
            <v-btn color="primary" @click="sendNotification">Envoyer</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const recipients = ref('')
  const message = ref('')
  
  function sendNotification() {
    console.log("Envoyer un message aux destinataires:", recipients.value)
    console.log("Message:", message.value)
  }
  </script>
  