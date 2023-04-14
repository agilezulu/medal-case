<script setup>
import {onMounted} from "vue";
import { RouterLink, RouterView } from "vue-router";
import { medalStore } from "@/store";
import LoginStrava from "@/components/LoginStrava.vue";
import router from "@/router";
const store = medalStore();

const items =[
  {
    label: "Athletes",
    icon: "pi pi-fw pi-bolt",
    to: "/",
  },
];
const myProfile = () => {
  router.push({ name: "athlete", params: { slug: store.loggedInAthlete.slug } })
}
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
      <Button
          @click="myProfile()"
          class="p-button-outlined p-button-secondary p-button-sm"
          iconPos="right"
          v-if="store.isLoggedIn"
      >Me &nbsp;<font-awesome-icon icon="fa-light fa-fw fa-user" /></Button>
      <LoginStrava />
    </template>
  </Menubar>
  <router-view></router-view>
</template>

<style lang="scss">

</style>
