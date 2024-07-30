<template>
  <v-app>
    <v-main>
      <v-container class="fill-height d-flex align-center justify-center" fluid>
        <v-row justify="center">
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title class="headline">Inscription Utilisateur</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="submitForm">
                  <v-text-field
                    v-model="user.name"
                    label="Nom"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="user.email"
                    label="Email"
                    type="email"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="user.password"
                    label="Mot de passe"
                    type="password"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="user.phone" 
                    label="Numéro de téléphone"
                    required
                  ></v-text-field>
                  <v-btn color="primary" class="white--text" type="submit">S'inscrire</v-btn>
                  <v-btn @click="$router.push('/users/connection')" class="white--text mt-4" block>J'ai un compte ?</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: {
        name: '',
        email: '',
        password: '',
        phone: ''  // Ajout du numéro de téléphone
      }
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post('http://localhost:8080/api/register', this.user);
        console.log('Formulaire soumis:', response.data);
        // Réinitialiser le formulaire après soumission
        this.user.name = '';
        this.user.email = '';
        this.user.password = '';
        this.user.phone = '';  // Réinitialiser le numéro de téléphone
        this.$router.push('/users/connection');
      } catch (error) {
        console.error('Erreur lors de la soumission du formulaire:', error);
      }
    }
  }
};
</script>

<style scoped>
.fill-height {
  min-height: 50vh; /* S'assure que le conteneur occupe toute la hauteur de la vue */
}
</style>
