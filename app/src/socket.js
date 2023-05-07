import { reactive } from "vue";
import { io } from "socket.io-client";
import { getJWT } from "@/utils/helpers.js";
export const state = reactive({
  connected: false,
  processing: false,
  runUpdates: []
});

const NODE_ENV = import.meta.env.VITE_NODE_ENV;
const URL = NODE_ENV === "dev" ? "http://127.0.0.1:5180" : "https://api.medalcase.com";
//export const socket = io(URL);

const token = getJWT();
export const socket = io(URL, {
  autoConnect: false, extraHeaders: {
    "Authorization": `Bearer ${token}`
  }
});

socket.on("connect", () => {
  state.connected = true;
  state.runUpdates = [];
});

socket.on("disconnect", () => {
  state.connected = false;
});

socket.on("update", (...args) => {
  //state.runUpdates.push(args);
});

socket.on('athlete_update', function(msg) {
  console.log('athlete_update', msg);
  state.runUpdates.push(msg)
});

socket.on('athlete_update_complete', function() {
  state.processing = false;
  socket.disconnect();
});
