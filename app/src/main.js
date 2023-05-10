import { createApp } from "vue";
import App from "@/App.vue";
import router from "@/router";
import { createPinia } from "pinia";
import { Amplify } from "aws-amplify";
//import awsExports from "./aws-exports";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from "@fortawesome/vue-fontawesome";
import Popper from "vue3-popper";

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
import ConfirmDialog from "primevue/confirmdialog";

import DialogService from "primevue/dialogservice";
import ToastService from "primevue/toastservice";
import ConfirmationService from "primevue/confirmationservice";
import "./assets/main.scss";


import "primeflex/primeflex.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";
import "@/assets//theme.css";

import {
  faMedal,
  faPersonRunning,
  faArrowUpRightFromSquare,
  faArrowRightFromBracket,
  faUser,
  faArrowsRotate,
  faPencil,
  faCircleStar,
  faChevronLeft,
  faTrashCan,
} from "@fortawesome/pro-light-svg-icons";

import {
  faHexagon,
  faMountain
} from "@fortawesome/sharp-light-svg-icons";

import {
  faStarOfLife,
  faHexagon as fasHexagon
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
  faStarOfLife,
  faChevronLeft,
  faTrashCan,
  fasHexagon,
  faMountain
);

//Amplify.configure(awsExports);
Amplify.configure({
  API: {
    endpoints: [
      {
        name: 'medalcaseapi',
        endpoint: 'https://api.medalcase.com',
        custom_header: async () => {
          return {
            'X-Api-Key': 'YkxgqM5IVEae9AViOs7Jqa3ad98Jsgmn2TACafs5',
            'Authorization': `Bearer ${localStorage.getItem('medalcase_jwt')}`
          };
        }
      }
    ]
  }
});

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(PrimeVue, { ripple: true });
app.use(ToastService);
app.use(DialogService);
app.use(ConfirmationService);

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
app.component("ConfirmDialog", ConfirmDialog);

app.component("Popper", Popper);

app.component("font-awesome-icon", FontAwesomeIcon);
app.component("font-awesome-layers", FontAwesomeLayers);
app.component("font-awesome-layers-text", FontAwesomeLayersText);

app.mount("#app");
