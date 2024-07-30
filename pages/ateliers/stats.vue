<template>
    <v-app>
        <v-app-bar app color="primary" dark>
      <v-toolbar-title>Paramètres</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="$router.push('/acceuil')">Acceuil</v-btn>
      <v-btn text @click="$router.push('/ateliers/profil')">Profil</v-btn>
      <v-btn text @click="$router.push('/ateliers/services')">Services</v-btn>
      <v-btn text @click="$router.push('/ateliers/rendezvous')">Rendez-vous</v-btn>
    
     
     
    </v-app-bar>
      <v-main>
        <v-container fluid>
          <!-- Statistiques des Rendez-vous -->
          <v-row class="mb-4">
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Statistiques des Rendez-vous</v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <bar-chart :data="appointmentsData" :options="chartOptions"></bar-chart>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-list>
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>Nombre total de rendez-vous</v-list-item-title>
                            <v-list-item-subtitle>{{ totalAppointments }}</v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>Taux de réservation</v-list-item-title>
                            <v-list-item-subtitle>{{ bookingRate }}%</v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                      </v-list>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
  
          <!-- Statistiques des Avis -->
          <v-row>
            <v-col cols="12">
              <v-card class="pa-4" outlined>
                <v-card-title>Statistiques des Avis</v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <pie-chart :data="reviewsData" :options="chartOptions"></pie-chart>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-list>
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>Note moyenne</v-list-item-title>
                            <v-list-item-subtitle>{{ averageRating }}</v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                        <v-list-item>
                          <v-list-item-content>
                            <v-list-item-title>Nombre d'avis</v-list-item-title>
                            <v-list-item-subtitle>{{ totalReviews }}</v-list-item-subtitle>
                          </v-list-item-content>
                        </v-list-item>
                      </v-list>
                    </v-col>
                  </v-row>
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
  import { Bar, Pie } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
    ArcElement,
  } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)
  
  // Composants pour les graphiques
  const BarChart = defineComponent({
    name: 'BarChart',
    components: {
      Bar
    },
    props: {
      data: {
        type: Object,
        required: true
      },
      options: {
        type: Object,
        required: true
      }
    },
    template: '<Bar :data="data" :options="options" />'
  })
  
  const PieChart = defineComponent({
    name: 'PieChart',
    components: {
      Pie
    },
    props: {
      data: {
        type: Object,
        required: true
      },
      options: {
        type: Object,
        required: true
      }
    },
    template: '<Pie :data="data" :options="options" />'
  })
  
  // Données fictives pour les statistiques des rendez-vous
  const totalAppointments = 150
  const bookingRate = 75
  const appointmentsData = ref({
    labels: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin'],
    datasets: [
      {
        label: 'Rendez-vous',
        backgroundColor: '#42A5F5',
        data: [30, 45, 28, 80, 60, 90]
      }
    ]
  })
  
  // Données fictives pour les statistiques des avis
  const totalReviews = 50
  const averageRating = 4.5
  const reviewsData = ref({
    labels: ['1 étoile', '2 étoiles', '3 étoiles', '4 étoiles', '5 étoiles'],
    datasets: [
      {
        label: 'Avis',
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
        data: [2, 4, 10, 20, 14]
      }
    ]
  })
  
  // Options de configuration pour les graphiques
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
  }
  </script>
  
  <style scoped>
  /* Styles personnalisés pour la page de visualisation des statistiques */
  </style>
  