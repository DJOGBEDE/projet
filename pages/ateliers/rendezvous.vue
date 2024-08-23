<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Rendez-vous</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Acceuil</v-btn>
      <v-btn text @click="$router.push('/ateliers/dashbord')">Tableau de bord</v-btn>
      <v-btn text @click="$router.push('/ateliers/profil')">Profil</v-btn>
      <v-btn text @click="$router.push('/ateliers/services')">Services</v-btn>
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
                      :key="appointment.id"
                    >
                      <v-list-item-content>
                        <v-list-item-title class="mb-1">
                          {{ appointment.date }} à {{ appointment.time }}
                        </v-list-item-title>
                        <div class="mb-4">Message: {{ appointment.message }} </div>
                        <div>Service: {{ appointment.services }}</div>
                      </v-list-item-content>
                      <v-list-item-action class="mt-3 mb-3">
                        <v-btn
                          v-if="!appointment.accepted"
                          color="green"
                          @click="confirmAcceptAppointment(appointment)"
                        >
                          Accepter
                        </v-btn>
                        <v-btn
                          v-if="appointment.accepted"
                          color="grey"
                          disabled
                        >
                          Accepté
                        </v-btn>
                        <v-btn
                          class="ml-4"
                          @click="confirmDeleteAppointment(appointment)"
                          color="red"
                        >
                          Annuler
                        </v-btn>
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

        <!-- Dialogue pour confirmer l'acceptation d'un Rendez-vous -->
        <v-dialog v-model="acceptDialog" max-width="500px">
          <v-card>
            <v-card-title>Confirmer l'acceptation du Rendez-vous</v-card-title>
            <v-card-text>
              <p class="mb-4">Voulez-vous accepter ce rendez-vous?</p>
              <v-btn @click="acceptAppointment" color="green">Oui</v-btn>
              <v-btn class="ml-4" @click="acceptDialog = false" color="grey">Non</v-btn>
            </v-card-text>
          </v-card>
        </v-dialog>

        

        <!-- Confirmer l'annulation d'un Rendez-vous -->
        <v-dialog v-model="deleteDialog" max-width="500px">
          <v-card>
            <v-card-title>Annuler le Rendez-vous</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="deleteAppointment">
                <v-text-field
                  v-model="cancellationReason"
                  label="Raison de l'annulation"
                  required
                />
                <v-btn type="submit" color="red">Confirmer l'annulation</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const appointments = ref([])
const editDialog = ref(false)
const deleteDialog = ref(false)
const replyDialog = ref(false)
const acceptDialog = ref(false) // Dialogue d'acceptation
const replySubject = ref('')
const replyMessage = ref('')
const currentAppointment = ref({
  date: '',
  time: '',
  client: '',
  service: '',
  id: null
})
const currentIndex = ref(null)
const cancellationReason = ref('')
const userData = ref(null)

// Fonction pour récupérer les rendez-vous depuis l'API
const fetchAppointments = async () => {
  if (userData.value) {
    try {
      const response = await axios.get(`http://localhost:8080/api/rendezvous/${userData.value.id}`);
      appointments.value = response.data.map(appointment => ({
        ...appointment,
        accepted: false, // Initialiser à false pour chaque rendez-vous
        responded: false
      }));
    } catch (error) {
      console.error('Erreur lors de la récupération des rendez-vous:', error);
    }
  }
}

function editAppointment(index) {
  currentIndex.value = index
  currentAppointment.value = { ...appointments.value[index] }
  editDialog.value = true
}

function updateAppointment() {
  if (currentIndex.value !== null) {
    appointments.value[currentIndex.value] = { ...currentAppointment.value }
    editDialog.value = false
    console.log('Rendez-vous mis à jour', appointments.value)
  }
}

function confirmDeleteAppointment(appointment) {
  currentAppointment.value = { ...appointment }
  deleteDialog.value = true
}

async function deleteAppointment() {
  if (!cancellationReason.value) {
    console.error('La raison d\'annulation est requise.')
    return
  }

  try {
    const response = await axios.delete(`http://localhost:8080/api/rendezvous/${currentAppointment.value.id}`, {
      data: {
        reason: cancellationReason.value
      }
    })

    await axios.post('http://localhost:8080/api/notifications', {
      message: 'Votre rendez-vous a été annulé.',
      type: 'annulation',
      user_id: currentAppointment.value.user_id,
      created_at: new Date().toISOString(),
      workshop_id: currentAppointment.value.atelier_id,
      workshop_messages: cancellationReason.value,
      rdv_id : currentAppointment.value.id,
    })

    appointments.value = appointments.value.filter(appointment => appointment.id !== currentAppointment.value.id)
    deleteDialog.value = false
    cancellationReason.value = ''
    console.log('Rendez-vous annulé', currentAppointment.value.id)
    alert('Rendez-vous annulé avec succès.')
  } catch (error) {
    console.error('Erreur lors de l\'annulation du rendez-vous:', error)
  }
}

const fetchUserData = async () => {
  const token = process.client ? localStorage.getItem('token') : null
  if (token) {
    try {
      const response = await axios.get('http://localhost:8080/api/atelier', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      userData.value = response.data
    } catch (error) {
      console.error('Erreur lors de la récupération des données de l\'utilisateur:', error)
      userData.value = null
    }
  }
}

onMounted(async () => {
  await fetchUserData()
  await fetchAppointments()
})

function confirmAcceptAppointment(appointment) {
  currentAppointment.value = { ...appointment }
  acceptDialog.value = true
}

async function acceptAppointment() {
  try {
    // Envoyer une notification pour indiquer que le rendez-vous a été accepté
    await axios.post('http://localhost:8080/api/notifications', {
      message: 'Votre rendez-vous a été accepté.',
      type: 'accepté',
      user_id: currentAppointment.value.user_id, // ID du client
      created_at: new Date().toISOString(), // Date actuelle au format ISO
      workshop_id: userData.value.id, // ID de l'atelier
      workshop_messages: 'Accepté',
      rdv_id : currentAppointment.value.id,
    });

    // Fermer le dialogue de confirmation
    acceptDialog.value = false;

    console.log('Rendez-vous accepté', currentAppointment.value.id);
    alert('Rendez-vous accepté avec succès.'); // Notification de succès

  } catch (error) {
    console.error('Erreur lors de l\'acceptation du rendez-vous:', error);
  }
}

</script>
