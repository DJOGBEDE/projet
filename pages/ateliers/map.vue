<template>
  <div class="notification-icon">
    <v-btn @click="markAsViewed" icon>
      <v-icon>mdi-bell</v-icon>
      <div v-if="unviewedCount > 0" class="notification-dot"></div>
    </v-btn>

    <v-menu v-if="notifications.length > 0" offset-y>
      <template #activator="{ props }">
        <v-btn v-bind="props" icon>
          <v-icon>mdi-bell</v-icon>
        </v-btn>
      </template>
      <v-list min-width="800px">
        <v-list-item-group>
          <v-list-item
            v-for="(notification, index) in notifications"
            :key="index"
            @click="openDialog(notification)"
          >
            <v-list-item-content>
              <v-list-item-title>{{ notification.message }}</v-list-item-title>
              <v-list-item-subtitle>{{ formatDate(notification.created_at) }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-menu>

    <v-dialog v-model="dialog" max-width="800px" width="100%" height="400px">
  <v-card>
    <v-card-title min-width="800px"  >{{ selectedNotification?.message }}</v-card-title>
    <v-card-subtitle>{{ formatDate(selectedNotification?.created_at) }}</v-card-subtitle>
    <v-card-text>
      <p>Détails de la notification ici...</p>
      <p>{{ selectedNotification?.workshop_messages }}</p>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="dialog = false">Fermer</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const notifications = ref([]);
const unviewedCount = ref(0);
const dialog = ref(false);
const selectedNotification = ref(null);
const workshopId = 47; // Remplace par l'ID de l'atelier

// Récupère les notifications
const fetchNotifications = async () => {
  try {
    const response = await axios.get(`http://localhost:8080/api/notifications/${workshopId}`);
    notifications.value = response.data;
    unviewedCount.value = notifications.value.length; // Compte les notifications non consultées
  } catch (error) {
    console.error('Erreur lors de la récupération des notifications:', error);
  }
};

// Marquer les notifications comme consultées
const markAsViewed = async () => {
  if (unviewedCount.value > 0) {
    try {
      await axios.post(`http://localhost:8080/api/notifications/viewed/${workshopId}`);
      notifications.value = []; // Vider les notifications après consultation
      unviewedCount.value = 0; // Réinitialiser le compteur
    } catch (error) {
      console.error('Erreur lors de la mise à jour des notifications:', error);
    }
  }
};

// Ouvre le dialogue avec les détails de la notification
const openDialog = (notification) => {
  selectedNotification.value = notification;
  dialog.value = true;
};

// Formater la date
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString(); // Formate selon vos besoins
};

onMounted(fetchNotifications);
</script>

<style scoped>
.notification-icon {
  position: relative;
}

.notification-dot {
  position: absolute;
  top: 0; /* Ajustez pour positionner le point légèrement sur l'icône */
  right: -5px; /* Ajustez pour positionner le point à droite de l'icône */
  width: 12px; /* Taille du point */
  height: 12px; /* Taille du point */
  background-color: red; /* Couleur du point */
  border-radius: 50%; /* Pour un point circulaire */
}
</style>
