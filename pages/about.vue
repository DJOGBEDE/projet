<template>
    <v-app>
      <v-main>
        <v-container fluid>
          <!-- Introduction -->
          <v-parallax
            src="/home/delkael/Téléchargements/projet2/mecano_project/public/v9.jpg"
            height="500"
          >
            <v-row class="fill-height" align="center" justify="center">
              <v-col class="text-center">
                <h1 class="display-2 white--text">En Savoir Plus</h1>
                <p class="headline white--text">Découvrez notre application et nos services</p>
              </v-col>
            </v-row>
          </v-parallax>
  
          <!-- Vision -->
          <v-row class="my-5">
            <v-col cols="12" md="6">
              <v-card class="elevation-2">
                <v-img
                  src="/home/delkael/Téléchargements/projet2/mecano_project/public/v10.jpg"
                  height="300px"
                  class="white--text align-end"
                  gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                >
                  <v-card-title>Notre Vision</v-card-title>
                </v-img>
                <v-card-text>
                  <p>
                    Notre vision est de rendre le processus de recherche et de prise de rendez-vous avec des ateliers de mécanique aussi simple et efficace que possible. Nous croyons en l'innovation et en la technologie pour améliorer la qualité des services et la satisfaction des clients.
                  </p>
                </v-card-text>
              </v-card>
            </v-col>
  
            <!-- Services -->
            <v-col cols="12" md="6">
              <v-card class="elevation-2">
                <v-img
                  src="/home/delkael/Téléchargements/projet2/mecano_project/public/v11.jpg"
                  height="300px"
                  class="white--text align-end"
                  gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                >
                  <v-card-title>Nos Services</v-card-title>
                </v-img>
                <v-card-text>
                  <p>
                    Nous offrons une plateforme conviviale qui permet aux clients de trouver facilement des ateliers de mécanique près de chez eux, de contacter ces ateliers, et de prendre rendez-vous directement. Nos services incluent :
                  </p>
                  <ul>
                    <li>Recherche d'ateliers par localisation</li>
                    <li>Prise de rendez-vous en ligne</li>
                    <li>Contact direct avec les ateliers</li>
                  </ul>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Témoignages -->
          <v-row class="my-5">
            <v-col cols="12">
              <v-card class="elevation-2">
                <v-card-title>Témoignages</v-card-title>
                <v-card-text>
                  <v-carousel>
                    <v-carousel-item v-for="(testimonial, i) in testimonials" :key="i">
                      <v-row>
                        <v-col cols="12" md="8" class="mx-auto">
                          <v-card class="pa-4">
                            <v-card-text class="text-center">
                              <v-avatar size="80" class="mx-auto mb-4">
                                <img :src="testimonial.avatar">
                              </v-avatar>
                              <div>{{ testimonial.name }}</div>
                              <div class="font-italic">"{{ testimonial.message }}"</div>
                            </v-card-text>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-carousel-item>
                  </v-carousel>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Contact -->
          <v-row class="my-5 ">
            <v-col cols="12">
              <v-card class="elevation-2">
                <v-card-title>Contactez-Nous</v-card-title>
                <v-card-text>
                  <p>
                    Si vous avez des questions ou souhaitez en savoir plus, n'hésitez pas à <v-btn class="ml-4" @click="$router.push('/contacts')">nous contacter</v-btn>.
                  </p>
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
  
  const testimonials = ref([
    {
      name: 'Jean Dupont',
      message: 'Une plateforme très pratique qui m\'a permis de trouver un atelier rapidement et de prendre rendez-vous en quelques clics.',
      avatar: 'https://via.placeholder.com/80'
    },
    {
      name: 'Marie Martin',
      message: 'Je recommande vivement cette application pour sa facilité d\'utilisation et son service client réactif.',
      avatar: 'https://via.placeholder.com/80'
    },
    {
      name: 'Jean Dupont',
      message: 'Une plateforme très pratique qui m\'a permis de trouver un atelier rapidement et de prendre rendez-vous en quelques clics.',
      avatar: 'https://via.placeholder.com/80'
    },
    {
      name: 'Marie Martin',
      message: 'Je recommande vivement cette application pour sa facilité d\'utilisation et son service client réactif.',
      avatar: 'https://via.placeholder.com/80'
    },
    {
      name: 'Jean Dupont',
      message: 'Une plateforme très pratique qui m\'a permis de trouver un atelier rapidement et de prendre rendez-vous en quelques clics.',
      avatar: 'https://via.placeholder.com/80'
    },
    {
      name: 'Marie Martin',
      message: 'Je recommande vivement cette application pour sa facilité d\'utilisation et son service client réactif.',
      avatar: 'https://via.placeholder.com/80'
    }
  ])
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page "En savoir plus" */
  .my-5 {
    margin-top: 3rem !important;
    margin-bottom: 3rem !important;
  }
  </style>
  