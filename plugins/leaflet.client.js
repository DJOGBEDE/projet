import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default defineNuxtPlugin(() => {
  return {
    provide: {
      leafletMap: L, // Changer le nom ici
    },
  };
});
