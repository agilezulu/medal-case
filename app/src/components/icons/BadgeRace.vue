<script setup>
const props = defineProps({
  border: { type: String, default: 'currentColor' },
  center: { type: String, default: 'currentColor' },
  classname: { type: String, default: 'badge race' },
})
</script>
<template>
  <span :class="classname">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1332.14 1332.14">
      <path :fill="border"  d="m665.82,70.83l503.25,298.97v600.04l-503.25,298.97-503.25-298.97V369.8L665.82,70.83m0-48.85L120.57,345.9v647.84l545.25,323.92,545.25-323.92V345.9L665.82,21.98h0Z"/>
      <path :fill="center" d="m1121.29,400.73l-375.29,128.23-79.62-398.23-79.62,398.23-375.29-128.23,295.67,270-295.67,270,375.29-128.23,79.62,398.23,79.62-398.23,375.29,128.23-295.67-270,295.67-270Zm-375.42,411.53h-158.97s-79.48-141.53-79.48-141.53l79.48-141.53h158.97s79.48,141.53,79.48,141.53l-79.48,141.53Z"/>
    </svg>
  </span>
</template>
