import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

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
const redirectUrl = NODE_ENV === "production" ? URL_LIVE : URL_LOCAL;
const streaksAPI = NODE_ENV === "production" ? STREAKS_LIVE : STREAKS_LOCAL;
const URL = {
  login: `${streaksAPI}/athlete/login`,
  list: `${streaksAPI}/athlete`,
};
export const STRAVA_OAUTH_URL = `https://www.strava.com/oauth/authorize?client_id=${VUE_APP_CLIENT_ID}&response_type=code&redirect_uri=${redirectUrl}/exchange_token&approval_prompt=force&scope=${SCOPES.join(
  ","
)}`;

const jwtName = "medalcase_jwt";
const setJWT = (token) => window.localStorage.setItem(jwtName, token);
const getJWT = () => window.localStorage.getItem(jwtName);
const removeJWT = () => window.localStorage.removeItem(jwtName);

export const medalStore = defineStore('todos', {
  state: () => ({
    loading: false,
    accessToken: null,
    units: ['mi', 'km'],
    selectedUnits: "mi",
    athleteList: [],
    classes: [
      {
        name: "Marathon",
        getter: "runsMarathon",
        classname: "marathon"
      },
      {
        name: "Ultra",
        getter: "runsUltra",
        classname: "ultra"
      }
    ],
    runs: {
      totals: {
        runs: 0,
        distance: 0,
        time: 0
      },
      by_mile: {},
      classes: {
        half: {
          tot: 0,
          runs: []
        },
        marathon: {
          tot: 0,
          runs: []
        },
        ultra: {
          tot: 0,
          subclass: {},
          runs: [],
        }
      }
    },
  }),
  getters: {
    isLoggedIn(state) {
      console.log('isLoggedIn', !!state.accessToken);
      return !!state.accessToken;
    },
    runsByMile(state) {
      const sortedKeys = Object.keys(state.runs.by_mile).sort((a, b) => parseInt(a, 10) - parseInt(b, 10));
      let byMile = [];
      sortedKeys.forEach(dist => {
        byMile.push({
          mile: dist,
          count: state.runs.by_mile[`${dist}`]
        });
      });
      return byMile;
    },
    runsHalf(state) {
      return state.runs.classes.half.runs.sort((a, b) => a.elapsed_time - b.elapsed_time);
    },
    runsMarathon(state) {
      return state.runs.classes.marathon.runs.sort((a, b) => a.elapsed_time - b.elapsed_time);
    },
    runsUltra(state) {
      return state.runs.classes.ultra.runs.sort((a, b) => b.distance - a.distance)
    }
  },
  actions: {
    setAccess() {
      this.accessToken = getJWT();
      if (this.accessToken){
        axios.defaults.headers.common[
          "Authorization"
          ] = `Bearer ${this.accessToken}`;
      }
    },
    doLogout(){
      axios.defaults.headers.common["Authorization"] = null;
      removeJWT();
      window.location = NODE_ENV === "production" ? URL_LIVE : URL_LOCAL;
    },
    async getAccessTokenFromCode(code) {
      const state = this;
      try {
        console.log("getAccessToken", code);
        axios.post(
          URL.login,
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
          router.push("/me");
        });


      } catch (response) {
        console.log("Authorisation error", response.errors);
      }
    },
    async getRuns() {
      const response = await axios.get('/data/16055914_runs_summary.json');
      //const response = await axios.get('/data/33593239_runs_summary.json');
      this.runs = response.data;
    },
    async getAthletes() {
      this.loading = true;
      try {
        console.log("getAthletes");
        const response = await axios.get(URL.list);
        this.athleteList = response.data;
      } catch (response) {
        console.log("error", response.errors);
      } finally {
        this.loading = false;
      }
    },
  },
})
