<script setup>
import {onMounted} from "vue";
import { RouterLink, RouterView } from "vue-router";
import { medalStore } from "@/store";
import LoginStrava from "@/components/LoginStrava.vue";
const store = medalStore();
console.log(store.medalcase.athlete);
const items = [
  {
    label: "Athletes",
    icon: "pi pi-fw pi-bolt",
    to: "/",
  },
  {
    label: "Me",
    icon: "pi pi-fw pi-user",
    to: `/athlete/${store.medalcase.athlete.slug}`,
    visible: () => store.isLoggedIn,
  },
];
onMounted(() => {
  store.setAccess();
});
</script>

<template>
  <Menubar :model="items">
    <template #item="{ item }">
      <router-link
          :to="item.to"
          custom
          v-slot="{ href, navigate, isActive, isExactActive }"
      >
        <a
            :href="href"
            @click="navigate"
            class="p-menuitem-link"
            :class="{
              'active-link': isActive,
              'active-link-exact': isExactActive,
            }"
        ><i :class="item.icon"></i>{{ item.label }}</a
        >
      </router-link>
    </template>
    <template #end>
      <LoginStrava />
    </template>
  </Menubar>
  <router-view></router-view>
</template>

<style lang="scss">

</style>
