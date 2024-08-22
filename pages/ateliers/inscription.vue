<template>
  <v-app>
    <v-main>
      <v-container class="fill-height d-flex align-center justify-center" fluid>
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="headline">Inscription Atelier</v-card-title>
              <v-card-text>
                <v-form @submit.prevent="submitForm" ref="form">
                  <v-text-field
                    v-model="workshop.name"
                    label="Nom de l'atelier"
                    :rules="[v => !!v || 'Le nom de l\'atelier est requis']"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.address"
                    label="Adresse"
                    :rules="[v => !!v || 'L\'adresse est requise']"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.phone"
                    label="Numéro de téléphone"
                    :rules="[v => !!v || 'Le numéro de téléphone est requis']"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.email"
                    label="Adresse e-mail"
                    type="email"
                    :rules="[v => !!v || 'L\'adresse e-mail est requise', v => /.+@.+\..+/.test(v) || 'Adresse e-mail invalide']"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.website"
                    label="Site web (si disponible)"
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.password"
                    :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="showPassword ? 'text' : 'password'"
                    @click:append="showPassword = !showPassword"
                    label="Mot de passe"
                    :rules="[v => !!v || 'Le mot de passe est requis', v => v.length >= 7 || 'Le mot de passe doit contenir au moins 7 caractères']"
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model="workshop.confirmPassword"
                    :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="showPassword ? 'text' : 'password'"
                    @click:append="showPassword = !showPassword"
                    label="Confirmer le mot de passe"
                    :rules="[v => !!v || 'La confirmation du mot de passe est requise', v => v === workshop.password || 'Les mots de passe ne correspondent pas']"
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
import axios from 'axios';

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
      },
      showPassword: false
    };
  },
  methods: {
    async submitForm() {
      const isValid = this.$refs.form.validate();
      if (!isValid) {
        return;
      }

      try {
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
        this.$router.push('/ateliers/connection'); // Redirection après succès
      } catch (error) {
        console.error('Erreur lors de la soumission du formulaire:', error);
      }
    }
  }
};
</script>
