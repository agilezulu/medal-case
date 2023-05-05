<script setup>
const props = defineProps({
  className: String
})
</script>
<template>
  <img :src="`/img/${className}.png`" style="width: 100%;"/>
</template>
