<script setup>
import { onMounted, computed } from "vue";
import { SCOPES, medalStore } from "@/store";
import LoginStrava from "@/components/LoginStrava.vue";
import {useToast} from "primevue/usetoast";
const store = medalStore();
const toast = useToast();
const scopesDesc = {
  read: "general access access to read public data (segments, routes, profile, posts, events, feeds, leaderboards)",
  "profile:read_all":
    "read profile information to be able to create your Medalcase account",
  read_all: "access to prive data (routes, posts, etc)",
  "activity:read":
    "read activity data for activities that are visible to Everyone and Followers, excluding privacy zone data",
  "activity:read_all":
    "the same access as activity:read, plus privacy zone data and access to read the activities with visibility set to Only You",
};
let params = new URLSearchParams(window.location.search);
const gotScopes = params.get("scope").split(",");
const code = params.get("code");
const validatedScope = (scope) => {
  return gotScopes.indexOf(scope) > -1;
};

// check that we hav all requested scopes
const allValid = computed(() => {
  let valid = true;
  SCOPES.forEach((s) => {
    if (!validatedScope(s)) {
      valid = false;
      return false;
    }
  });
  return valid;
});
onMounted(() => {
  if (allValid.value) {
    console.log(`SCOPES OK -> ${code}`);
    store.getAccessTokenFromCode(code).then((response) => {
      console.log('getAccessTokenFromCode', response);
      if (response && response.error){
        toast.add({
          severity: 'error',
          summary: response.error.name,
          detail: response.error.description,
          life: 5000
        });
      }
    });
  } else {
    toast.add({
      severity: 'error',
      summary: "Missing authorisations",
      detail: "Some required Strava authorsations are missing",
      life: 5000
    });
    console.log("ERROR -> Missing scope(s)");
  }
});
</script>
<template>
  <div class="grid">
    <div class="col-1"></div>
    <div class="col-10">
      <div v-if="!allValid">
        <div>
          <p>
            In order for Streaks to function we need access to all permissions.
          </p>
        </div>
        <table>
          <tbody>
            <tr v-for="s in SCOPES" :key="s">
              <td
                class="scope-name"
                :class="validatedScope(s) ? 'valid' : 'missing'"
              >
                {{ s }}
              </td>
              <td
                class="scope-state"
                :class="validatedScope(s) ? 'valid' : 'missing'"
              >
                {{ validatedScope(s) ? "OK" : "missing" }}
              </td>
              <td class="scope-desc">{{ scopesDesc[s] }}</td>
            </tr>
          </tbody>
        </table>
        <div>
          <p>Please re-authorise Strava with all required values:</p>
          <LoginStrava :show="true" />
        </div>
      </div>
    </div>
    <div class="col-1"></div>
  </div>
</template>

<style lang="scss">
.scope-name {
  font-weight: bold;
  &.missing {
    color: #a62020;
    font-weight: bold;
  }
}
.scope-state {
  text-align: center;
  padding: 0 6px;
  &.valid {
    background-color: #bbf1a4;
  }
  &.missing {
    background-color: #de7d7d;
    border: solid 1px #a62020;
    color: #ffffff;
    font-weight: bold;
  }
}
</style>
