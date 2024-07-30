<template>
  <v-container class="fill-height d-flex align-center justify-center" fluid>
    <v-card class="pa-5" min-width="800">
      <v-card-title class="headline text-center">Connexion Atelier</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field label="Email" required></v-text-field>
          <v-text-field label="Mot de passe" type="password" required></v-text-field>
          <v-btn color="secondary" @click="$router.push('/ateliers/dashbord')" class="white--text" block>Se connecter</v-btn>
          <v-btn @click="$router.push('/users/mp')" color="blue" class="white--text mt-4 mb-4" block>Mots de passe oublié ?</v-btn>
          <v-btn @click="$router.push('/ateliers/inscription')" class="white--text" block>Je n'ai pas un compte ?</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  // Pas besoin de script pour cet exemple
}
</script>

<style>
/* Style optionnel */
</style>
