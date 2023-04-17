<script setup>
import {onMounted} from "vue";
import {RouterLink, RouterView} from "vue-router";
import router from "@/router";
import {medalStore} from "@/store";
import LoginStrava from "@/components/LoginStrava.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import {storeToRefs} from "pinia";

const store = medalStore();
const { loading } = storeToRefs(medalStore());
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
      <router-link to="/" class="p-menuitem-link"><img src="/medalcase_logo.svg"> Medalcase</router-link>
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
  <div v-if="loading">
    <LoadingSpinner />
  </div>
  <div class="container">
    <div class="left-column"></div>
    <div class="center-column"><router-view></router-view></div>
    <div class="right-column"></div>
  </div>
  <div class="footer">
    <router-link to="/about" class="p-menuitem-link">About</router-link>
    <Toast/>
  </div>

</template>

<style lang="scss">
$page-width: 720px;
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  justify-content: space-between;
}
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.footer {
  min-height: 80px;
  background-color: #eeeeee;
  padding: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.left-column,
.right-column {
  flex-basis: calc((100% - $page-width)/2);
  max-width: calc((100% - $page-width)/2);
}

.center-column {
  flex-basis: $page-width;
  max-width: $page-width;
}

@media (max-width: 1024px) {
  .left-column,
  .right-column {
    flex-basis: 50%;
    max-width: 50%;
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
