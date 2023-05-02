<script setup>
import { medalStore, STRAVA_OAUTH_URL } from "@/store";
const store = medalStore();

// eslint-disable-next-line no-undef
defineProps({
  show: {
    type: Boolean,
    required: false,
    default: false,
  },
});
const login = () => {
  window.location = STRAVA_OAUTH_URL;
};

</script>
<template>
  <template v-if="!store.isLoggedIn || show">
    <Button
      @click="login"
      class="p-button-outlined p-button-secondary"
      style="padding: 0"
    >
      <img src="@/assets/connect_with_strava.svg" />
    </Button>
  </template>
  <template v-else>
    <a href="javascript:void(0);"

       class="p-menuitem-link active-link active-link-exact"
        @click="store.doLogout()"
        v-if="store.isLoggedIn"
    >Log out &nbsp;<font-awesome-icon icon="fa-light fa-fw fa-arrow-right-from-bracket" /></a>
  </template>
</template>
<style lang="scss">

</style>
