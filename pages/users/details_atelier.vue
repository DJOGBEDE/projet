<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <!-- Informations Générales -->
          <v-row class="mb-4">
            <v-col cols="12" md="6">
              <v-card class="pa-4" outlined>
                <v-img
                  src="https://via.placeholder.com/600x400"
                  height="200px"
                  class="white--text align-end"
                  gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                >
                  <v-card-title>{{ atelier.name }}</v-card-title>
                </v-img>
                <v-card-text>
                  <v-list>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Adresse:</v-list-item-title>
                        <v-list-item-subtitle>{{ atelier.address }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Téléphone:</v-list-item-title>
                        <v-list-item-subtitle>{{ atelier.phone }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Site Web:</v-list-item-title>
                        <v-list-item-subtitle>
                          <v-btn
                            text
                            :href="atelier.website"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {{ atelier.website }}
                          </v-btn>
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Services Proposés:</v-list-item-title>
                        <v-list-item-subtitle>{{ atelier.services.join(', ') }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Horaires d'Ouverture:</v-list-item-title>
                        <v-list-item-subtitle>{{ atelier.openingHours }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
  
            <!-- Carte de Localisation -->
            <v-col cols="12" md="6">
              <v-card class="pa-4" outlined>
                <v-card-title>Localisation</v-card-title>
                <v-card-text>
                  <!-- Remplacer par votre composant de carte -->
                  <div id="map" style="height: 400px; width: 100%;"></div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Prise de Rendez-vous -->
          <v-row class="mb-4">
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Prendre un Rendez-vous</v-card-title>
                <v-card-text>
                  <v-form>
                    <v-text-field label="Nom" v-model="appointment.name" />
                    <v-text-field label="Téléphone" v-model="appointment.phone" />
                    <v-menu
                      v-model="menu"
                      :close-on-content-click="false"
                      transition="scale-transition"
                      offset-y
                    >
                      <template #activator="{ on, attrs }">
                        <v-text-field
                          v-model="appointment.date"
                          label="Date"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                        />
                      </template>
                      <v-date-picker v-model="appointment.date" @input="menu = false" />
                    </v-menu>
                    <v-menu
                      v-model="menuTime"
                      :close-on-content-click="false"
                      transition="scale-transition"
                      offset-y
                    >
                      <template #activator="{ on, attrs }">
                        <v-text-field
                          v-model="appointment.time"
                          label="Heure"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                        />
                      </template>
                      <v-time-picker v-model="appointment.time" format="24hr" @input="menuTime = false" />
                    </v-menu>
                    <v-btn @click="submitAppointment" color="primary">Envoyer la demande</v-btn>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Contact Direct -->
          <v-row class="mb-4">
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Contact Direct</v-card-title>
                <v-card-text>
                  <v-btn @click="contactByPhone" color="primary" class="mr-2">Appeler l'Atelier</v-btn>
                  <v-btn @click="contactByEmail" color="primary">Envoyer un Message</v-btn>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Avis et Évaluation -->
          <v-row>
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Avis et Évaluation</v-card-title>
                <v-card-text>
                  <v-list>
                    <v-list-item-group v-if="reviews.length > 0">
                      <v-list-item v-for="review in reviews" :key="review.id">
                        <v-list-item-content>
                          <v-list-item-title>{{ review.author }}</v-list-item-title>
                          <v-list-item-subtitle>{{ review.date }}</v-list-item-subtitle>
                          <v-rating :value="review.rating" readonly />
                          <v-list-item-body>{{ review.comment }}</v-list-item-body>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list-item-group>
                    <v-list-item v-else>
                      <v-list-item-content>
                        <v-list-item-title>Aucun avis encore.</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                  <v-form>
                    <v-text-field label="Votre Nom" v-model="newReview.author" />
                    <v-textarea label="Votre Avis" v-model="newReview.comment" />
                    <v-rating v-model="newReview.rating" />
                    <v-btn @click="submitReview" color="primary">Soumettre un Avis</v-btn>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  // Données fictives pour l'exemple
  const atelier = ref({
    name: 'Atelier Exemple',
    address: '123 Rue de l\'Exemple, Ville',
    phone: '0123456789',
    website: 'https://www.exemple.com',
    services: ['Réparation Moteur', 'Changement Huile', 'Alignement Roues'],
    openingHours: 'Lundi - Vendredi: 09h00 - 18h00'
  })
  
  const appointment = ref({
    name: '',
    phone: '',
    date: '',
    time: ''
  })
  
  const menu = ref(false)
  const menuTime = ref(false)
  
  const reviews = ref([
    { id: 1, author: 'Jean Dupont', date: '2024-07-23', rating: 4, comment: 'Très bon service !' },
    { id: 2, author: 'Marie Martin', date: '2024-07-22', rating: 5, comment: 'Excellent, je recommande vivement.' }
  ])
  
  const newReview = ref({
    author: '',
    comment: '',
    rating: 0
  })
  
  function submitAppointment() {
    // Logique pour soumettre la demande de rendez-vous
  }
  
  function contactByPhone() {
    window.location.href = `tel:${atelier.value.phone}`
  }
  
  function contactByEmail() {
    window.location.href = `mailto:contact@${atelier.value.website}`
  }
  
  function submitReview() {
    // Logique pour soumettre un nouvel avis
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page des détails de l'atelier */
  #map {
    /* Ajustez la taille de la carte selon vos besoins */
  }
  </style>
  