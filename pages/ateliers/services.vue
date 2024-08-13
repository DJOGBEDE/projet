<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Services</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Acceuil</v-btn>
      <v-btn text @click="$router.push('/ateliers/dashbord')">Tableau de bord</v-btn>
      <v-btn text @click="$router.push('/ateliers/profil')">Profil</v-btn>
      <v-btn text @click="$router.push('/ateliers/rendezvous')">Rendez-vous</v-btn>
      <v-btn text @click="$router.push('/ateliers/stats')">Statistiques</v-btn>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <!-- Ajouter de Nouveaux Services -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Ajouter de Nouveaux Services</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="addService">
                  <v-text-field v-model="newService.name" label="Nom du service" required />
                  <v-text-field v-model="newService.description" label="Description" required />
                  <v-btn type="submit" color="primary">Ajouter le service</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Modifier les Services Existants -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Modifier les Services Existants</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item-group v-if="services.length > 0">
                    <v-list-item v-for="(service, index) in services" :key="service.id">
                      <v-list-item-content>
                        <v-list-item-title class="mb-4">{{ service.name }}</v-list-item-title>
                        <v-list-item-subtitle class="mb-6">{{ service.description }}</v-list-item-subtitle>
                      </v-list-item-content>
                      <v-list-item-action>
                        <v-btn @click="editService(index)" class="mr-4" color="primary">Modifier</v-btn>
                        <v-btn @click="confirmDeleteService(service.id)" color="red">Supprimer</v-btn>
                      </v-list-item-action>
                    </v-list-item>
                  </v-list-item-group>
                  <v-list-item v-else>
                    <v-list-item-content>
                      <v-list-item-title>Aucun service trouvé.</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Modifier un Service -->
        <v-dialog v-model="editDialog" max-width="500px">
          <v-card>
            <v-card-title>Modifier le Service</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="updateService">
                <v-text-field v-model="currentService.name" label="Nom du service" required />
                <v-text-field v-model="currentService.description" label="Description" required />
                <v-btn type="submit" color="primary">Mettre à jour</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-dialog>

        <!-- Dialog de confirmation de suppression -->
        <v-dialog v-model="confirmDeleteDialog" max-width="400px">
          <v-card>
            <v-card-title class="headline">Confirmer la Suppression</v-card-title>
            <v-card-text>
              Êtes-vous sûr de vouloir supprimer ce service définitivement ?
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn color="grey" text @click="confirmDeleteDialog = false">Annuler</v-btn>
              <v-btn color="red" text @click="deleteService(confirmedServiceId)">Supprimer</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const services = ref([]);
const newService = ref({ name: '', description: '', workshop_id: 1 }); // Remplacez workshop_id par une valeur appropriée
const editDialog = ref(false);
const currentService = ref({ name: '', description: '', workshop_id: '' });
const currentIndex = ref(null);
const userData = ref(null);
const confirmDeleteDialog = ref(false);
const confirmedServiceId = ref(null); // ID du service à confirmer pour suppression

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

async function fetchServices() {
  try {
    const response = await axios.get(`http://localhost:8080/services/workshop/${userData.value.id}`);
    
    services.value = response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des services:', error);
  }
}

async function addService() {
  try {
    const response = await axios.post('http://localhost:8080/services', {
      ...newService.value,
      workshop_id: userData.value.id
    });
    services.value.push(response.data);
    newService.value.name = '';
    newService.value.description = '';
  } catch (error) {
    console.error('Erreur lors de l\'ajout du service:', error);
  }
}

function editService(index) {
  currentIndex.value = index;
  currentService.value = { ...services.value[index] };
  editDialog.value = true;
}

async function updateService() {
  try {
    await axios.put(`http://localhost:8080/services/${currentService.value.id}`, currentService.value);
    services.value[currentIndex.value] = { ...currentService.value };
    editDialog.value = false;
  } catch (error) {
    console.error('Erreur lors de la mise à jour du service:', error);
  }
}

function confirmDeleteService(serviceId) {
  confirmedServiceId.value = serviceId; // Stocke l'ID du service à supprimer
  confirmDeleteDialog.value = true; // Ouvre le dialogue de confirmation
}

async function deleteService(serviceId) {
  try {
    await axios.delete(`http://localhost:8080/services/${serviceId}`);
    services.value = services.value.filter(service => service.id !== serviceId);
    confirmDeleteDialog.value = false; // Ferme le dialogue après la suppression
  } catch (error) {
    console.error('Erreur lors de la suppression du service:', error);
  }
}

// Récupérer les données de l'utilisateur et les services lorsque le composant est monté
onMounted(() => {
  fetchUserData().then(fetchServices);
});
</script>

<style scoped>
/* Styles personnalisés pour la page */
</style>
