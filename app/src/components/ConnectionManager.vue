<script setup>
import { socket, state } from "@/socket";
const connect = () => {
  socket.connect();
};
const disconnect = () => {
  socket.disconnect();
};
</script>
<template>
    <p>connected: {{ state.connected }}</p>
    <button v-if="!state.connected" @click="connect()">Connect</button>
    <button v-if="state.connected" @click="disconnect()">Disconnect</button>
</template>


