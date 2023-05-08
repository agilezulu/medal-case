<script setup>
import { onMounted, ref } from "vue";
import {RouterLink, RouterView} from "vue-router";
import router from "@/router";
import {medalStore} from "@/store";
import LoginStrava from "@/components/LoginStrava.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
const store = medalStore();

const myProfile = () => {
  router.push({name: "me"});
  //router.push({ name: "athlete", params: { slug: store.loggedInAthlete.slug } });
}
onMounted(() => {
  store.setAccess();
});
</script>

<template>
  <Menubar>
    <template #start>
      <router-link to="/" class="p-menuitem-link"><img src="/medalcase_logo.svg"><span class="mcase-face" style="letter-spacing: 0.5px;">Medalcase</span></router-link>
    </template>
    <template #end>
      <ul role="menubar" tabindex="0" class="menu-end">
        <li id="link-me" class="p-menuitem" role="menuitem" aria-label="Me" aria-level="1" aria-setsize="1" aria-posinset="2">
          <div class="p-menuitem-content">
          <a href="javascript:void(0);"
              @click="myProfile()"
              class="p-menuitem-link active-link active-link-exact"
              v-if="store.isLoggedIn"
          >Me &nbsp;<font-awesome-icon icon="fa-light fa-fw fa-user"/>
          </a>
          </div>
        </li>
        <li id="link-strava" class="p-menuitem" role="menuitem" aria-label="Athletes" aria-level="1" aria-setsize="1" aria-posinset="3">
          <div class="p-menuitem-content">
          <LoginStrava />
          </div>
        </li>
      </ul>
    </template>
  </Menubar>
    <div id="app-body">
  <div class="container">
      <div v-if="store.loading" class="spinner-canvas">
        <LoadingSpinner />
      </div>
      <router-view></router-view>
  </div>
    </div>
  <div id="app-footer">
    <router-link to="/about" class="p-menuitem-link">About</router-link>
    <div class="pbs"><img src="/img/api_logo_pwrdBy_strava_horiz_light.svg" style="width: 138px;"></div>
    <Toast position="top-right">
      <template #message="slotProps">
        <div class="p-toast-message-text">
          <span class="p-toast-summary">{{slotProps.message.summary}}</span>
          <div class="p-toast-detail" v-html="slotProps.message.detail" />
        </div>
      </template>
    </Toast>
    <ConfirmDialog group="account">
        <template #message="slotProps">
            <div class="flex p-4 align-items-center">
                <i :class="slotProps.message.icon" class="action-color" style="font-size: 1.5rem"></i>
                <div class="pl-2" v-html="slotProps.message.message"></div>
            </div>
        </template>
    </ConfirmDialog>
  </div>

</template>

<style lang="scss">
@import "@/assets/variables.scss";

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  justify-content: space-between;
}
.p-menubar {
  box-shadow: 0 5px 5px rgba(0,0,0,0.3);
  z-index: 12;
}
.p-inputswitch.p-inputswitch-checked.btn-action .p-inputswitch-slider,
.p-inputswitch.p-inputswitch-checked.btn-action:not(.p-disabled):hover .p-inputswitch-slider {
  background: $color-action;
}

.p-button.btn-action,
.p-button.btn-action:enabled:hover {
  background: $color-action;
  border: 1px solid $color-action;
}

.container {
  flex: 1;
  display: flex;
  width: 100%;
}
#app-body {
  box-shadow: 0 5px 5px rgba(0,0,0,0.3);
  z-index: 10;
  flex: 1;
  display: flex;
}
#app-footer {
  z-index: 9;
  min-height: 80px;
  background-color: #eeeeee;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  .pbs {
    display: flex;
  }
}
.p-toast {
  .p-toast-message {
    .p-toast-message-content {
      .p-toast-summary {
        font-weight: 700;
        font-size: 1.2rem;
      }

      .p-toast-detail {

      }
    }
  }
}
.spinner-canvas {
  position: absolute;
  top: 0;
  left: 0;
  background-color: #ffffff;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.left-column,
.right-column {
  flex-basis: calc((100% - $page-width)/2);
  max-width: calc((100% - $page-width)/2);
  //background-color: #f5f5f5;
}

.center-column {
  flex-basis: $page-width;
  max-width: $page-width;
}

@media (max-width: 1024px) {
  .left-column,
  .right-column {
    display: none;
  }
  .center-column {
    flex-basis: 100%;
    max-width: 100%;
    padding: 0 12px;
  }
}
.p-menubar-start {
  display: flex;
  align-items: center;
  a {
    color: #495057;
  }
  img {
    width: 40px;
    height: 40px;
  }
}
.p-menubar-end {
  .menu-end {
    display: flex;
  }
}
</style>
