<template>
    <div class="success-container">
      <h2>Paiement réussi !</h2>
      <p>Merci pour votre paiement.</p>
    </div>
  </template>
  
  <script>
  export default {
    mounted() {
      const queryParams = this.$route.query;
      // Ici, tu peux gérer le traitement des données reçues après paiement
      console.log('Détails du paiement:', queryParams);
    },
  };
  </script>
  
  <style scoped>
  .success-container {
    text-align: center;
    padding: 50px;
  }
  </style>
  