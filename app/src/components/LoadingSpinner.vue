<script setup>
import { OrbitSpinner } from "epic-spinners";
import MedalcaseLogoPulse from "@/components/icons/MedalcaseLogoPulse.vue";
</script>

<template>
    <div class="spinner-cont">
      <div class="spinnerbg add-spin"><MedalcaseLogoPulse border="#FD4B01" center="#ffffff" /></div>
      <orbit-spinner
          :animation-duration="1200"
          :size="155"
          color="#FD4B01"
      />
    </div>
</template>

<style lang="scss">

.spinner-cont {
  width: 155px;
  height: 155px;
  position: relative;
  .spinnerbg {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    padding: 45px;
  }
}
</style>
