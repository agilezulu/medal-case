<script setup>
const props = defineProps({
  border: String,
  center: String
})
</script>
<template>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1117.1 1333.2">
      <path :fill="border" d="M558.5,67.7l503.3,299v600l-503.3,299l-503.2-299v-600L558.5,67.7 M558.5,18.8L13.3,342.7v647.8l545.2,323.9
	l545.3-323.9V342.7L558.5,18.8L558.5,18.8z"/>
      <polygon :fill="center" points="995.1,925.9 995.1,407.2 558.6,147.8 122,407.2 122,925.9 558.6,1185.3 "/>
  </svg>
</template>
