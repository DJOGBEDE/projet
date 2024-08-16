<template>
    <v-app>
        <v-app-bar app color="primary" dark>
      <v-toolbar-title>Paramètres</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Acceuil</v-btn>
      <v-btn text @click="$router.push('/ateliers/dashbord')">Tableau de bord</v-btn>
      <v-btn text @click="$router.push('/ateliers/profil')">Profil</v-btn>
      <v-btn text @click="$router.push('/ateliers/services')">Services</v-btn>
      <v-btn text @click="$router.push('/ateliers/rendezvous')">Rendez-vous</v-btn>
     
     
     
    </v-app-bar>
      <v-main>
        <v-container fluid>
          <!-- Barre de Navigation des Paramètres -->
          <v-card class="pa-4" outlined>
            <v-tabs v-model="tab" background-color="primary" dark>
              
            </v-tabs>
            
            <!-- Préférences -->
            <v-tabs-items v-model="tab">
              
  
              <!-- Avis -->
              <v-tab-item>
                <v-card-text>
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
                </v-card-text>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-container>
      </v-main>
  
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
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  // État pour la navigation par onglets
  const tab = ref(0)
  
  // Préférences
  const preferences = ref({
    emailNotifications: false,
    smsNotifications: false,
    emailCommunication: false,
    phoneCommunication: false,
  })
  
  function savePreferences() {
    // Logique pour sauvegarder les préférences, par exemple en utilisant une API
    console.log('Préférences sauvegardées:', preferences.value)
  }
  
  // Avis
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
  /* Styles personnalisés pour la page des paramètres */
  </style>
  