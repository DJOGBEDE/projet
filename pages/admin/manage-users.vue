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
                </v-toolbar>
              </template>
              <template v-slot:item.action="{ item }">
                <v-btn @click="editUser(item)" color="primary" icon>
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn @click="confirmDeleteUser(item.id)" color="red" icon>
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
        
        <!-- Dialog pour confirmation de suppression -->
        <v-dialog v-model="deleteDialog" max-width="500">
          <v-card>
            <v-card-title class="headline">Confirmer la suppression</v-card-title>
            <v-card-text>Êtes-vous sûr de vouloir supprimer cet utilisateur ?</v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="red" @click="deleteUser">Supprimer</v-btn>
              <v-btn text @click="deleteDialog = false">Annuler</v-btn>
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

// Stocker l'ID de l'utilisateur à supprimer
const userIdToDelete = ref(null)
const deleteDialog = ref(false)

// Fonction pour récupérer les utilisateurs via API
const fetchUsers = async () => {
  try {
    const response = await axios.get('http://localhost:8080/api/rese')
    users.value = response.data
  } catch (error) {
    console.error('Erreur lors de la récupération des utilisateurs:', error)
  }
}

// Fonction pour éditer un utilisateur (logique à définir)
function editUser(user) {
  console.log('Modifier l\'utilisateur:', user)
  // Logique pour éditer l'utilisateur
}

// Fonction pour confirmer la suppression
function confirmDeleteUser(id) {
  userIdToDelete.value = id
  deleteDialog.value = true
}

// Fonction pour supprimer un utilisateur via API
const deleteUser = async () => {
  try {
    await axios.delete(`http://localhost:8080/api/selectusers/${userIdToDelete.value}`)
    users.value = users.value.filter(user => user.id !== userIdToDelete.value)
    deleteDialog.value = false
  } catch (error) {
    console.error('Erreur lors de la suppression de l\'utilisateur:', error)
  }
}

// Récupérer les utilisateurs lors du montage du composant
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
/* Styles personnalisés */
.v-card-title {
  color: #1976D2;
}

.v-btn {
  margin-right: 8px;
}
</style>
