<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <h2>MY MOVIE WILL GO ON</h2>
      </div>

      <v-spacer></v-spacer>

      <v-btn @click="sendData" text>
        <span class="mr-2">Predict revenue</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <IAForm v-model="values"></IAForm>
      <result
        v-model="showDialog"
        :result="revenue"
        :budget="values.budget_adj"
      ></result>
    </v-main>
  </v-app>
</template>

<script>
import IAForm from "./components/IAForm.vue";
import Result from "./components/Result.vue";
import { HTTP } from "./plugins/axios.js";

export default {
  name: "App",

  components: {
    IAForm,
    Result,
  },

  data: () => ({
    revenue: 0,
    showDialog: false,
    values: {
      cast: [],
      director: [],
      runtime: 0,
      genres: [],
      production_companies: [],
      budget_adj: 0,
    },
  }),

  methods: {
    async sendData() {
      try {
        const result = await HTTP.post("/predict", JSON.stringify(this.values));
        this.revenue = Math.round(result.data.predicted_revenue);
        this.showDialog = true;
      } catch {
        alert(
          "Une erreur s'est produite: Veillez à bien renseignez vos champs"
        );
      }
    },
  },
};
</script>
