<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Profil de l'Atelier</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/ateliers/services')">Services</v-btn>
      <v-btn text @click="$router.push('/ateliers/rendezvous')">Rendez-vous</v-btn>
      <v-btn text @click="$router.push('/ateliers/stats')">Statistiques</v-btn>
      <v-btn text @click="$router.push('/ateliers/paramettres')">Paramètres</v-btn>
     
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <!-- Informations de Profil -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Informations de Profil</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="updateProfile">
                  <v-text-field
                    v-model="profile.name"
                    label="Nom de l'atelier"
                    required
                  />
                  <v-text-field
                    v-model="profile.address"
                    label="Adresse"
                    required
                  />
                  <v-text-field
                    v-model="profile.phone"
                    label="Numéro de téléphone"
                    required
                  />
                  <v-text-field
                    v-model="profile.email"
                    label="Adresse e-mail"
                    type="email"
                    required
                  />
                  <v-text-field
                    v-model="profile.website"
                    label="Site web"
                  />
                  <v-btn type="submit" color="primary">Mettre à jour</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Horaires d'Ouverture -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Horaires d'Ouverture</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="updateOpeningHours">
                  <v-text-field
                    v-model="openingHours.monday"
                    label="Lundi"
                  />
                  <v-text-field
                    v-model="openingHours.tuesday"
                    label="Mardi"
                  />
                  <v-text-field
                    v-model="openingHours.wednesday"
                    label="Mercredi"
                  />
                  <v-text-field
                    v-model="openingHours.thursday"
                    label="Jeudi"
                  />
                  <v-text-field
                    v-model="openingHours.friday"
                    label="Vendredi"
                  />
                  <v-text-field
                    v-model="openingHours.saturday"
                    label="Samedi"
                  />
                  <v-text-field
                    v-model="openingHours.sunday"
                    label="Dimanche"
                  />
                  <v-btn type="submit" color="primary">Mettre à jour</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Gestion des Photos -->
        <v-row>
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title>Gestion des Photos</v-card-title>
              <v-card-text>
                <v-file-input
                  v-model="photoFiles"
                  label="Ajouter ou Modifier les Photos"
                  multiple
                  accept="image/*"
                  @change="handleFileChange"
                />
                <v-btn @click="uploadPhotos" color="primary">Télécharger</v-btn>
                <v-row class="mt-4">
                  <v-col
                    v-for="(photo, index) in profile.photos"
                    :key="index"
                    cols="12"
                    md="4"
                  >
                    <v-img :src="photo" class="mb-2" />
                    <v-btn @click="removePhoto(index)" color="red">Supprimer</v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

const profile = ref({
  name: '',
  address: '',
  phone: '',
  email: '',
  website: '',
  photos: []
})

const openingHours = ref({
  monday: '',
  tuesday: '',
  wednesday: '',
  thursday: '',
  friday: '',
  saturday: '',
  sunday: ''
})

const photoFiles = ref([])

function handleFileChange(event) {
  // Met à jour photoFiles avec les fichiers sélectionnés
  photoFiles.value = Array.from(event.target.files).map(file => URL.createObjectURL(file))
}

function updateProfile() {
  // Logique pour mettre à jour les informations du profil
  console.log('Informations de profil mises à jour', profile.value)
}

function updateOpeningHours() {
  // Logique pour mettre à jour les horaires d'ouverture
  console.log('Horaires d\'ouverture mis à jour', openingHours.value)
}

function uploadPhotos() {
  // Logique pour télécharger les photos
  profile.value.photos.push(...photoFiles.value)
  photoFiles.value = []
  console.log('Photos téléchargées', profile.value.photos)
}

function removePhoto(index) {
  // Logique pour supprimer une photo
  profile.value.photos.splice(index, 1)
  console.log('Photo supprimée', index)
}

function goToServices() {
  router.push('/atelier/services')
}

function goToAppointments() {
  router.push('/atelier/appointments')
}

function goToStatistics() {
  router.push('/atelier/statistics')
}

function goToSettings() {
  router.push('/atelier/settings')
}
</script>

<style scoped>
/* Styles personnalisés pour la page de gestion de profil */
</style>
