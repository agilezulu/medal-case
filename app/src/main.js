import { createApp } from "vue";
import App from "@/App.vue";
import router from "@/router";
import { createPinia } from "pinia";
import { Amplify } from "aws-amplify";
import awsExports from "./aws-exports";


import PrimeVue from "primevue/config";
import SelectButton from "primevue/selectbutton";
import Menubar from "primevue/menubar";
import Button from "primevue/button";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Row from "primevue/row";
import Accordion from "primevue/accordion";
import AccordionTab from "primevue/accordiontab";
import "./assets/main.scss";

import "primevue/resources/themes/lara-light-indigo/theme.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";

Amplify.configure(awsExports);

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(PrimeVue, { ripple: true });

app.component("SelectButton", SelectButton);
app.component("Menubar", Menubar);
app.component("Button", Button);
app.component("DataTable", DataTable);
app.component("Column", Column);
app.component("Row", Row);
app.component("Accordion", Accordion);
app.component("AccordionTab", AccordionTab);


app.mount('#app');
