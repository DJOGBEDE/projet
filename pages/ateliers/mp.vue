<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <!-- Barre de Navigation des Paramètres -->
          <v-card class="pa-4" outlined>
            <v-tabs v-model="tab" background-color="primary" dark>
              <v-tab>Modifier le Mot de Passe</v-tab>
              <v-tab>Récupérer le Mot de Passe</v-tab>
            </v-tabs>
            
            <!-- Modification de Mot de Passe -->
            <v-tabs-items v-model="tab">
              <v-tab-item>
                <v-card-text>
                  <v-form @submit.prevent="changePassword">
                    <v-text-field
                      v-model="passwords.currentPassword"
                      label="Mot de passe actuel"
                      type="password"
                      required
                    ></v-text-field>
                    <v-text-field
                      v-model="passwords.newPassword"
                      label="Nouveau mot de passe"
                      type="password"
                      required
                    ></v-text-field>
                    <v-text-field
                      v-model="passwords.confirmPassword"
                      label="Confirmer le nouveau mot de passe"
                      type="password"
                      required
                    ></v-text-field>
                    <v-btn type="submit" color="primary">Modifier le mot de passe</v-btn>
                  </v-form>
                </v-card-text>
              </v-tab-item>
  
              <!-- Récupération de Mot de Passe -->
              <v-tab-item>
                <v-card-text>
                  <v-form @submit.prevent="recoverPassword">
                    <v-text-field
                      v-model="recovery.email"
                      label="Adresse e-mail"
                      type="email"
                      required
                    ></v-text-field>
                    <v-btn type="submit" color="primary">Récupérer le mot de passe</v-btn>
                  </v-form>
                </v-card-text>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  // État pour la navigation par onglets
  const tab = ref(0)
  
  // Modification de Mot de Passe
  const passwords = ref({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  
  function changePassword() {
    // Logique pour changer le mot de passe
    if (passwords.value.newPassword !== passwords.value.confirmPassword) {
      console.error('Les mots de passe ne correspondent pas')
      return
    }
    console.log('Mot de passe modifié:', passwords.value)
    // Implémenter la logique de modification de mot de passe, par exemple via une API
  }
  
  // Récupération de Mot de Passe
  const recovery = ref({
    email: ''
  })
  
  function recoverPassword() {
    // Logique pour récupérer le mot de passe
    console.log('Récupération du mot de passe pour:', recovery.value.email)
    // Implémenter la logique de récupération de mot de passe, par exemple via une API
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page de modification et de récupération de mot de passe */
  </style>
  