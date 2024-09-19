<template>
  <div>
    <h1>Paiement avec CinetPay</h1>
    <button @click="checkout">Procéder au Paiement</button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

const checkout = () => {
  // Configuration du SDK CinetPay
  CinetPay.setConfig({
    apikey: '1519658666d9e16f2c0819.57979115', // Remplacez par votre clé API
    site_id: '5879320', // Remplacez par votre identifiant de site
    notify_url: 'http://localhost:8080/notify/', // URL de notification
    mode: 'PRODUCTION' // Mode de production ou test
  });

  // Fonction pour initier le paiement
  CinetPay.getCheckout({
    transaction_id: Math.floor(Math.random() * 100000000).toString(), // ID de transaction unique
    amount: 1000, // Montant à payer (en XOF)
    currency: 'XOF', // Devise
    channels: 'ALL', // Canaux de paiement
    description: 'Payement pour vos operations', // Description du paiement
    customer_name: "Nom", // Nom du client
    customer_surname: "Prénom", // Prénom du client
    customer_email: "client@example.com", // Email du client
    customer_phone_number: "+22954335162", // Numéro de téléphone du client
    customer_address: "Adresse", // Adresse du client
    customer_city: "Ville", // Ville du client
    customer_country: "BN", // Code ISO du pays
    customer_state: "BN", // Code ISO de l'état
    customer_zip_code: "06510" // Code postal
  });

  // Gestion de la réponse après le paiement
  CinetPay.waitResponse(function(data) {
    if (data.status === "ACCEPTED") {
      alert("Votre paiement a été effectué avec succès !");
      // Rediriger ou mettre à jour l'interface utilisateur ici
    } else if (data.status === "REFUSED") {
      alert("Votre paiement a échoué.");
    } else {
      alert("Statut de paiement inconnu : " + data.status);
    }
  });
}

// Charger le SDK CinetPay au montage du composant
onMounted(() => {
  const script = document.createElement('script');
  script.src = 'https://cdn.cinetpay.com/seamless/main.js';
  script.async = true;
  document.head.appendChild(script);
});
</script>

<style scoped>
/* Ajoutez vos styles ici */
</style>
