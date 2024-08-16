<template>
  <div>
    <h1>Liste des Ateliers</h1>
    <v-data-table
      :headers="headers"
      :items="workshops"
      item-key="id"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Ateliers</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="openDialog">Ajouter Atelier</v-btn>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon @click="editWorkshop(item)">mdi-pencil</v-icon>
        <v-icon @click="deleteWorkshop(item.id)">mdi-delete</v-icon>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ form.id ? 'Modifier' : 'Ajouter' }} Atelier</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="form.name"
              :rules="nameRules"
              label="Nom"
              required
            ></v-text-field>
            <v-text-field
              v-model="form.address"
              :rules="addressRules"
              label="Adresse"
              required
            ></v-text-field>
            <v-text-field
              v-model="form.phone_number"
              :rules="phoneRules"
              label="Numéro de Téléphone"
              required
            ></v-text-field>
            <v-text-field
              v-model="form.email"
              :rules="emailRules"
              label="Email"
              required
            ></v-text-field>
            <v-text-field
              v-model="form.website"
              label="Site Web"
            ></v-text-field>
            <v-text-field
              v-model="form.opening_hours"
              label="Horaires d'Ouverture"
            ></v-text-field>
            <v-text-field
              v-model="form.latitude"
              label="Latitude"
            ></v-text-field>
            <v-text-field
              v-model="form.longitude"
              label="Longitude"
            ></v-text-field>
            <v-text-field
              v-model="form.photo"
              label="Photo"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="closeDialog">Annuler</v-btn>
          <v-btn color="blue darken-1" text @click="saveWorkshop">Enregistrer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        { text: 'Nom', value: 'name' },
        { text: 'Adresse', value: 'address' },
        { text: 'Numéro de Téléphone', value: 'phone_number' },
        { text: 'Email', value: 'email' },
        { text: 'Site Web', value: 'website' },
        { text: 'Horaires', value: 'opening_hours' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      workshops: [],
      dialog: false,
      valid: true,
      form: {
        id: null,
        name: '',
        address: '',
        phone_number: '',
        email: '',
        website: '',
        opening_hours: '',
        latitude: '',
        longitude: '',
        photo: '',
      },
      nameRules: [v => !!v || 'Nom est requis'],
      addressRules: [v => !!v || 'Adresse est requise'],
      phoneRules: [v => !!v || 'Numéro de téléphone est requis'],
      emailRules: [v => !!v || 'Email est requis'],
    };
  },
  methods: {
    async fetchWorkshops() {
      try {
        const response = await this.$axios.get('/api/workshops');
        this.workshops = response.data;
      } catch (error) {
        console.error('Erreur lors de la récupération des ateliers:', error);
      }
    },
    openDialog() {
      this.form = {
        id: null,
        name: '',
        address: '',
        phone_number: '',
        email: '',
        website: '',
        opening_hours: '',
        latitude: '',
        longitude: '',
        photo: '',
      };
      this.dialog = true;
    },
    async saveWorkshop() {
      if (this.$refs.form.validate()) {
        try {
          if (this.form.id) {
            // Update existing workshop
            await this.$axios.put(`/api/workshops/${this.form.id}`, this.form);
          } else {
            // Add new workshop
            await this.$axios.post('/api/workshops', this.form);
          }
          this.fetchWorkshops();
          this.dialog = false;
        } catch (error) {
          console.error('Erreur lors de l\'enregistrement de l\'atelier:', error);
        }
      }
    },
    async editWorkshop(item) {
      this.form = { ...item };
      this.dialog = true;
    },
    async deleteWorkshop(id) {
      try {
        await this.$axios.delete(`/api/workshops/${id}`);
        this.fetchWorkshops();
      } catch (error) {
        console.error('Erreur lors de la suppression de l\'atelier:', error);
      }
    },
  },
  mounted() {
    this.fetchWorkshops();
  },
};
</script>
