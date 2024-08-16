<template>
  <v-app>
    <v-main>
      <v-container fluid>
        <v-card class="pa-4" outlined>
          <v-card-title class="text-h5 font-weight-bold">Gestion des Utilisateurs</v-card-title>
          <v-card-text>
            <v-data-table :headers="headers" :items="users" item-key="id">
              <template v-slot:top>
                <v-toolbar flat>
                  <v-toolbar-title>Utilisateurs</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" dark @click="fetchUsers">Rafraîchir</v-btn>
                  <v-btn color="primary" dark @click="showAddDialog">Ajouter Utilisateur</v-btn>
                </v-toolbar>
              </template>
              <template v-slot:item.action="{ item }">
                <v-btn @click="editUser(item)" color="primary" icon>
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>

        <!-- Dialog pour ajout d'utilisateur -->
        <v-dialog v-model="addDialog" max-width="500">
          <v-card>
            <v-card-title class="headline">Ajouter un utilisateur</v-card-title>
            <v-card-text>
              <v-form ref="formAdd" v-model="formValid">
                <v-text-field
                  v-model="newUser.name"
                  label="Nom d'utilisateur"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="newUser.email"
                  label="Email"
                  type="email"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="newUser.password"
                  label="Mot de passe"
                  type="password"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="newUser.phone"
                  label="Numéro de téléphone"
                  required
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="addUser">Ajouter</v-btn>
              <v-btn text @click="addDialog = false">Annuler</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Dialog pour modification d'utilisateur -->
        <v-dialog v-model="editDialog" max-width="500">
          <v-card>
            <v-card-title class="headline">Modifier l'utilisateur</v-card-title>
            <v-card-text>
              <v-form ref="formEdit">
                <v-text-field
                  v-model="editedUser.username"
                  label="Nom d'utilisateur"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="editedUser.email"
                  label="Email"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="editedUser.role"
                  label="Rôle"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="editedUser.phone"
                  label="Téléphone"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="editedUser.created_at"
                  label="Créé le"
                  disabled
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="updateUser">Sauvegarder</v-btn>
              <v-btn text @click="editDialog = false">Annuler</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Définir les en-têtes du tableau
const headers = ref([
  { text: 'Nom d\'utilisateur', value: 'username' },
  { text: 'Email', value: 'email' },
  { text: 'Rôle', value: 'role' },
  { text: 'Téléphone', value: 'phone' },
  { text: 'Créé le', value: 'created_at' },
  { text: 'Actions', value: 'action', sortable: false },
])

// Stocker les utilisateurs récupérés
const users = ref([])

// Stocker les informations de l'utilisateur à ajouter
const newUser = ref({
  name: '',
  email: '',
  password: '',
  phone: ''
})
const addDialog = ref(false)
const formValid = ref(false)

// Stocker les informations de l'utilisateur en cours d'édition
const editedUser = ref({
  id: null,
  username: '',
  email: '',
  role: '',
  phone: '',
  created_at: ''
})
const editDialog = ref(false)

// Fonction pour récupérer les utilisateurs
const fetchUsers = async () => {
  try {
    const response = await axios.get('http://localhost:8080/api/users/all')
    users.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des utilisateurs:', error)
  }
}

// Fonction pour ouvrir le dialogue d'ajout
function showAddDialog() {
  newUser.value = {
    username: '',
    email: '',
    password: '',
    phone: ''
  }
  addDialog.value = true
}

// Fonction pour ajouter un nouvel utilisateur
const addUser = async () => {
  if (formValid.value) {
    try {
      const response = await axios.post('http://localhost:8080/api/register', newUser.value)
      users.value.push(response.data)
      addDialog.value = false
    } catch (error) {
      console.error('Erreur lors de l\'ajout de l\'utilisateur:', error)
    }
  } else {
    alert('Veuillez remplir tous les champs du formulaire.')
  }
}

// Fonction pour ouvrir le dialogue d'édition
function editUser(user) {
  editedUser.value = { ...user } // Copier les informations de l'utilisateur
  editDialog.value = true
}

// Fonction pour mettre à jour les informations de l'utilisateur
const updateUser = async () => {
  try {
    await axios.put(`http://localhost:8080/api/users/${editedUser.value.id}`, editedUser.value)
    users.value = users.value.map(user => (user.id === editedUser.value.id ? editedUser.value : user))
    editDialog.value = false
  } catch (error) {
    console.error('Erreur lors de la mise à jour de l\'utilisateur:', error)
  }
}

// Récupérer les utilisateurs lors du montage du composant
onMounted(() => {
  fetchUsers()
})
</script>