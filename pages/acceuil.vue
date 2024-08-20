<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Notre Application</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/connection')">Connexion</v-btn>
        <v-btn text @click="$router.push('/users/inscription')">Inscription Utilisateur</v-btn>
        <v-btn text @click="$router.push('/ateliers/inscription')">Inscription Atelier</v-btn>
        <v-btn text @click="$router.push('/contacts')">Nous Contacter</v-btn>
        <v-btn text @click="$router.push('/about')">En Savoir Plus</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <!-- Section de présentation -->
        <v-row class="my-12">
          <v-col cols="12" class="text-center">
            <transition name="fade">
              <div>
                <h1 class="display-1 font-weight-bold">Bienvenue sur Notre Application</h1>
                <p class="subtitle-1">Découvrez les meilleurs ateliers de mécanique près de chez vous.</p>
              </div>
            </transition>
          </v-col>
        </v-row>

        <!-- Section avec photos et description -->
        <v-row>
          <v-col cols="12" md="4">
            <transition name="fade">
              <v-img src="/home/delkael/Téléchargements/projet2/mecano_project/public/V6.jpg"></v-img>
            </transition>
          </v-col>
          <v-col cols="12" md="8">
            <transition name="slide-fade">
              <div>
                <h2 class="headline">Notre Vision</h2>
                <p>Nous visons à faciliter la vie des automobilistes en leur offrant un accès rapide et facile aux meilleurs ateliers de mécanique de leur région.</p>
              </div>
            </transition>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="8">
            <transition name="slide-fade">
              <div>
                <h2 class="headline">Nos Services</h2>
                <p>Nous proposons une plateforme où les ateliers peuvent s'inscrire et offrir leurs services. Les utilisateurs peuvent facilement trouver, contacter, et prendre rendez-vous avec des ateliers proches de chez eux.</p>
              </div>
            </transition>
          </v-col>
          <v-col cols="12" md="4">
            <transition name="fade">
              <v-img src="/home/delkael/Téléchargements/projet2/mecano_project/public/v5.jpg"></v-img>
            </transition>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="4">
            <transition name="fade">
              <v-img src="/home/delkael/Téléchargements/projet2/mecano_project/public/v7.jpg"></v-img>
            </transition>
          </v-col>
          <v-col cols="12" md="8">
            <transition name="slide-fade">
              <div>
                <h2 class="headline">Types de Services Offerts</h2>
                <ul>
                  <li>Réparation de moteur</li>
                  <li>Changement d'huile</li>
                  <li>Entretien des freins</li>
                  <li>Diagnostique électronique</li>
                  <li>Et bien plus encore...</li>
                </ul>
              </div>
            </transition>
          </v-col>
        </v-row>

        <!-- Section de contact -->
        <v-row class="my-12">
          <v-col cols="12" class="text-center">
            <transition name="fade">
              <div>
                <h2 class="headline">Contactez-nous</h2>
                <v-btn color="primary" class="white--text" @click="navigateTo('contacts')">Nous Contacter</v-btn>
              </div>
            </transition>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  methods: {
    navigateTo(page) {
      this.$router.push({ path: `/${page}` });
    }
  }
}
</script>

<style>
/* Styles des transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 5s ease;
}
.slide-fade-enter, .slide-fade-leave-to {
  transform: translateX(10px);
  opacity: 0;
}
</style>
