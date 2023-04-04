import { defineStore } from "pinia";
import axios from "axios";

/*
const apiClient = axios.create({
  baseURL: 'https://api.example.com/',
});

 */
export const medalStore = defineStore('todos', {
  state: () => ({
    units: ['mi', 'km'],
    selectedUnits: "mi",
    classes: [
      {
        name: "Ultra",
        getter: "runsUltra",
        classname: "ultra"
      },
      {
        name: "Marathon",
        getter: "runsMarathon",
        classname: "marathon"
      },
      {
        name: "Half",
        getter: "runsHalf",
        classname: "half"
      },
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
    async getRuns() {
      const response = await axios.get('/data/16055914_runs_summary.json');
      //const response = await axios.get('/data/33593239_runs_summary.json');
      this.runs = response.data;
    },
  },
})
