<template>
  <div>
    <v-text-field
      class="mb-4 ml-4"
      v-model="search"
      density="comfortable"
      placeholder="Rechercher un service"
      prepend-inner-icon="mdi-magnify"
      style="max-width: 900px;"
      variant="solo"
      clearable
      hide-details
    ></v-text-field>

    <v-card class="pa-4" outlined>
      <v-card-title>Liste des Ateliers</v-card-title>
    <v-container>
      <v-row>
        <v-col v-for="service in paginatedServices" :key="service.id" cols="12" sm="6" md="4">
          <v-card @click="goToAtelier(service.workshop_id)" class="mb-4" outlined>
            <v-card-title>{{ service.name }}</v-card-title>
            <v-card-subtitle>{{ service.description }}</v-card-subtitle>
            <v-card-text>
              <div v-if="getAtelierById(service.workshop_id)">
                <h3>Atelier Associé :</h3>
                <v-list dense>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-store</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title class="text-subtitle-1">
                        <strong>Nom:</strong> {{ getAtelierById(service.workshop_id).name }}
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-map-marker</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title class="text-subtitle-1">
                        <strong>Adresse:</strong> {{ getAtelierById(service.workshop_id).address }}
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-phone</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title class="text-subtitle-1">
                        <strong>Téléphone:</strong> {{ getAtelierById(service.workshop_id).phone_number }}
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-web</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title class="text-subtitle-1">
                        <strong>Site Web:</strong>
                        <a :href="getAtelierById(service.workshop_id).website" target="_blank">{{ getAtelierById(service.workshop_id).website }}</a>
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-clock-outline</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title class="text-subtitle-1">
                        <strong>Heures d'ouverture:</strong> {{ getAtelierById(service.workshop_id).opening_hours }}
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-pagination
        v-model="currentPage"
        :length="pageCount"
        class="mt-4"
        color="primary"
      ></v-pagination>
    </v-container>
  </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const services = ref([]);
const ateliers = ref([]);
const search = ref('');
const currentPage = ref(1);
const itemsPerPage = 6;

const router = useRouter();

onMounted(async () => {
  try {
    // Récupération des services
    const responseServices = await axios.get('http://localhost:8080/api/services');
    services.value = responseServices.data;
    
    // Récupération de tous les ateliers
    const responseAteliers = await axios.get('http://localhost:8080/api/ateliers');
    ateliers.value = responseAteliers.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des services ou des ateliers:', error);
  }
});

// Filtrer les services en fonction de la recherche
const filterServices = () => {
  return services.value.filter(service =>
    service.name.toLowerCase().includes(search.value.toLowerCase()) ||
    service.description.toLowerCase().includes(search.value.toLowerCase())
  );
};

// Filtrer les services uniques par atelier
const filteredServices = computed(() => {
  const uniqueServices = [];
  const seenWorkshops = new Set();

  filterServices().forEach(service => {
    // Ajout uniquement si l'atelier n'a pas déjà été vu
    if (!seenWorkshops.has(service.workshop_id)) {
      uniqueServices.push(service);
      seenWorkshops.add(service.workshop_id);
    }
  });

  return uniqueServices;
});

// Pagination des services filtrés
const paginatedServices = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredServices.value.slice(start, end);
});

// Nombre total de pages pour la pagination
const pageCount = computed(() => Math.ceil(filteredServices.value.length / itemsPerPage));

// Récupérer les détails de l'atelier par ID
const getAtelierById = (id) => {
  return ateliers.value.find(atelier => atelier.id === id);
};

// Rediriger vers la page de l'atelier
const goToAtelier = (id) => {
  router.push(`/users/${id}`);
};
</script>

<style scoped>
h1 {
  font-size: 2em;
  margin-bottom: 0.5em;
  color: #3f51b5;
}

h3 {
  font-size: 1.2em;
  margin-top: 0.5em;
  margin-bottom: 0.2em;
  color: #3f51b5;
}

.text-center {
  text-align: center;
}

a {
  color: #1976D2;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
