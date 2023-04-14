<script setup>
import { medalStore } from "@/store";
import { storeToRefs } from "pinia";
import { metersToDistanceUnits, getDate, secsToHMS } from "@/utils/helpers.js";

const { athleteList, loading } = storeToRefs(medalStore())
const { getAthletes } = medalStore();

getAthletes();
</script>

<template>
  <div class="greetings">
    <h1 class="green">Athletes</h1>
    <div>Welcome</div>
    <div v-show="loading">Loading...</div>
    <div v-for="athlete in athleteList" :key="athlete.uuid">
      <router-link :to="{ name: 'athlete', params: { slug: athlete.slug } }">{{athlete.firstname}} {{athlete.lastname}}</router-link>
    </div>

  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

</style>
