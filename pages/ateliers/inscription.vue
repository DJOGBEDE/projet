<template>
  <v-app>
    <v-main>
      <v-container class="fill-height d-flex align-center justify-center" fluid>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="headline">Inscription Atelier</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="submitForm">
                  <v-text-field
                    v-model="workshop.name"
                    label="Nom de l'atelier"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.address"
                    label="Adresse"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.phone"
                    label="Numéro de téléphone"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.email"
                    label="Adresse e-mail"
                    type="email"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.website"
                    label="Site web (si disponible)"
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.password"
                    label="Mot de passe"
                    type="password"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.confirmPassword"
                    label="Confirmer le mot de passe"
                    type="password"
                    required
                  ></v-text-field>
                  <v-btn color="primary" class="white--text" type="submit">S'inscrire</v-btn>
                  <v-btn @click="$router.push('/ateliers/connection')" class="white--text mt-4" block>J'ai un compte ?</v-btn>
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
import axios from 'axios'; // N'oubliez pas d'importer axios

export default {
  data() {
    return {
      workshop: {
        name: '',
        address: '',
        phone: '',
        email: '',
        website: '',
        password: '',
        confirmPassword: ''
      }
    };
  },
  methods: {
    async submitForm() {
  try {
    console.log('Mot de passe:', this.workshop.password);
    console.log('Confirmer le mot de passe:', this.workshop.confirmPassword);
    
    if (this.workshop.password.trim() !== this.workshop.confirmPassword.trim()) {
      throw new Error("Les mots de passe ne correspondent pas");
    }

    const response = await axios.post('http://localhost:8080/api/workshops', this.workshop);
    console.log('Formulaire soumis:', response.data);
    
    // Réinitialiser le formulaire après soumission
    this.workshop.name = '';
    this.workshop.address = '';
    this.workshop.phone = '';
    this.workshop.email = '';
    this.workshop.website = '';
    this.workshop.password = '';
    this.workshop.confirmPassword = '';
    this.$router.push('/users/connection'); // Redirection après succès
  } catch (error) {
    console.error('Erreur lors de la soumission du formulaire:', error);
  }
}

  }
};
</script>
