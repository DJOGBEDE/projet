<template>
  <v-app>
    <v-main>
      <v-container class="fill-height d-flex align-center justify-center" fluid>
        <v-row justify="center" >
          <v-col cols="12" md="8">
            <v-card >
              <v-card-title class="headline">Nous Contacter</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="submitForm">
                  <v-text-field
                    v-model="contact.name"
                    label="Nom"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="contact.email"
                    label="Email"
                    type="email"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="contact.subject"
                    label="Sujet"
                    required
                  ></v-text-field>
                  <v-textarea
                    v-model="contact.message"
                    label="Message"
                    required
                  ></v-textarea>
                  <v-btn color="primary" class="white--text" type="submit">Envoyer</v-btn>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <span>Suivez-nous sur les réseaux sociaux :</span>
                <v-spacer></v-spacer>
                <v-btn icon @click="openLink('https://www.facebook.com')">
                  <v-icon>mdi-facebook</v-icon>
                </v-btn>
                <v-btn icon @click="openLink('https://www.twitter.com')">
                  <v-icon>mdi-twitter</v-icon>
                </v-btn>
                <v-btn icon @click="openLink('https://www.instagram.com')">
                  <v-icon>mdi-instagram</v-icon>
                </v-btn>
                <v-btn icon @click="openLink('https://www.linkedin.com')">
                  <v-icon>mdi-linkedin</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

const contact = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const submitForm = async () => {
  try {
    const response = await fetch('http://localhost:8080/api/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(contact.value),
    });

    const result = await response.json();

    if (response.ok) {
      console.log('Formulaire de contact soumis:', result.message);
      // Réinitialiser le formulaire après soumission
      contact.value.name = ''
      contact.value.email = ''
      contact.value.subject = ''
      contact.value.message = ''
    } else {
      console.error('Erreur lors de la soumission:', result.error);
    }
  } catch (error) {
    console.error('Erreur lors de la soumission:', error);
  }
};

const openLink = (url) => {
  window.open(url, '_blank')
}
</script>

<style scoped>
/* Styles personnalisés pour la page de contact */
</style>
