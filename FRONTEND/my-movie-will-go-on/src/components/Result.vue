<template>
  <div>
    <!--Dialog background-->
    <div v-show="value" class="dialog-background" @click="closeDialog"></div>

    <!--Dialog box to display the details of the tcket-->
    <v-card elevation="24" v-show="value" class="dialog-box">
      <v-card-title class="bold px-4 d-flex flex-row justify-space-around">
        <div>Résultat de la prédiction</div>
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text
        style="height: calc(100% - 130px)"
        class="d-flex flex-row overflow-y-auto overflow-x-hidden justify-space-around align-center"
      >
        <div
          style="width: calc(50% - 8px); font-weight: bold"
          class="d-flex flex-column align-center"
        >
          Revenue Estimé
          <div style="height: 80px" class="d-flex flex-row align-center">
            <div style="font-size: 5em">{{ displayMoney(result) }}</div>
          </div>
        </div>
        <div
          style="width: calc(50% - 8px); font-weight: bold"
          class="d-flex flex-column align-center"
        >
          <div>Rendement</div>
          <div style="height: 80px" class="d-flex flex-row align-center">
            <div
              style="font-size: 5em"
              :style="{
                color:
                  rendement <= 100
                    ? 'red'
                    : rendement >= 200
                    ? 'green'
                    : 'orange',
              }"
            >
              {{ rendement }}%
            </div>
          </div>
          <div class="d-flex flex-row" style="width: 100%">
            <div
              class="text-center"
              style="width: calc(100% / 3); height: 22px; background-color: red"
            >
              En perte
            </div>
            <div
              class="text-center"
              style="
                width: calc(100% / 3);
                height: 22px;
                background-color: orange;
              "
            ></div>
            <div
              class="text-center"
              style="
                width: calc(100% / 3);
                height: 22px;
                background-color: green;
              "
            >
              Rentable
            </div>
          </div>
        </div>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-4" style="height: 64px">
        <v-spacer></v-spacer>
        <v-btn @click="closeDialog" color="blue darken-4" text class="bold">
          FERMER
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "result-dialog",

  props: {
    value: {
      type: Boolean,
      default: false,
    },

    result: {
      type: Number,
      default: 0,
    },

    budget: {
      type: Number,
      default: 1,
    },
  },

  computed: {
    rendement() {
      return Math.round((this.result / this.budget) * 100);
    },
  },

  methods: {
    closeDialog() {
      this.$emit("input", false);
    },
    displayMoney(val) {
      return `${val.toLocaleString()} $`;
    },
  },
};
</script>

<style>
.dialog-background {
  position: fixed;
  width: 3000px;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.1);
}

.dialog-box {
  position: absolute;
  width: 85%;
  height: calc(100% - 120px);
  top: 70px;
  left: 7.5%;
}
</style>
