import { defineStore } from "pinia";
import { API } from 'aws-amplify';
import axios from "axios";
import router from "@/router";
import { groupBy } from "@/utils/helpers.js";

const NODE_ENV = import.meta.env.VITE_NODE_ENV;
const VUE_APP_CLIENT_ID = import.meta.env.VITE_VUE_APP_CLIENT_ID;
const URL_LOCAL = `http://${location.host}`;
const URL_LIVE = "https://medalcase.com";
const apiName = "medalcaseapi";
const API_LOCAL = "http://127.0.0.1:5180";
const API_LIVE = "";
const DEVMODE = (NODE_ENV && NODE_ENV === "dev");
const redirectUrl = DEVMODE ? URL_LOCAL :  URL_LIVE;
const mcaseAPI = DEVMODE ? API_LOCAL : API_LIVE;
console.log('DEVMODE', DEVMODE, NODE_ENV);
export const SCOPES = [
  "read",
  "profile:read_all",
  "activity:read_all"
];
// 'profile:read_all', 'profile:write', 'profile:read_all', 'activity:read_all', 'activity:write'
export const CLASSES = [
  { name: "26.2", key: "c_marathon", row: 1 },
  { name: "50k", key: "c_50k", row: 1  },
  { name: "50mi", key: "c_50mi", row: 1  },
  { name: "100k", key: "c_100k", row: 1  },
  { name: "100k+", key: "c_100kplus", row: 2  },
  { name: "100mi", key: "c_100mi", row: 2  },
  { name: "Xtreme", key: "c_xtreme", row: 2  },
];
const classKeys = CLASSES.map(c => c.key);
export const classLookup = CLASSES.reduce((obj, item) => {
  obj[item.key] = item;
  return obj;
}, {});

export const classRows = Object.values(CLASSES.reduce((acc, obj) => {
    let key = obj.row;
    if (key in acc) {
      acc[key].push(obj);
    } else {
      acc[key] = [obj];
    }
  return acc;
}, {}));

if (DEVMODE) {
  axios.interceptors.response.use((response) => {
    return response.data;
  }, (error) => {
    return Promise.reject(error.message);
  });
}

const apiPath = (key, param) => {
  return {
    login: `${mcaseAPI}/athlete/login`,
    list: `${mcaseAPI}/athlete/list`,
    athlete: `${mcaseAPI}/athlete/${param}`,
    build: `${mcaseAPI}/athlete`,
    run: `${mcaseAPI}/athlete/run`,
    chaeck: `${mcaseAPI}/athlete/chaeck`,
    }[key];
};

export const STRAVA_OAUTH_URL = `https://www.strava.com/oauth/authorize?client_id=${VUE_APP_CLIENT_ID}&response_type=code&redirect_uri=${redirectUrl}/exchange_token&approval_prompt=force&scope=${SCOPES.join(
  ","
)}`;

const jwtKey = "medalcase_jwt";
const userKey = "medalcase_user";
const setJWT = (token) => window.localStorage.setItem(jwtKey, token);
const getJWT = () => window.localStorage.getItem(jwtKey);
const removeJWT = () => window.localStorage.removeItem(jwtKey);

const setUser = (data) => window.localStorage.setItem(userKey, JSON.stringify(data));
const getUser = () => JSON.parse(window.localStorage.getItem(userKey));
const removeUSER = () => window.localStorage.removeItem(userKey);

export const medalStore = defineStore('todos', {
  state: () => ({
    loading: false,
    loadingLocal: false,
    accessToken: null,
    loggedInAthlete: {},
    units: ['mi', 'km'],
    selectedUnits: "mi",
    athleteList: [],
    athlete: {
      runs: [],
      new_runs: {},
      meta: {}
    },
  }),
  getters: {
    isLoggedIn(state) {
      return !!state.accessToken;
    },
    athleteRuns(state) {
      if (!state.athlete){ return; }
      return state.athlete.runs.length ? groupBy(state.athlete.runs, "class_key", ["class", "class_key"], "start_date_local") : {};
    },
    isLoading(state) {
      return state.loading;
    },
    getSessionSlug(state) {
      return state.loggedInAthlete.slug;
    },
    isOnboarding(state) {
      return state.athlete && !state.athlete.last_run_date && state.loggedInAthlete.slug ===  state.athlete.slug && !state.athlete.total_runs;
    }
  },
  actions: {
    setAccess() {
      this.accessToken = getJWT();
      this.loggedInAthlete = getUser();
      if (DEVMODE && this.accessToken){
        axios.defaults.headers.common[
          "Authorization"
          ] = `Bearer ${this.accessToken}`;
      }
    },
    doLogout(){
      if (DEVMODE) {
        axios.defaults.headers.common["Authorization"] = null;
      }
      removeJWT();
      removeUSER();
      this.accessToken = null;
      this.loggedInAthlete = {};
      window.location = NODE_ENV === "production" ? URL_LIVE : URL_LOCAL;
    },
    async getAccessTokenFromCode(code) {
      const state = this;
      const postBody = {code: code};
      console.log(postBody);
      const api = DEVMODE
        ? axios.post(apiPath('login'), postBody, {})
        : API.post(apiName, apiPath('login'), {body: postBody});
      try {
        api.then(authReponse => {
          const responseData = authReponse;
          if (DEVMODE) {
            axios.defaults.headers.common[
              "Authorization"
              ] = `Bearer ${responseData.access_token}`;
          }
          setJWT(responseData.access_token);
          state.accessToken = responseData.access_token;
          const userData = {
            firstname: responseData.firstname,
            lastname: responseData.lastname,
            slug: responseData.slug,
          };
          setUser(userData);
          this.loggedInAthlete = userData;
          router.push('/me');
        });

      } catch (response) {
        console.log("Authorisation error", response.errors);
      }
    },
    async getAthlete(slug) {
      this.loading = true;
      const api = DEVMODE ? axios.get(apiPath('athlete', slug)) : API.get(apiName, apiPath('athlete', slug), null);
      return api.then( (response) => {
          this.athlete = response;
          this.loading = false;
          return { data: this.athlete, error: null };
        })
        .catch((error) => {
          this.athlete = null;
          this.loading = false;
          return { data: null, error: error.response };
        });
    },
    async getAthletes(fetch) {
      if (!fetch && this.athleteList.length){ return; }
      this.loading = true;
      const api = DEVMODE ? axios.get(apiPath('list')) : API.get(apiName, apiPath('list'), null);
      api.then((response) => {
        this.athleteList = response;
        this.loading = false;
      }).catch((error) => {
        console.log("error", error);
        this.loading = false;
      });
    },
    async buildAthleteRuns() {
      this.loadingLocal = true;
      const api = DEVMODE ? axios.post(apiPath('build')) : API.post(apiName, apiPath('build'), null);
      return api.then((response) => {
          this.athlete = response;
          this.loadingLocal = false;
          return { data: this.athlete.meta, error: null };
        })
        .catch((error) => {
          this.loadingLocal = false;
          return { data: null, error: error };
        });
    },
    async checkAthleteProcessing() {
      this.loadingLocal = true;
      const api = DEVMODE ? axios.get(apiPath('check')) : API.get(apiName, apiPath('check'), null);
      return api.then((response) => {
          let is_processing = response.is_processing;
          if (is_processing){
            return  {is_processing: true, data: null, error: null};
          }
          else {
            this.athlete = response.athlete;
            this.loadingLocal = false;
            return {is_processing: response.is_processing, data: this.athlete.meta, error: null};
          }
        })
        .catch((error) => {
          this.loadingLocal = false;
          return { data: null, error: error };
        });
    },
    async updateRun(data) {
        const sendData = {
          class_key: data.class_key,
          name: data.name,
          race: data.race,
          strava_id: data.strava_id
        }
        return DEVMODE ? axios.put(apiPath('run'), sendData) : API.put(apiPath('run'), sendData);
    },
    refreshAthleteData(data) {
      this.athlete = data;
    }
  },
})
