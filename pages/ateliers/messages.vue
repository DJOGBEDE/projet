<template>
  <v-app>
    <v-container fluid>
      <!-- Liste des discussions -->
      <v-card>
        <v-card-title>
          <span>Discussions</span>
        </v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item-group>
              <v-list-item 
                v-for="discussion in discussions" 
                :key="discussion.user_id" 
                @click="fetchMessages(discussion)"
              >
                <v-list-item-avatar>
                  <v-avatar>
                    <img :src="getAvatarUrl(discussion.user_id_2)" alt="Avatar">
                  </v-avatar>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>User {{ discussion.user_id_2 }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card-text>
      </v-card>

      <!-- Zone d'affichage des messages -->
      <v-card v-if="selectedDiscussion" class="mt-4">
        <v-card-title>
          <span>Messages</span>
        </v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item-group>
              <v-list-item 
                v-for="message in messages" 
                :key="message.id"
                :class="{
                  'message-sent': message.user_id === userData.value.id,
                  'message-received': message.user_id !== userData.value.id
                }"
              >
                <v-list-item-avatar v-if="message.user_id !== userData.value.id">
                  <v-avatar>
                    <img :src="getAvatarUrl(message.user_id)" alt="Avatar">
                  </v-avatar>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>{{ message.subject }}</v-list-item-title>
                  <v-list-item-subtitle>{{ message.message }}</v-list-item-subtitle>
                  <v-list-item-subtitle>{{ formatDate(message.created_at) }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-text-field v-model="newMessage" label="Écrire un message" @keyup.enter="sendMessage"></v-text-field>
          <v-btn @click="sendMessage" color="primary">Envoyer</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-app>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const discussions = ref([]);
const messages = ref([]);
const newMessage = ref('');
const selectedDiscussion = ref(null);
const workshopId = 47; // ID de l'atelier

const userData = ref(null);

// Récupère les données de l'utilisateur connecté
const fetchUserData = async () => {
  const token = process.client ? localStorage.getItem('token') : null;
  if (token) {
    try {
      const response = await axios.get('http://localhost:8080/api/atelier', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      userData.value = response.data; // Stocker les données de l'utilisateur
      await fetchDiscussions(); // Récupérer les discussions après avoir les données de l'utilisateur
    } catch (error) {
      console.error("Erreur lors de la récupération des données de l'utilisateur:", error);
      userData.value = null; // Réinitialiser en cas d'erreur
    }
  }
};

// Récupère la liste des discussions
const fetchDiscussions = async () => {
  if (userData.value && userData.value.id) {
    try {
      const response = await axios.get(`http://localhost:8080/api/discussions/${userData.value.id}/messages`);
      discussions.value = response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des discussions:', error);
    }
  } else {
    console.error("Les données de l'utilisateur ne sont pas encore disponibles.");
  }
};

// Récupère les messages d'une discussion sélectionnée
const fetchMessages = async (discussion) => {
  selectedDiscussion.value = discussion;  // Stocker la discussion sélectionnée

  try {
    const response = await axios.get(`http://localhost:8080/api/messages/${discussion.user_id}/${userData.value.id}`);
    messages.value = response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des messages:', error);
  }
};

// Envoie un message
const sendMessage = async () => {
  if (!newMessage.value || !selectedDiscussion.value) return;

  const { user_id_2 } = selectedDiscussion.value;

  try {
    await axios.post('http://localhost:8080/api/messages', {
      message: newMessage.value,
      user_id: userData.value.id, // ID de l'utilisateur qui envoie le message (l'atelier ici)
      message_users: user_id_2, // ID de l'autre utilisateur
      workshop_id: workshopId,
    });
    newMessage.value = ''; // Réinitialiser le champ de message
    fetchMessages(selectedDiscussion.value); // Récupérer les messages mis à jour
  } catch (error) {
    console.error("Erreur lors de l'envoi du message:", error);
  }
};

// Fonction pour formater les dates
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
  return new Date(dateString).toLocaleDateString('fr-FR', options);
};

// Fonction pour obtenir l'URL de l'avatar d'un utilisateur
const getAvatarUrl = (userId) => {
  return `https://api.adorable.io/avatars/50/${userId}.png`;
};

// Récupérer les données de l'utilisateur lorsque le composant est monté
onMounted(() => {
  fetchUserData();
  // Vérifier périodiquement les nouveaux messages
  setInterval(() => {
    if (selectedDiscussion.value) {
      fetchMessages(selectedDiscussion.value);
    }
  }, 5000); // Vérifie toutes les 5 secondes
});
</script>
<style scoped>
.pa-4 {
  padding: 16px;
}
.mb-4 {
  margin-bottom: 16px;
}

.message-sent {
  justify-content: flex-end;
  display: flex;
  background-color: #e0f7fa;
  border-radius: 10px;
  margin-bottom: 10px;
  padding: 10px;
  animation: fadeIn 0.3s ease-in-out;
}

.message-received {
  justify-content: flex-start;
  display: flex;
  background-color: #ffebee;
  border-radius: 10px;
  margin-bottom: 10px;
  padding: 10px;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
