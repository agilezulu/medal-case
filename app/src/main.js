import { createApp } from "vue";
import App from "@/App.vue";
import router from "@/router";
import { createPinia } from "pinia";
import { Amplify } from "aws-amplify";
import awsExports from "./aws-exports";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from "@fortawesome/vue-fontawesome";

import PrimeVue from "primevue/config";
import SelectButton from "primevue/selectbutton";
import Menubar from "primevue/menubar";
import Button from "primevue/button";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Row from "primevue/row";
import Accordion from "primevue/accordion";
import AccordionTab from "primevue/accordiontab";
import Dialog from "primevue/dialog";
import DynamicDialog from "primevue/dynamicdialog";
import Toast from "primevue/toast";
import InputText from "primevue/inputtext";
import Dropdown from "primevue/dropdown";
import InputSwitch from "primevue/inputswitch";

import DialogService from "primevue/dialogservice";
import ToastService from "primevue/toastservice";
import "./assets/main.scss";

import "primevue/resources/themes/lara-light-indigo/theme.css";
import "primeflex/primeflex.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";

import {
  faMedal,
  faPersonRunning,
  faArrowUpRightFromSquare,
  faArrowRightFromBracket,
  faUser,
  faArrowsRotate,
  faPencil,
  faCircleStar
} from "@fortawesome/pro-light-svg-icons";

import {
  faHexagon
} from "@fortawesome/sharp-light-svg-icons";

import {
  faStarOfLife
} from "@fortawesome/sharp-solid-svg-icons";


library.add(
  faMedal,
  faPersonRunning,
  faArrowUpRightFromSquare,
  faArrowRightFromBracket,
  faUser,
  faArrowsRotate,
  faPencil,
  faCircleStar,
  faHexagon,
  faStarOfLife
);

Amplify.configure(awsExports);

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(PrimeVue, { ripple: true });
app.use(ToastService);
app.use(DialogService);

app.component("SelectButton", SelectButton);
app.component("Menubar", Menubar);
app.component("Button", Button);
app.component("DataTable", DataTable);
app.component("Column", Column);
app.component("Row", Row);
app.component("Accordion", Accordion);
app.component("AccordionTab", AccordionTab);
app.component("Dialog", Dialog);
app.component("DynamicDialog", DynamicDialog);
app.component("Toast", Toast);
app.component("InputText", InputText);
app.component("Dropdown", Dropdown);
app.component("InputSwitch", InputSwitch);

app.component("font-awesome-icon", FontAwesomeIcon);
app.component("font-awesome-layers", FontAwesomeLayers);
app.component("font-awesome-layers-text", FontAwesomeLayersText);

app.mount("#app");
