<template>
  <v-container>
    <v-card>
      <v-card-title>Support Client</v-card-title>
      <v-card-text>
        <!-- Liste des demandes de support -->
        <v-list>
          <v-list-item v-for="ticket in supportTickets" :key="ticket.id">
            <v-list-item-content>
              <v-list-item-title class="mb-2">{{ ticket.subject }}</v-list-item-title>
              <v-list-item-subtitle>{{ ticket.name }} ({{ ticket.email }})</v-list-item-subtitle>
              <v-list-item-subtitle class="mt-2 mb-2">{{ ticket.message }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn color="primary" @click="openResponseDialog(ticket.id)">Répondre</v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <!-- Dialog pour répondre à une demande -->
    <v-dialog v-model="responseDialog" max-width="500px">
      <v-card>
        <v-card-title>
          Répondre à {{ selectedTicketId }}
        </v-card-title>
        <v-card-text>
          <!-- Message de succès -->
          <v-alert v-if="responseSent" type="success" class="text-center">
            Votre réponse a été envoyée avec succès !
          </v-alert>
          <!-- Formulaire de réponse -->
          <v-textarea
            v-else
            v-model="responseText"
            label="Votre réponse"
            rows="5"
            required
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <!-- Boutons pour l'envoi ou la confirmation -->
          <v-btn color="primary" v-if="!responseSent" @click="submitResponse">Envoyer</v-btn>
          <v-btn v-else color="primary" @click="closeDialog">OK</v-btn>
          <v-btn v-if="!responseSent" @click="responseDialog = false">Annuler</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Notification de confirmation -->
    <v-snackbar v-model="showSnackbar" :timeout="3000">
      Message envoyé avec succès !
      <v-btn color="primary" text @click="showSnackbar = false">OK</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const supportTickets = ref([])
const responseDialog = ref(false)
const selectedTicketId = ref(null)  // ID du ticket sélectionné
const responseText = ref('')
const responseSent = ref(false)  // État pour suivre si la réponse a été envoyée
const showSnackbar = ref(false)  // État pour gérer l'affichage de la notification

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8080/api/support/tickets')
    const data = await response.json()
    console.log('Données de l\'API:', data)

    // Vérifiez que data est un tableau
    if (Array.isArray(data)) {
      // Mapper les données pour créer des objets avec des propriétés nommées
      supportTickets.value = data.map(ticket => ({
        id: ticket[0],       // ID du ticket
        name: ticket[1],     // Nom de l'utilisateur
        email: ticket[2],    // Email de l'utilisateur
        subject: ticket[3],  // Sujet du ticket
        message: ticket[4],  // Message du ticket
      }))
      console.log('Support Tickets:', supportTickets.value) // Vérifiez le contenu des tickets
    } else {
      console.error('La structure des données de l\'API ne correspond pas à ce qui est attendu', data)
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des données de support:', error)
  }
})

// Ouvrir la boîte de dialogue de réponse avec l'ID du ticket
function openResponseDialog(ticketId) {
  selectedTicketId.value = ticketId  // Stocker l'ID du ticket sélectionné
  responseDialog.value = true
  responseSent.value = false  // Réinitialiser l'état d'envoi de la réponse
}

// Envoyer la réponse avec l'ID du ticket
async function submitResponse() {
  if (selectedTicketId.value) {
    try {
      const response = await fetch('http://localhost:8080/api/support/respond', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contact_id: selectedTicketId.value,  // Envoyer l'ID du ticket avec la réponse
          response: responseText.value,
        }),
      })

      if (response.ok) {
        console.log('Réponse envoyée avec succès')
        responseSent.value = true  // Indiquer que la réponse a été envoyée
        responseText.value = ''
        selectedTicketId.value = null  // Réinitialiser l'ID après l'envoi
        showSnackbar.value = true  // Afficher la notification
      } else {
        console.error('Erreur lors de l\'envoi de la réponse')
      }
    } catch (error) {
      console.error('Erreur lors de l\'envoi de la réponse:', error)
    }
  } else {
    console.error('Aucun ticket sélectionné')
  }
}

// Fermer la boîte de dialogue après confirmation
function closeDialog() {
  responseDialog.value = false
}
</script>

<style scoped>
/* Styles personnalisés pour le support client */
.text-center {
  text-align: center;
}
</style>
