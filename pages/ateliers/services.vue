<template>
    <v-app>
      <v-app-bar app color="primary" dark>
      <v-toolbar-title>Services</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Acceuil</v-btn>
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
                    <v-text-field
                      v-model="newService.name"
                      label="Nom du service"
                      required
                    />
                    <v-text-field
                      v-model="newService.description"
                      label="Description"
                      required
                    />
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
                      <v-list-item
                        v-for="(service, index) in services"
                        :key="index"
                      >
                        <v-list-item-content>
                          <v-list-item-title class="mb-4 " >
                            {{ service.name }}
                          </v-list-item-title>
                          <v-list-item-subtitle class="mb-6 " >
                            {{ service.description }}
                          </v-list-item-subtitle>
                        </v-list-item-content>
                        <v-list-item-action>
                          <v-btn @click="editService(index)" class="mr-4" color="primary">Modifier</v-btn>
                          <v-btn @click="deleteService(index)"   color="red">Supprimer</v-btn>
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
                  <v-text-field
                    v-model="currentService.name"
                    label="Nom du service"
                    required
                  />
                  <v-text-field
                    v-model="currentService.description"
                    label="Description"
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
  const services = ref([
    { name: 'Réparation de freins', description: 'Réparation complète des freins.' },
    { name: 'Changement d\'huile', description: 'Changement d\'huile rapide et efficace.' }
  ])
  
  const newService = ref({
    name: '',
    description: ''
  })
  
  const editDialog = ref(false)
  const currentService = ref({
    name: '',
    description: ''
  })
  const currentIndex = ref(null)
  
  function addService() {
    // Logique pour ajouter un nouveau service
    services.value.push({ ...newService.value })
    newService.value.name = ''
    newService.value.description = ''
    console.log('Service ajouté', services.value)
  }
  
  function editService(index) {
    // Logique pour éditer un service existant
    currentIndex.value = index
    currentService.value = { ...services.value[index] }
    editDialog.value = true
    console.log('Modifier le service', index)
  }
  
  function updateService() {
    // Logique pour mettre à jour un service existant
    if (currentIndex.value !== null) {
      services.value[currentIndex.value] = { ...currentService.value }
      editDialog.value = false
      console.log('Service mis à jour', services.value)
    }
  }
  
  function deleteService(index) {
    // Logique pour supprimer un service existant
    services.value.splice(index, 1)
    console.log('Service supprimé', index)
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page de gestion des services */
  </style>
  