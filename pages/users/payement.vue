<template>
    <v-app>
      <v-container fluid>
        <v-row>
          <v-col cols="12" md="6">
            <v-card class="pa-4" outlined>
              <v-card-title>
                <v-img
                  src="https://via.placeholder.com/400x200" 
                  height="200"
                  width="100%"
                  class="mb-3"
                ></v-img>
              </v-card-title>
              <v-card-subtitle class="headline">Détails du service</v-card-subtitle>
              <v-card-text>
                <p><strong>Nom du service:</strong> Service de Mécanique</p>
                <p><strong>Prix:</strong> 1000 FCFA</p>
                <p><strong>Description:</strong> Un service complet pour votre véhicule.</p>
              </v-card-text>
  
              <v-divider></v-divider>
  
              <v-card-subtitle class="headline mt-3">Moyens de paiement</v-card-subtitle>
              <v-card-text>
                <v-radio-group v-model="selectedPaymentMethod">
                  <v-radio label="Carte de crédit" value="credit_card"></v-radio>
                  <v-radio label="PayPal" value="paypal"></v-radio>
                  <v-radio label="Mobile Money" value="mobile_money"></v-radio>
                  <v-radio label="Virement bancaire" value="bank_transfer"></v-radio>
                </v-radio-group>
              </v-card-text>
  
              <v-divider></v-divider>
  
              <v-card-subtitle class="headline mt-3">Informations de paiement</v-card-subtitle>
              <v-card-text>
                <v-text-field
                  v-if="selectedPaymentMethod === 'credit_card'"
                  label="Numéro de carte"
                  v-model="cardNumber"
                  required
                ></v-text-field>
                <v-text-field
                  v-if="selectedPaymentMethod === 'credit_card'"
                  label="Date d'expiration (MM/AA)"
                  v-model="expiryDate"
                  required
                ></v-text-field>
                <v-text-field
                  v-if="selectedPaymentMethod === 'credit_card'"
                  label="CVV"
                  v-model="cvv"
                  required
                  type="password"
                ></v-text-field>
                <v-text-field
                  v-if="selectedPaymentMethod === 'paypal'"
                  label="Email PayPal"
                  v-model="paypalEmail"
                  required
                ></v-text-field>
                <v-text-field
                  v-if="selectedPaymentMethod === 'mobile_money'"
                  label="Numéro de téléphone"
                  v-model="mobileNumber"
                  required
                ></v-text-field>
                <v-text-field
                  v-if="selectedPaymentMethod === 'bank_transfer'"
                  label="Nom de la banque"
                  v-model="bankName"
                  required
                ></v-text-field>
                <v-text-field
                  v-if="selectedPaymentMethod === 'bank_transfer'"
                  label="Numéro de compte"
                  v-model="accountNumber"
                  required
                ></v-text-field>
              </v-card-text>
  
              <v-divider></v-divider>
  
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="confirmPayment">Confirmer le paiement</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
  
      <v-dialog v-model="paymentDialog" max-width="500">
        <v-card>
          <v-card-title class="headline">Confirmation de paiement</v-card-title>
          <v-card-text>
            Votre paiement a été effectué avec succès !
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="paymentDialog = false">Fermer</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  // Variables réactives
  const selectedPaymentMethod = ref(null)
  const cardNumber = ref('')
  const expiryDate = ref('')
  const cvv = ref('')
  const paypalEmail = ref('')
  const mobileNumber = ref('')
  const bankName = ref('')
  const accountNumber = ref('')
  const paymentDialog = ref(false)
  
  // Fonction pour confirmer le paiement
  function confirmPayment() {
    // Logique pour traiter le paiement ici
  
    // Afficher le dialogue de confirmation
    paymentDialog.value = true
  }
  </script>
  
  <style scoped>
  /* Ajoutez vos styles ici */
  </style>
  