<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <v-row justify="center">
            <v-col cols="12" md="8">
              <v-card class="pa-4" outlined>
                <v-card-title>Gestion des Préférences</v-card-title>
                <v-card-text>
                  <v-form>
                    <!-- Préférences de Notification -->
                    <v-row>
                      <v-col cols="12">
                        <h3>Préférences de Notification</h3>
                        <v-checkbox
                          v-model="preferences.emailNotifications"
                          label="Recevoir des notifications par e-mail"
                        ></v-checkbox>
                        <v-checkbox
                          v-model="preferences.smsNotifications"
                          label="Recevoir des notifications par SMS"
                        ></v-checkbox>
                      </v-col>
                    </v-row>
  
                    <!-- Préférences de Communication -->
                    <v-row>
                      <v-col cols="12">
                        <h3>Préférences de Communication</h3>
                        <v-checkbox
                          v-model="preferences.emailCommunication"
                          label="Communication par e-mail"
                        ></v-checkbox>
                        <v-checkbox
                          v-model="preferences.phoneCommunication"
                          label="Communication par téléphone"
                        ></v-checkbox>
                      </v-col>
                    </v-row>
  
                    <v-row justify="center" class="mt-4">
                      <v-col cols="12" md="4">
                        <v-btn color="primary" @click="savePreferences">
                          Sauvegarder
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-form>
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
  
  const preferences = ref({
    emailNotifications: false,
    smsNotifications: false,
    emailCommunication: false,
    phoneCommunication: false,
  })
  
  function savePreferences() {
    // Logique pour sauvegarder les préférences, par exemple en utilisant une API
    console.log('Préférences sauvegardées:', preferences.value)
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page des préférences */
  </style>
  