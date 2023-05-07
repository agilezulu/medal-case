import { reactive } from "vue";
import { io } from "socket.io-client";
import { getJWT } from "@/utils/helpers.js";
export const state = reactive({
  connected: false,
  processing: false,
  runUpdates: []
});

const NODE_ENV = import.meta.env.VITE_NODE_ENV;
const URL = NODE_ENV === "dev" ? "http://127.0.0.1:5180" : "https://8vzirn1xee.execute-api.eu-west-1.amazonaws.com";
//export const socket = io(URL);

export const socket = io(URL, {
  autoConnect: false, path: "/prod", extraHeaders: {
    "Authorization": `Bearer ${getJWT()}`
  }
});

export const setSockAuth = () => {
  socket.disconnect();
  socket.io.opts.extraHeaders = {
    "Authorization": `Bearer ${getJWT()}`
  };
  socket.connect();
};

socket.on("connect", () => {
  state.connected = true;
  state.runUpdates = [];
});

socket.on("disconnect", () => {
  state.connected = false;
});

socket.on("update", () => {
  //state.runUpdates.push(args);
});

socket.on('athlete_update', function(msg) {
  state.runUpdates.push(msg.data);
  const messageContainer = document.getElementById("runs-stream-container");
  messageContainer.scrollTop = messageContainer.scrollHeight;
});

socket.on('athlete_update_complete', function() {
  console.log('SOCK: athlete_update_complete')
  state.processing = false;
  socket.disconnect();
});
