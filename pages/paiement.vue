<template>
  <div class="home">
    <!-- Bouton pour afficher la carte de paiement -->
    <button @click="showPaymentForm = true" class="pay-button">Payer</button>

    <!-- v-card pour entrer le montant et procéder au paiement -->
    <div v-if="showPaymentForm" class="payment-card">
      <div class="card-content">
        <h3>Entrer le montant</h3>
        <input v-model="amount" type="number" placeholder="Montant en CFA" class="amount-input" />

        <button @click="open" class="proceed-button">Passer au paiement</button>
        <button @click="closeForm" class="cancel-button">Annuler</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Importer les hooks de Nuxt 3
import { ref, onMounted, onBeforeUnmount } from 'vue';

// Variables réactives
const amount = ref(0); // Montant par défaut
const showPaymentForm = ref(false); // Contrôle de l'affichage de la v-card
const openKkiapayWidget = ref(null);
const removeKkiapayListener = ref(null);

// Fonction pour ouvrir le widget de paiement
const open = () => {
  if (openKkiapayWidget.value && amount.value > 0) {
    openKkiapayWidget.value({
      amount: amount.value, // Utiliser le montant entré par l'utilisateur
      api_key: 'a4d592906e9411ef94e0cb57a5c3525f', // Clé publique API
      sandbox: true, // Activer le mode test
      phone: '97000000', // Numéro de téléphone du client
    });
    // Fermer le formulaire une fois le paiement ouvert
    showPaymentForm.value = false;
  } else {
    alert('Veuillez entrer un montant valide');
  }
};

// Fonction pour fermer la carte de paiement
const closeForm = () => {
  showPaymentForm.value = false;
};

// Fonction de gestion du succès
const successHandler = (response) => {
  console.log('Paiement réussi :', response);
};

// Charger le widget au montage du composant
onMounted(async () => {
  const { openKkiapayWidget: openWidget, addKkiapayListener, removeKkiapayListener: removeListener } = await import('kkiapay');
  
  openKkiapayWidget.value = openWidget;
  removeKkiapayListener.value = removeListener;
  
  // Ajouter un listener pour le succès des transactions
  addKkiapayListener('success', successHandler);
});

// Nettoyage avant la destruction du composant
onBeforeUnmount(() => {
  if (removeKkiapayListener.value) {
    removeKkiapayListener.value('success', successHandler);
  }
});
</script>

<style scoped>
/* Styles généraux */
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f4f4;
}

/* Bouton principal pour déclencher le formulaire de paiement */
.pay-button {
  padding: 15px 30px;
  background-color: #0095ff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pay-button:hover {
  background-color: #007acc;
}

/* Styles pour la v-card */
.payment-card {
  background-color: white;
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  padding: 20px;
  max-width: 400px;
  width: 100%;
  margin: 20px;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

h3 {
  margin-bottom: 15px;
  font-size: 22px;
  color: #333;
}

.amount-input {
  padding: 10px;
  font-size: 16px;
  width: 100%;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

/* Boutons dans la v-card */
.proceed-button {
  padding: 12px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 10px;
}

.proceed-button:hover {
  background-color: #218838;
}

.cancel-button {
  padding: 12px 20px;
  background-color: #ff3860;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.cancel-button:hover {
  background-color: #e01e37;
}
</style>
