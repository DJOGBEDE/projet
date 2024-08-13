<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Rendez-vous</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Acceuil</v-btn>
      <v-btn text @click="$router.push('/ateliers/dashbord')">Tableau de bord</v-btn>
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
                          :color="appointment.responded ? 'green' : 'primary'" 
                          @click="openReplyDialog(appointment)"
                        >
                          {{ appointment.responded ? 'Rendez-vous consulté' : 'Répondre' }}
                        </v-btn>
                        <v-btn 
                        class="ml-4" @click="confirmDeleteAppointment(appointment)" color="red">Annuler</v-btn>
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

        <!-- Dialogue pour répondre à un rendez-vous -->
        <v-dialog v-model="replyDialog" max-width="500px">
          <v-card>
            <v-card-title>Répondre au Rendez-vous</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="sendMessage">
                <v-text-field
                  v-model="replySubject"
                  label="Sujet"
                  required
                />
                <v-textarea
                  v-model="replyMessage"
                  label="Message"
                  required
                  rows="4"
                />
                <v-btn type="submit" color="primary">Envoyer</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-dialog>

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
const replyDialog = ref(false); // Dialogue de réponse
const replySubject = ref(''); // Sujet du message
const replyMessage = ref(''); // Message
const currentAppointment = ref({
  date: '',
  time: '',
  client: '',
  service: '',
  id: null // Ajouter un champ pour l'ID
})
const currentIndex = ref(null)
const cancellationReason = ref('')
const userData = ref(null);

// Fonction pour récupérer les rendez-vous depuis l'API
const fetchAppointments = async () => {
  if (userData.value) {
    try {
      const response = await axios.get(`http://localhost:8080/api/rendezvous/${userData.value.id}`);
      appointments.value = response.data.map(appointment => ({
        ...appointment,
        responded: false // Initialiser à false pour chaque rendez-vous
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
  // Ouvre le dialogue de confirmation pour l'annulation
  currentAppointment.value = { ...appointment }; // Stocker l'appointment pour l'annulation
  deleteDialog.value = true;
}

async function deleteAppointment() {
  if (!cancellationReason.value) {
    console.error('La raison d\'annulation est requise.');
    return;
  }

  try {
    const response = await axios.delete(`http://localhost:8080/api/rendezvous/${currentAppointment.value.id}`, {
      data: {
        reason: cancellationReason.value
      }
    });

    // Insérer une notification dans la table notifications
    await axios.post('http://localhost:8080/api/notifications', {
      message: 'Votre rendez-vous a été annulé.',
      type: 'annulation',
      user_id: currentAppointment.value.user_id, // ID du client
      created_at: new Date().toISOString(), // Ajout de la date actuelle au format ISO
      workshop_id: currentAppointment.value.atelier_id, // ID de l'atelier
      workshop_messages: cancellationReason.value
    });

    // Supprimer le rendez-vous
    appointments.value = appointments.value.filter(appointment => appointment.id !== currentAppointment.value.id);
    deleteDialog.value = false; // Fermer la boîte de dialogue
    cancellationReason.value = ''; // Réinitialiser la raison
    console.log('Rendez-vous annulé', currentAppointment.value.id);
    alert('Rendez-vous annulé avec succès.'); // Notification de succès
  } catch (error) {
    console.error('Erreur lors de l\'annulation du rendez-vous:', error);
  }
}

const fetchUserData = async () => {
  const token = process.client ? localStorage.getItem('token') : null; 
  if (token) {
    try {
      const response = await axios.get('http://localhost:8080/api/atelier', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      userData.value = response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des données de l\'utilisateur:', error);
      userData.value = null;
    }
  }
};

// Récupérer les données utilisateur et les rendez-vous lors du montage du composant
onMounted(async () => {
  await fetchUserData();
  await fetchAppointments();
});

// Ouvrir le dialogue de réponse
function openReplyDialog(appointment) {
  currentAppointment.value = { ...appointment }; // Stocker l'appointment pour répondre
  replyDialog.value = true; // Ouvrir le dialogue
}

// Envoyer un message
async function sendMessage() {
  if (!replySubject.value || !replyMessage.value) {
    console.error('Le sujet et le message sont requis.');
    return;
  }

  try {
    const response = await axios.post('http://localhost:8080/api/messages', {
      subject: replySubject.value,
      message: replyMessage.value,
      user_id: currentAppointment.value.user_id, // ID du client
      workshop_id: currentAppointment.value.atelier_id, // ID de l'atelier
      created_at: new Date().toISOString(),
    });

    // Réinitialiser les champs
    replySubject.value = '';
    replyMessage.value = '';
    replyDialog.value = false; // Fermer le dialogue
    console.log('Message envoyé', response.data);
    alert('Message envoyé avec succès.'); // Notification de succès

     // Marquer le rendez-vous comme répondu
     appointments.value[currentIndex.value].responded = true; // Mettre à jour l'état du rendez-vous

  } catch (error) {
    console.error('Erreur lors de l\'envoi du message:', error);
  }
}
</script>

<style scoped>
/* Styles personnalisés pour la page de gestion des rendez-vous */
</style>
