<script setup>
import { medalStore } from "@/store";
import { STRAVA_OAUTH_URL } from "@/store";
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
  <div class="strava-auth" v-if="!store.isLoggedIn || show">
    <Button
      @click="login"
      class="p-button-outlined p-button-secondary"
      style="padding: 0"
    >
      <img src="@/assets/connect_with_strava.svg" />
    </Button>
  </div>
  <div v-else>
    <Button
        @click="store.doLogout()"
        class="p-button-outlined p-button-secondary p-button-sm"
        label="Log out"
        icon="pi pi-power-off"
        iconPos="right"
        v-if="store.isLoggedIn"
    />
  </div>
</template>
<style lang="scss">
.strava-auth {
  display: inline-block;
}
</style>
