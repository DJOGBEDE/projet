<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>REndez-vous</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Acceuil</v-btn>
      <v-btn text @click="$router.push('/ateliers/profil')">Profil</v-btn>
      <v-btn text @click="$router.push('/ateliers/services')">Services</v-btn>
     
      <v-btn text @click="$router.push('/ateliers/stats')">Statistiques</v-btn>
     
     
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <!-- Consultation des Rendez-vous -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Consultation des Rendez-vous</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item-group v-if="appointments.length > 0">
                    <v-list-item
                      v-for="(appointment, index) in appointments"
                      :key="index"
                    >
                      <v-list-item-content>
                        <v-list-item-title class="mb-1">
                          {{ appointment.date }} à {{ appointment.time }}
                        </v-list-item-title>
                        <v-list-item-subtitle class="mb-4">
                          Client: {{ appointment.client }}<br>
                          Service: {{ appointment.service }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                      <v-list-item-action>
                        <v-btn @click="editAppointment(index)" class="mr-4" color="primary">Modifier</v-btn>
                        <v-btn @click="deleteAppointment(index)" color="red">Annuler</v-btn>
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

        <!-- Modifier un Rendez-vous -->
        <v-dialog v-model="editDialog" max-width="500px">
          <v-card>
            <v-card-title>Modifier le Rendez-vous</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="updateAppointment">
                <v-text-field
                  v-model="currentAppointment.date"
                  label="Date"
                  required
                  type="date"
                />
                <v-text-field
                  v-model="currentAppointment.time"
                  label="Heure"
                  required
                  type="time"
                />
                <v-text-field
                  v-model="currentAppointment.client"
                  label="Client"
                  required
                />
                <v-text-field
                  v-model="currentAppointment.service"
                  label="Service demandé"
                  required
                />
                <v-btn type="submit" color="primary">Mettre à jour</v-btn>
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
const appointments = ref([
  { date: '2024-08-01', time: '10:00', client: 'Jean Dupont', service: 'Réparation de freins' },
  { date: '2024-08-02', time: '14:00', client: 'Marie Curie', service: 'Changement d\'huile' }
])

const editDialog = ref(false)
const currentAppointment = ref({
  date: '',
  time: '',
  client: '',
  service: ''
})
const currentIndex = ref(null)

function editAppointment(index) {
  // Logique pour éditer un rendez-vous existant
  currentIndex.value = index
  currentAppointment.value = { ...appointments.value[index] }
  editDialog.value = true
  console.log('Modifier le rendez-vous', index)
}

function updateAppointment() {
  // Logique pour mettre à jour un rendez-vous existant
  if (currentIndex.value !== null) {
    appointments.value[currentIndex.value] = { ...currentAppointment.value }
    editDialog.value = false
    console.log('Rendez-vous mis à jour', appointments.value)
  }
}

function deleteAppointment(index) {
  // Logique pour annuler un rendez-vous existant
  appointments.value.splice(index, 1)
  console.log('Rendez-vous annulé', index)
}
</script>

<style scoped>
/* Styles personnalisés pour la page de gestion des rendez-vous */
</style>
