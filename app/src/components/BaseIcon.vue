<script setup>
import {computed} from "vue";

const icons = {
  logo: import('@/components/icons/MedalcaseLogo.vue'),
  // ...
}

const props = defineProps({
    name: {
      type: String,
      required: true,
      validator(value) {
        return Object.prototype.hasOwnProperty.call(this.icons, value)
      }
    }
  });


const iconComponent = computed(() => {
  return icons[this.name]
});


</script>
<template>
  <component
      :is="iconComponent"
      role="img"
      class="inline-block fill-current"
      style="height: 1em; width: 1em;"
  />
</template>

