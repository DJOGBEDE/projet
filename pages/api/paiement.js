import { defineEventHandler, readBody } from 'h3'
import axios from 'axios'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { montant, description, email, telephone } = body

  // Remplacez par vos informations d'API CinetPay
  const apiKey = '1519658666d9e16f2c0819.57979115'
  const siteId = '5879320'
  const transactionId = Date.now().toString() // Générer un ID unique pour chaque transaction

  const data = {
    amount: montant,
    currency: 'XOF', // Devise utilisée, ici Franc CFA
    description: description,
    email: email,
    phone_number: telephone,
    transaction_id: transactionId,
    site_id: siteId,
    notify_url: 'https://votre-site.com/notify', // URL de notification (à remplacer)
    return_url: 'https://votre-site.com/thankyou', // URL de retour après paiement (à remplacer)
  }

  try {
    const response = await axios.post('https://api.cinetpay.com/v1/payment', data, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
    })

    // Vérifier la réponse de l'API CinetPay
    if (response.data.code === '201') {
      return {
        success: true,
        paymentUrl: response.data.data.payment_url, // URL de paiement renvoyée par CinetPay
      }
    } else {
      return {
        success: false,
        message: response.data.message || 'Erreur lors de la création du paiement.',
      }
    }
  } catch (error) {
    console.error('Erreur API:', error.response?.data || error.message) // Log d'erreur complet
    return {
      success: false,
      message: error.response?.data?.message || 'Erreur lors de la connexion à CinetPay.',
    }
  }
})
