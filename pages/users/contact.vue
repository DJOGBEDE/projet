<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <!-- Formulaire de Contact -->
          <v-row class="mb-4">
            <v-col cols="12" md="6">
              <v-card class="pa-4" outlined>
                <v-card-title>Formulaire de Contact</v-card-title>
                <v-card-text>
                  <v-form @submit.prevent="submitForm">
                    <v-text-field
                      v-model="form.name"
                      label="Nom"
                      required
                    />
                    <v-text-field
                      v-model="form.email"
                      label="Email"
                      type="email"
                      required
                    />
                    <v-text-field
                      v-model="form.subject"
                      label="Sujet"
                      required
                    />
                    <v-textarea
                      v-model="form.message"
                      label="Message"
                      required
                      rows="5"
                    />
                    <v-btn type="submit" color="primary">Envoyer</v-btn>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-col>
  
            <!-- Coordonnées -->
            <v-col cols="12" md="6">
              <v-card class="pa-4" outlined>
                <v-card-title>Coordonnées</v-card-title>
                <v-card-text>
                  <v-list>
                    <v-list-item>
                      <v-list-item-icon>
                        <v-icon>mdi-phone</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title>Téléphone:</v-list-item-title>
                        <v-list-item-subtitle>{{ contactInfo.phone }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-icon>
                        <v-icon>mdi-email</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title>Email:</v-list-item-title>
                        <v-list-item-subtitle>
                          <v-btn
                            text
                            :href="`mailto:${contactInfo.email}`"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {{ contactInfo.email }}
                          </v-btn>
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-icon>
                        <v-icon>mdi-map-marker</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title>Adresse:</v-list-item-title>
                        <v-list-item-subtitle>{{ contactInfo.address }}</v-list-item-subtitle>
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
  import { ref } from 'vue'
  
  const form = ref({
    name: '',
    email: '',
    subject: '',
    message: ''
  })
  
  const contactInfo = ref({
    phone: '0123456789',
    email: 'contact@exemple.com',
    address: '123 Rue de l\'Exemple, Ville'
  })
  
  function submitForm() {
    // Logique pour soumettre le formulaire
    console.log('Form Submitted:', form.value)
    // Réinitialiser le formulaire après envoi
    form.value = {
      name: '',
      email: '',
      subject: '',
      message: ''
    }
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page de contact */
  </style>
  