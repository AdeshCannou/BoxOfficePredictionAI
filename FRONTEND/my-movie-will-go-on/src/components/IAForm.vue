<template>
  <v-form
    style="width: 100¨%; height: 100%"
    class="d-flex flex-row justify-space-between flex-wrap"
  >
    <div
      style="height: calc(50% - 8px); width: calc(100% / 3 - 3px)"
      class="d-flex flex-column align-center text-center"
    >
      Acteurs
      <v-autocomplete
        v-model="selectedActor"
        label="Acteurs"
        :items="actors"
        append-icon="mdi-chevron-down"
        clearable
        clear-icon="mdi-close-circle-outline"
        multiple
        outlined
        menu-props="offset-y"
      >
        <template v-slot:selection="{ item, index }">
          <v-chip
            @click:close="
              selectedActor = selectedActor.filter((d) => d !== item)
            "
            close
            :close-icon="'mdi-close-circle'"
            style="font-size: 12px; height: 24px; max-width: calc(90% - 25px)"
            v-if="index < 1"
          >
            <span style="max-width: 90%; overflow: hidden">{{ item }}</span>
          </v-chip>

          <span
            v-if="index === 1"
            class="text-grey text-caption align-self-center"
          >
            (+{{ selectedActor.length - 1 }})
          </span>
        </template>
      </v-autocomplete>
    </div>
    <div
      style="height: calc(50% - 8px); width: calc(100% / 3 - 3px)"
      class="d-flex flex-column align-center text-center"
    >
      Directeurs
      <v-autocomplete
        v-model="selectedDirecteur"
        label="Directeur"
        :items="directeurs"
        append-icon="mdi-chevron-down"
        clearable
        clear-icon="mdi-close-circle-outline"
        multiple
        outlined
        menu-props="offset-y"
      >
        <template v-slot:selection="{ item, index }">
          <v-chip
            @click:close="
              selectedDirecteur = selectedDirecteur.filter((d) => d !== item)
            "
            close
            :close-icon="'mdi-close-circle'"
            style="font-size: 12px; height: 24px; max-width: calc(90% - 25px)"
            v-if="index < 1"
          >
            <span style="max-width: 90%; overflow: hidden">{{ item }}</span>
          </v-chip>

          <span
            v-if="index === 1"
            class="text-grey text-caption align-self-center"
          >
            (+{{ selectedDirecteur.length - 1 }})
          </span>
        </template>
      </v-autocomplete>
    </div>
    <div
      style="height: calc(50% - 8px); width: calc(100% / 3 - 3px)"
      class="d-flex flex-column align-center text-center"
    >
      Temps (min)
      <v-text-field
        outlined
        type="number"
        v-model="selectedTemps"
      ></v-text-field>
    </div>
    <div
      style="height: calc(50% - 8px); width: calc(100% / 3 - 3px)"
      class="d-flex flex-column align-center text-center"
    >
      Genres
      <v-autocomplete
        v-model="selectedGenre"
        label="Genres"
        :items="genres"
        append-icon="mdi-chevron-down"
        clearable
        clear-icon="mdi-close-circle-outline"
        multiple
        outlined
        menu-props="offset-y"
      >
        <template v-slot:selection="{ item, index }">
          <v-chip
            @click:close="
              selectedGenre = selectedGenre.filter((d) => d !== item)
            "
            close
            :close-icon="'mdi-close-circle'"
            style="font-size: 12px; height: 24px; max-width: calc(90% - 25px)"
            v-if="index < 1"
          >
            <span style="max-width: 90%; overflow: hidden">{{ item }}</span>
          </v-chip>

          <span
            v-if="index === 1"
            class="text-grey text-caption align-self-center"
          >
            (+{{ selectedGenre.length - 1 }})
          </span>
        </template>
      </v-autocomplete>
    </div>
    <div
      style="height: calc(50% - 8px); width: calc(100% / 3 - 3px)"
      class="d-flex flex-column align-center text-center"
    >
      Companies
      <v-autocomplete
        v-model="selectedCompanie"
        label="Companies"
        :items="companies"
        append-icon="mdi-chevron-down"
        clearable
        clear-icon="mdi-close-circle-outline"
        multiple
        outlined
        menu-props="offset-y"
      >
        <template v-slot:selection="{ item, index }">
          <v-chip
            @click:close="
              selectedCompanie = selectedCompanie.filter((d) => d !== item)
            "
            close
            :close-icon="'mdi-close-circle'"
            style="font-size: 12px; height: 24px; max-width: calc(90% - 25px)"
            v-if="index < 1"
          >
            <span style="max-width: 90%; overflow: hidden">{{ item }}</span>
          </v-chip>

          <span
            v-if="index === 1"
            class="text-grey text-caption align-self-center"
          >
            (+{{ selectedCompanie.length - 1 }})
          </span>
        </template>
      </v-autocomplete>
    </div>
    <div
      style="height: calc(50% - 8px); width: calc(100% / 3 - 3px)"
      class="d-flex flex-column align-center text-center"
    >
      Budget ($)
      <v-text-field
        outlined
        type="number"
        v-model="selectedBudget"
      ></v-text-field>
    </div>
  </v-form>
</template>

<script>
import { db } from "../../db.js";
export default {
  name: "ia-form",

  props: {
    value: {
      type: Object,
      default: () => ({}),
    },
  },

  data: () => ({
    selectedActor: [],
    selectedDirecteur: [],
    selectedTemps: 0,
    selectedGenre: [],
    selectedCompanie: [],
    selectedBudget: 0,

    actors: db.cast,
    directeurs: db.director,
    genres: db.genres,
    companies: db.production_companies,
  }),

  watch: {
    selectedActor(newVal) {
      this.$emit("input", { ...this.value, cast: newVal });
    },
    selectedDirecteur(newVal) {
      this.$emit("input", { ...this.value, director: newVal });
    },
    selectedTemps(newVal) {
      this.$emit("input", { ...this.value, runtime: parseInt(newVal) });
    },
    selectedGenre(newVal) {
      this.$emit("input", { ...this.value, genres: newVal });
    },
    selectedCompanie(newVal) {
      this.$emit("input", { ...this.value, production_companies: newVal });
    },
    selectedBudget(newVal) {
      this.$emit("input", { ...this.value, budget_adj: parseInt(newVal) });
    },
  },
};
</script>

<style></style>
