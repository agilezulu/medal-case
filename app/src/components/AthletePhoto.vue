<script setup>
import { computed } from"vue";
const props = defineProps({
  photo: String,
  size: Number
});

const hex2props = computed(() => {
  return {
    'height': props.size + "px",
    'width': (props.size * (99/120)) + "px"
  };
});
</script>
<template>
    <div class="photo-logo" :style="hex2props">
        <div class="pl-bg"><img src="/medalcase_logo.svg" /></div>
        <div class="a-photo" :style="`background-image: url('${photo}');`"></div>
    </div>

</template>

<style lang="scss">
.photo-logo {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  .pl-bg {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
  }
  .a-photo {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 69%;
    height: 69%;
    transform: translate(-50%, -50%);
    background-repeat: no-repeat;
    background-position: 50%;
    background-size: cover;
    clip-path: polygon(0% 25%, 0% 75%, 50% 100%, 100% 75%, 100% 25%, 50% 0%);
  }
}

</style>
