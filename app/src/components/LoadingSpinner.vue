<script setup>
import { OrbitSpinner } from "epic-spinners";
</script>

<template>
  <div class="spinner-canvas">
    <orbit-spinner
        :animation-duration="1200"
        :size="155"
        color="#FD4B01"
    />
  </div>
</template>

<style scoped>
.spinner-canvas {
  position: fixed;
  background-color: #ffffff;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
</style>
