<script setup>
const props = defineProps({
  border: String,
  center: String
})
</script>
<template>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1332.14 1332.14">
    <svg:style type="text/css">
      <![CDATA[
      .hue {
        fill: #FD4B01;
        animation: pulse 10s infinite;
      animation-timing-function: ease-in-out;
      -webkit-animation: pulse 10s infinite;
      }
      @keyframes pulse {
        0%   { fill: #FD4B01 }
        50%  { fill: #ffffff }
        100% { fill: #FD4B01 }
      }
      @-webkit-keyframes pulse {
        0%   { fill: #FD4B01 }
        50%  { fill: #ffffff }
        100% { fill: #FD4B01 }
      }
      ]]>
    </svg:style>
    <path :fill="border" d="m666.07,70.83l503.25,298.97v600.04l-503.25,298.97-503.25-298.97V369.8L666.07,70.83m0-48.85L120.82,345.9v647.84l545.25,323.92,545.25-323.92V345.9L666.07,21.98h0Z"/>
    <polygon class="hue" points="1102.64 929.74 1102.64 411.03 666.07 151.67 229.5 411.03 229.5 929.74 666.07 1189.09 1102.64 929.74"/></svg>
</template>
