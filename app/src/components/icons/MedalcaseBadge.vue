<script setup>
const props = defineProps({
  className: String
})
</script>
<template>
  <img :src="`/img/${className}.png`" :alt="className" style="height: 103px;"/>
</template>
