<script setup>
import Popper from "vue3-popper";

</script>
<template>
    <Popper arrow hover placement="left">
        <slot />
        <template #content>
            <div v-html="$attrs.content"></div>
        </template>
    </Popper>
</template>
