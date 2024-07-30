<template>
    <v-app>
      <v-app-bar app color="primary" dark>
      <v-toolbar-title>Tableau de bord</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Acceuil</v-btn>
      <v-btn text @click="$router.push('/users/dashbord')">Tableau de bord</v-btn>
     
      <v-btn icon @click="$router.push('/users/messages')">
        <v-icon>mdi-email</v-icon>
      </v-btn>
      <v-btn icon @click="$router.push('/users/notifications')">
        <v-icon>mdi-bell</v-icon>
      </v-btn>
    </v-app-bar>
      <v-main>
        <v-container fluid>
          <!-- Informations Personnelles -->
          <v-row class="mb-4">
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Informations Personnelles</v-card-title>
                <v-card-text>
                  <v-form @submit.prevent="updateProfile">
                    <v-text-field
                      v-model="profile.name"
                      label="Nom"
                      required
                    />
                    <v-text-field
                      v-model="profile.email"
                      label="Email"
                      type="email"
                      required
                    />
                    <v-text-field
                      v-model="profile.phone"
                      label="Numéro de Téléphone"
                    />
                    <v-btn type="submit" color="primary">Mettre à jour</v-btn>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Historique des Rendez-vous -->
          <v-row class="mb-4">
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Historique des Rendez-vous</v-card-title>
                <v-card-text>
                  <v-list>
                    <v-list-item-group v-if="appointments.length > 0">
                      <v-list-item
                        v-for="appointment in appointments"
                        :key="appointment.id"
                      >
                        <v-list-item-content>
                          <v-list-item-title>
                            {{ appointment.date }} à {{ appointment.time }}
                          </v-list-item-title>
                          <v-list-item-subtitle class="mt-6 mr-4">
                            {{ appointment.details }}
                          </v-list-item-subtitle>
                        </v-list-item-content>
                        <v-list-item-action>
                          <v-btn @click="viewDetails(appointment.id)" class="mt-4 mr-4">Voir détails</v-btn>
                          <v-btn @click="cancelAppointment(appointment.id)" class="mt-4 mr-4" color="red">Annuler</v-btn>
                        </v-list-item-action>
                      </v-list-item>
                    </v-list-item-group>
                    <v-list-item v-else>
                      <v-list-item-content>
                        <v-list-item-title>Aucun rendez-vous trouvé.</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Préférences -->
          <v-row>
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Préférences</v-card-title>
                <v-card-text>
                  <v-form>
                    <v-switch
                      v-model="preferences.notifications"
                      label="Notifications par email"
                    />
                    <v-switch
                      v-model="preferences.messages"
                      label="Messages"
                    />
                    <v-btn @click="updatePreferences" color="primary">Enregistrer les préférences</v-btn>
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
  const profile = ref({
    name: '',
    email: '',
    phone: ''
  })
  
  const appointments = ref([
    { id: 1, date: '2024-08-01', time: '10:00', details: 'Rendez-vous pour vérification' },
    { id: 2, date: '2024-08-05', time: '14:00', details: 'Changement d\'huile' }
  ])
  
  const preferences = ref({
    notifications: true,
    messages: false
  })
  
  function updateProfile() {
    // Logique pour mettre à jour les informations personnelles
    console.log('Informations mises à jour', profile.value)
  }
  
  function viewDetails(id) {
    // Logique pour afficher les détails du rendez-vous
    console.log('Afficher les détails du rendez-vous', id)
  }
  
  function cancelAppointment(id) {
    // Logique pour annuler le rendez-vous
    appointments.value = appointments.value.filter(appointment => appointment.id !== id)
    console.log('Rendez-vous annulé', id)
  }
  
  function updatePreferences() {
    // Logique pour mettre à jour les préférences
    console.log('Préférences mises à jour', preferences.value)
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page de gestion de profil */
  </style>
  