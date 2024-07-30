<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <!-- Consultation des Messages -->
          <v-row class="mb-4">
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Consultation des Messages</v-card-title>
                <v-card-text>
                  <v-list>
                    <v-list-item-group v-if="messages.length > 0">
                      <v-list-item
                        v-for="(message, index) in messages"
                        :key="index"
                        @click="selectMessage(index)"
                      >
                        <v-list-item-content>
                          <v-list-item-title>
                            {{ message.subject }}
                          </v-list-item-title>
                          <v-list-item-subtitle>
                            De: {{ message.name }} ({{ message.email }})
                          </v-list-item-subtitle>
                        </v-list-item-content>
                        <v-list-item-action>
                          <v-btn @click.stop="replyToMessage(index)" color="primary">Répondre</v-btn>
                        </v-list-item-action>
                      </v-list-item>
                    </v-list-item-group>
                    <v-list-item v-else>
                      <v-list-item-content>
                        <v-list-item-title>Aucun message trouvé.</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Répondre au Message -->
          <v-dialog v-model="replyDialog" max-width="500px">
            <v-card>
              <v-card-title>Répondre au Message</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="sendReply">
                  <v-text-field
                    v-model="replyMessage.subject"
                    label="Sujet"
                    required
                  />
                  <v-textarea
                    v-model="replyMessage.body"
                    label="Message"
                    required
                    rows="5"
                  />
                  <v-btn type="submit" color="primary">Envoyer</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-dialog>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  // Données fictives pour l'exemple
  const messages = ref([
    { name: 'Jean Dupont', email: 'jean@example.com', subject: 'Demande de rendez-vous', body: 'Je souhaite prendre un rendez-vous pour la semaine prochaine.' },
    { name: 'Marie Curie', email: 'marie@example.com', subject: 'Information sur les services', body: 'Pouvez-vous me donner plus d\'informations sur vos services ?' }
  ])
  
  const replyDialog = ref(false)
  const selectedMessageIndex = ref(null)
  const replyMessage = ref({
    subject: '',
    body: ''
  })
  
  function selectMessage(index) {
    // Logique pour sélectionner un message et afficher ses détails
    selectedMessageIndex.value = index
    console.log('Message sélectionné', messages.value[index])
  }
  
  function replyToMessage(index) {
    // Logique pour répondre à un message
    selectedMessageIndex.value = index
    replyMessage.value.subject = `Re: ${messages.value[index].subject}`
    replyMessage.value.body = `Bonjour ${messages.value[index].name},\n\n`
    replyDialog.value = true
    console.log('Répondre au message', index)
  }
  
  function sendReply() {
    // Logique pour envoyer une réponse
    if (selectedMessageIndex.value !== null) {
      console.log('Réponse envoyée', replyMessage.value)
      replyDialog.value = false
    }
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page de gestion des messages */
  </style>
  