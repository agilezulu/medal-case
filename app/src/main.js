import { createApp } from "vue";
import App from "@/App.vue";
import router from "@/router";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import SelectButton from "primevue/selectbutton";

import "./assets/main.css";

import "primevue/resources/themes/lara-light-indigo/theme.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(PrimeVue);

app.component("SelectButton", SelectButton);

app.mount('#app');
