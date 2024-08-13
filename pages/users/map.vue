<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Mes Rendez-vous</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Historique des Rendez-vous</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item-group v-if="resultats.length > 0">
                    <v-list-item
                      v-for="resultat in resultats"
                      :key="resultat.id"
                    >
                      <v-list-item-content>
                        <v-list-item-title>
                          {{ resultat.date }} à {{ resultat.time }}
                        </v-list-item-title>
                        <v-list-item-subtitle class="mt-6 mr-4">
                          {{ resultat.details }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
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
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const resultats = ref([]); // Pour stocker les rendez-vous
const userData = ref({}); // Initialisez userData comme un objet vide

// Fonction pour récupérer les données de l'utilisateur
const fetchUserData = async () => {
  const token = process.client ? localStorage.getItem('token') : null; 
  if (token) {
    try {
      const response = await axios.get('http://localhost:8080/api/user', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      userData.value = response.data; // Stocker les données de l'utilisateur
    } catch (error) {
      console.error('Erreur lors de la récupération des données de l\'utilisateur:', error);
      userData.value = null; 
    }
  }
};

// Fonction pour récupérer les rendez-vous
const fetchAppointments = async () => {
  if (userData.value && userData.value.id) { // Vérifiez si userData.value existe et a une ID
    const token = process.client ? localStorage.getItem('token') : null; 
    try {
      const response = await axios.get(`http://localhost:8080/api/reservations/${userData.value.id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      resultats.value = response.data; // Stockez les résultats dans resultats
      console.log(resultats.value);
    } catch (error) {
      console.error('Erreur lors de la récupération des rendez-vous', error);
    }
  } else {
    console.error('Les données de l\'utilisateur ne sont pas disponibles.');
  }
};

// Récupérer les données lors du chargement du composant
onMounted(() => {
  fetchUserData().then(() => {
    fetchAppointments(); // Appel des rendez-vous après que l'utilisateur a été récupéré
  });
});
</script>

<style scoped>
/* Styles personnalisés pour la page des rendez-vous */
</style>
