<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <!-- Consultation des Avis -->
          <v-row class="mb-4">
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Consultation des Avis</v-card-title>
                <v-card-text>
                  <v-list>
                    <v-list-item-group v-if="reviews.length > 0">
                      <v-list-item
                        v-for="(review, index) in reviews"
                        :key="index"
                      >
                        <v-list-item-content>
                          <v-list-item-title>
                            {{ review.client }}
                          </v-list-item-title>
                          <v-list-item-subtitle>
                            {{ review.comment }}
                          </v-list-item-subtitle>
                          <v-rating
                            :value="review.rating"
                            readonly
                            color="amber"
                          ></v-rating>
                          <v-btn
                            v-if="!review.response"
                            @click="replyToReview(index)"
                            color="primary"
                          >Répondre</v-btn>
                        </v-list-item-content>
                        <v-list-item-content v-if="review.response">
                          <v-list-item-subtitle class="ml-4">
                            <strong>Réponse:</strong> {{ review.response }}
                          </v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list-item-group>
                    <v-list-item v-else>
                      <v-list-item-content>
                        <v-list-item-title>Aucun avis trouvé.</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Répondre à un Avis -->
          <v-dialog v-model="replyDialog" max-width="500px">
            <v-card>
              <v-card-title>Répondre à l'Avis</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="submitReply">
                  <v-textarea
                    v-model="currentReply"
                    label="Votre réponse"
                    required
                  ></v-textarea>
                  <v-btn type="submit" color="primary">Envoyer la réponse</v-btn>
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
  const reviews = ref([
    { client: 'Jean Dupont', comment: 'Excellent service!', rating: 5, response: '' },
    { client: 'Marie Curie', comment: 'Très bon accueil.', rating: 4, response: '' }
  ])
  
  const replyDialog = ref(false)
  const currentReply = ref('')
  const currentReviewIndex = ref(null)
  
  function replyToReview(index) {
    // Ouvre le dialogue pour répondre à un avis
    currentReviewIndex.value = index
    replyDialog.value = true
  }
  
  function submitReply() {
    // Logique pour soumettre la réponse
    if (currentReviewIndex.value !== null) {
      reviews.value[currentReviewIndex.value].response = currentReply.value
      replyDialog.value = false
      currentReply.value = ''
      console.log('Réponse envoyée', reviews.value)
    }
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page de gestion des avis */
  </style>
  