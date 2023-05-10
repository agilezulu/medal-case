<script setup>
import { computed } from "vue";
import {elevationColor, elevationFromDistanceUnits} from "@/utils/helpers";
import {medalStore} from "@/store";
const store = medalStore();
const props = defineProps({
  run: {
    type: Object,
    required: true,
  }
});
const elevationScore = computed(() => {
  return Math.round((props.run.total_elevation_gain/props.run.distance)*1000);
});
const colorE = computed(() => {
  return elevationScore.value < 12 ? '#ffffff' : elevationScore.value < 35 ? '#777777' : '#ffffff';
});
</script>

<template>
  <span class="elev">
      {{ elevationFromDistanceUnits(run.total_elevation_gain, store.selectedUnits)}}
      <span class="elev-score" :style="`background-color: ${elevationColor(elevationScore)}; color: ${colorE}`"><font-awesome-icon icon="fa-sharp fa-light fa-mountain"  fixed-width />{{elevationScore}}</span>
  </span>
</template>

<style scoped lang="scss">
.elev-score {
  display: inline-block;
  width: 50px;
  color: #ffffff;
  line-height: 1;
  padding: 2px 0;
  font-weight: 500;
  border-radius: 15px;
  text-align: center;
}
</style>
