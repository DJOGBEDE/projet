<template>
  <div>
    <h1>Liste des Ateliers</h1>
    <v-data-table
      :headers="headers"
      :items="workshops"
      item-key="id"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Ateliers</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="openAddDialog">Ajouter Atelier</v-btn>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon @click="editWorkshop(item)">mdi-pencil</v-icon>
        <v-icon @click="toggleWorkshopStatus(item)" :color="item.is_blocked ? 'red' : 'green'">
          {{ item.is_blocked ? 'mdi-lock' : 'mdi-lock-open' }}
          
        </v-icon>
      </template>
    </v-data-table>

    <!-- Dialog pour l'ajout d'atelier -->
    <v-dialog v-model="addDialog" max-width="500px">
      <v-container class="fill-height d-flex align-center justify-center" fluid>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="headline">Ajouter Atelier</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="submitAddForm">
                  <v-text-field
                    v-model="form.name"
                    label="Nom de l'atelier"
                    :rules="nameRules"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="form.address"
                    label="Adresse"
                    :rules="addressRules"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="form.phone_number"
                    label="Numéro de téléphone"
                    :rules="phoneRules"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="form.email"
                    label="Adresse e-mail"
                    type="email"
                    :rules="emailRules"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="form.website"
                    label="Site web (si disponible)"
                  ></v-text-field>
                  <v-text-field
                    v-model="form.password"
                    label="Mot de passe"
                    type="password"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="form.confirmPassword"
                    label="Confirmer le mot de passe"
                    type="password"
                    required
                  ></v-text-field>
                  <v-btn color="primary" class="white--text" type="submit">Ajouter</v-btn>
                  <v-btn @click="closeAddDialog" class="white--text mt-4" block>Annuler</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-dialog>

    <!-- Dialog pour la modification d'atelier -->
    <v-dialog v-model="editDialog" max-width="500px">
      <v-container class="fill-height d-flex align-center justify-center" fluid>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="headline">Modifier Atelier</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="submitEditForm">
                  <v-text-field
                    v-model="form.name"
                    label="Nom de l'atelier"
                    :rules="nameRules"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="form.address"
                    label="Adresse"
                    :rules="addressRules"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="form.phone_number"
                    label="Numéro de téléphone"
                    :rules="phoneRules"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="form.email"
                    label="Adresse e-mail"
                    type="email"
                    :rules="emailRules"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="form.website"
                    label="Site web (si disponible)"
                  ></v-text-field>
                  <v-btn color="primary" class="white--text" type="submit">Modifier</v-btn>
                  <v-btn @click="closeEditDialog" class="white--text mt-4" block>Annuler</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-dialog>

    <!-- Dialog pour le blocage/déblocage d'atelier -->
    <v-dialog v-model="statusDialog" max-width="500px">
      <v-card>
        <v-card-title class="headline">Changer le statut de l'atelier</v-card-title>
        <v-card-text>
          Êtes-vous sûr de vouloir {{ form.is_blocked ? 'débloquer' : 'bloquer' }} cet atelier ?
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="confirmToggleStatus">Oui</v-btn>
          <v-btn @click="closeStatusDialog">Non</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Notifications -->
    <v-snackbar v-model="snackbar.show" :timeout="snackbar.timeout" :color="snackbar.color">
      {{ snackbar.text }}
      <v-btn color="white" @click="snackbar.show = false">Fermer</v-btn>
    </v-snackbar>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const headers = [
  { text: 'Nom', value: 'name' },
  { text: 'Adresse', value: 'address' },
  { text: 'Numéro de Téléphone', value: 'phone_number' },
  { text: 'Email', value: 'email' },
  { text: 'Site Web', value: 'website' },
  { text: 'Horaires', value: 'opening_hours' },
  { text: 'Actions', value: 'actions', sortable: false },
]

const workshops = ref([])
const addDialog = ref(false)
const editDialog = ref(false)
const statusDialog = ref(false)
const form = ref({
  id: null,
  name: '',
  address: '',
  phone_number: '',
  email: '',
  website: '',
  password: '',
  confirmPassword: '',
  is_blocked: false
})

const nameRules = [v => !!v || 'Nom est requis']
const addressRules = [v => !!v || 'Adresse est requise']
const phoneRules = [v => !!v || 'Numéro de téléphone est requis']
const emailRules = [v => !!v || 'Email est requis']

const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  timeout: 6000
})

const fetchWorkshops = async () => {
  try {
    const response = await axios.get('http://localhost:8080/api/workshops')
    workshops.value = response.data.map(item => ({
      id: item[0],
      name: item[1],
      address: item[2],
      phone_number: item[3],
      email: item[4],
      website: item[5],
      opening_hours: item[6],
      latitude: item[7],
      longitude: item[8],
      photo: item[9],
      is_blocked: item[10] // Assuming this field indicates if the workshop is blocked
    }))
  } catch (error) {
    console.error('Erreur lors de la récupération des ateliers:', error)
  }
}

const openAddDialog = () => {
  form.value = {
    id: null,
    name: '',
    address: '',
    phone_number: '',
    email: '',
    website: '',
    password: '',
    confirmPassword: '',
    is_blocked: false
  }
  addDialog.value = true
}

const closeAddDialog = () => {
  addDialog.value = false
}

const submitAddForm = async () => {
  try {
    if (form.value.password.trim() !== form.value.confirmPassword.trim()) {
      throw new Error("Les mots de passe ne correspondent pas")
    }

    await axios.post('http://localhost:8080/api/workshops', form.value)
    snackbar.value = { show: true, text: 'Atelier ajouté avec succès', color: 'success' }
    await fetchWorkshops()
    closeAddDialog()
  } catch (error) {
    console.error('Erreur lors de l\'ajout de l\'atelier:', error)
    snackbar.value = { show: true, text: `Erreur : ${error.message}`, color: 'error' }
  }
}

const editWorkshop = (item) => {
  form.value = { ...item, password: '', confirmPassword: '' }
  editDialog.value = true
}

const closeEditDialog = () => {
  editDialog.value = false
}

const submitEditForm = async () => {
  try {
    await axios.put(`http://localhost:8080/api/workshops/${form.value.id}`, form.value)
    snackbar.value = { show: true, text: 'Atelier modifié avec succès', color: 'success' }
    await fetchWorkshops()
    closeEditDialog()
  } catch (error) {
    console.error('Erreur lors de la modification de l\'atelier:', error)
    snackbar.value = { show: true, text: `Erreur : ${error.message}`, color: 'error' }
  }
}

const toggleWorkshopStatus = (item) => {
  form.value = { ...item }
  statusDialog.value = true
}

const closeStatusDialog = () => {
  statusDialog.value = false
}

const confirmToggleStatus = async () => {
  try {
    form.value.is_blocked = !form.value.is_blocked
    await axios.put(`http://localhost:8080/api/workshops/${form.value.id}/status`, {
      is_blocked: form.value.is_blocked
    })
    snackbar.value = { show: true, text: 'Statut de l\'atelier mis à jour', color: 'success' }
    await fetchWorkshops()
    closeStatusDialog()
  } catch (error) {
    console.error('Erreur lors du changement de statut de l\'atelier:', error)
    snackbar.value = { show: true, text: `Erreur : ${error.response ? error.response.data.error : error.message}`, color: 'error' }
  }
}

onMounted(fetchWorkshops)
</script>
