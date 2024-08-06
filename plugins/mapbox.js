// ~/plugins/mapbox.js
import mapboxgl from 'mapbox-gl';

export default defineNuxtPlugin((nuxtApp) => {
  mapboxgl.accessToken = 'YOUR_MAPBOX_ACCESS_TOKEN';
  nuxtApp.provide('mapbox', mapboxgl);
});
