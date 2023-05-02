<script setup>
import { computed } from"vue";
const props = defineProps({
  photo: String,
  size: Number
});

const hex2props = computed(() => {
  return {
    'height': props.size + "px",
    'width': (props.size/2) + "px"
  };
});
</script>
<template>
  <div class="a-photo hexagon " :style="hex2props"><div class="hexagon-in1"><div class="hexagon-in2" :style="`background-image: url('${photo}');`"></div></div></div>
</template>

<style lang="scss">
.a-photo {
  position: absolute;
}
.hexagon {
  overflow: hidden;
  visibility: hidden;
  -webkit-transform: rotate(120deg);
  -moz-transform: rotate(120deg);
  -ms-transform: rotate(120deg);
  -o-transform: rotate(120deg);
  transform: rotate(120deg);
}
.hexagon-in1 {
  overflow: hidden;
  width: 100%;
  height: 100%;
  -webkit-transform: rotate(-60deg);
  -moz-transform: rotate(-60deg);
  -ms-transform: rotate(-60deg);
  -o-transform: rotate(-60deg);
  transform: rotate(-60deg);
}
.hexagon-in2 {
  width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-position: 50%;
  visibility: visible;
  -webkit-transform: rotate(-60deg);
  -moz-transform: rotate(-60deg);
  -ms-transform: rotate(-60deg);
  -o-transform: rotate(-60deg);
  transform: rotate(-60deg);
  background-size: cover;
}

</style>
