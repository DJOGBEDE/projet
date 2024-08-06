import 'leaflet/dist/leaflet.css';

export default defineNuxtPlugin(async (nuxtApp) => {
    // Charger Leaflet uniquement côté client
    if (process.client) {
        const L = await import('leaflet');

        // Supprimer les icônes par défaut pour qu'elles fonctionnent correctement
        delete L.Icon.Default.prototype._getIconUrl;
        L.Icon.Default.mergeOptions({
            iconRetinaUrl: 'https://unpkg.com/leaflet/dist/images/marker-icon-2x.png',
            iconUrl: 'https://unpkg.com/leaflet/dist/images/marker-icon.png',
            shadowUrl: 'https://unpkg.com/leaflet/dist/images/marker-shadow.png',
        });

        nuxtApp.provide('leaflet', L);
    }
});
