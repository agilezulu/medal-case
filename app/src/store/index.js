import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";
import { groupBy } from "@/utils/helpers.js";

const NODE_ENV = import.meta.env.VITE_NODE_ENV;
const VUE_APP_CLIENT_ID = import.meta.env.VITE_VUE_APP_CLIENT_ID;
const URL_LOCAL = `http://${location.host}`;
const URL_LIVE = "https://medalcase.com";

const STREAKS_LOCAL = "http://localhost:5180";
const STREAKS_LIVE = "https://medalcase.com/v1/";
export const SCOPES = [
  "read",
  "profile:read_all",
  "activity:read",
  "activity:read_all"
];
export const CLASSES = [
  { name: "26.2", key: "c_marathon", row: 1 },
  { name: "50k", key: "c_50k", row: 1  },
  { name: "50mi", key: "c_50mi", row: 2  },
  { name: "100k", key: "c_100k", row: 2  },
  { name: "100k+", key: "c_100kplus", row: 2  },
  { name: "100mi", key: "c_100mi", row: 3  },
  { name: "Xtreme", key: "c_xtreme", row: 3  },
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

const redirectUrl = NODE_ENV === "production" ? URL_LIVE : URL_LOCAL;
const streaksAPI = NODE_ENV === "production" ? STREAKS_LIVE : STREAKS_LOCAL;
const API = (key, param) => {
  return {
    login: `${streaksAPI}/athlete/login`,
    list: `${streaksAPI}/athlete/list`,
    athlete: `${streaksAPI}/athlete/${param}`,
    build: `${streaksAPI}/athlete`,
    run: `${streaksAPI}/athlete/run`,
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
      return groupBy(state.athlete.runs, "class_key", ["class", "class_key"], "start_date_local");
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
      if (this.accessToken){
        axios.defaults.headers.common[
          "Authorization"
          ] = `Bearer ${this.accessToken}`;
      }
      //console.log('this.loggedInAthlete', this.loggedInAthlete);
    },
    doLogout(){
      axios.defaults.headers.common["Authorization"] = null;
      removeJWT();
      removeUSER();
      this.accessToken = null;
      this.loggedInAthlete = {};
      window.location = NODE_ENV === "production" ? URL_LIVE : URL_LOCAL;
    },
    async getAccessTokenFromCode(code) {
      const state = this;
      try {
        axios.post(
          API('login'),
          {
            code: code,
          },
          {}
        ).then(authReponse => {
          const responseData = authReponse.data;
          axios.defaults.headers.common[
            "Authorization"
            ] = `Bearer ${responseData.access_token}`;
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
      return axios.get(API('athlete', slug))
        .then( (response) => {
          this.athlete = response.data;
          this.loading = false;
          return { data: this.athlete, error: null };
        })
        .catch((error) => {
          this.athlete = null;
          this.loading = false;
          return { data: null, error: error.response.data };
        });

    },
    async getAthletes(fetch) {
      if (!fetch && this.athleteList.length){ return; }
      try {
        this.loading = true;
        const response = await axios.get(API('list'));
        this.athleteList = response.data;
      } catch (response) {
        console.log("error", response.errors);
      } finally {
        this.loading = false;
      }
    },
    async buildAthleteRuns() {
      this.loadingLocal = true;

      return axios.post(API('build'), null)
        .then((response) => {
          this.athlete = response.data;
          this.loadingLocal = false;
          return { data: this.athlete.meta, error: null };
        })
        .catch((error) => {
          this.loadingLocal = false;
          return { data: null, error: error.response.data };
        });
    },
    async updateRun(data) {
        const sendData = {
          class_key: data.class_key,
          name: data.name,
          race: data.race,
          strava_id: data.strava_id
        }
        return axios.put(API('run'), sendData);
    },
    refreshAthleteData(data) {
      this.athlete = data;
    }
  },
})
