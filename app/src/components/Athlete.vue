<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { medalStore, classLookup } from "@/store";
import { metersToDistanceUnits, getDate, secsToHMS } from "@/utils/helpers.js";
import {storeToRefs} from "pinia";
import { useDialog } from "primevue/usedialog";
import { useToast } from "primevue/usetoast";
import { formatDate } from "@/utils/helpers.js";
import RunEdit from "@/components/RunEdit.vue";
import AthleteMedalcase from "@/components/AthleteMedalcase.vue";

import MedalcaseLogo from "@/components/icons/MedalcaseLogo.vue";
import BadgeRace from "@/components/icons/BadgeRace.vue";
import BadgeRun from "@/components/icons/BadgeRun.vue";

const props =  defineProps({
  currentUser: Boolean,
});

const { athlete, loadingLocal } = storeToRefs(medalStore());
const store = medalStore();
const route = useRoute();
const dialog = useDialog();
const toast = useToast();

const formatMessages = (meta) => {
  const gotNew = Object.keys(meta.new_runs).length;
  let detail = `<div class="m-detail"><div>${meta.scanned_runs} runs since: ${formatDate(meta.last_scan_date)}</div>`;
  if (gotNew) {
    Object.keys(meta.new_runs).forEach((key) => {
      detail += `<div class="m-info"><div class="m-name">${classLookup[key].name}:</div><div class="m-count">${meta.new_runs[key]}</div></div>`;
    });
  }
  detail += '</div>';
  let summary =  !gotNew ? "No new medals" : "Congrats! New medals found";
  return { 
    detail: detail,
    summary: summary,
    severity: gotNew ? "success": "info",
  };
}
const buildRuns = () => {
  store.buildAthleteRuns().then((meta) => {
    const messages = formatMessages(meta);
    toast.add({
      severity: messages.severity,
      summary: messages.summary,
      detail: messages.detail,
      life: 5000
    });
  });


}

const dynamicDialogRef = ref(null);

const editRun = (run) => {
  dynamicDialogRef.value = dialog.open(RunEdit, {
    data: {
      run: run
    },
    props: {
      header: `Update ${run.name}`,
      style: {
        width: '50vw',
      },
      breakpoints:{
        '960px': '75vw',
        '640px': '90vw'
      },
      modal: true
    },
    onClose: (response) => {
      if (response.data) {
        toast.add({ severity: 'success', detail: "Run successfully updated", life: 3000 });
        store.refreshAthleteData(response.data);
      }
    }
  });

}

onMounted(() => {
  const athleteSlug = props.currentUser ? store.getSessionSlug : route.params.slug;
  if (athleteSlug) {
    store.getAthlete(athleteSlug);
  }
  else {
    toast.add({ severity: 'error', summary: "Error", detail: "Cannot find identifier for athlete", life: 5000 });
  }
});
</script>

<template>
  <div>
    <div id="case-header">

      <AthleteMedalcase :athlete="athlete" />

      <div v-if="currentUser" class="tools-cont">
        <div class="update-tools">
          <a href="javascript:void(0);"
              @click="buildRuns()"
              class="p-button p-component p-button-secondary p-button-outlined p-button-sm"
              :disabled="loadingLocal"
              v-if="store.isLoggedIn"
          >Update Medalcase <font-awesome-icon icon="fa-light fa-arrows-rotate" fixed-width :spin="loadingLocal" /></a>
          <div class="last-run-date">Last run: {{formatDate(athlete.last_run_date)}}</div>
        </div>
      </div>
    </div>
    <div id="case-summary">

        <div class="class-body">

          <Accordion class="accordion-custom" :multiple="true" :activeIndex="[0]">
            <template v-for="runClass in store.athleteRuns" :key="runClass.gKey">
            <AccordionTab>
              <template #header>
                <div class="run-class">
                  <div class="class-name">{{ runClass.class }}</div>
                  <div class="counts">
                    <div class="class-count race">
                      <div class="count race" :class="runClass.class_key">
                        <BadgeRace />
                        <span> {{athlete[`${runClass.gKey}_race`]}}</span>
                      </div>
                    </div>
                    <div class="class-count" :class="runClass.class_key">
                      <div class="medal-bg">
                        <MedalcaseLogo border="currentColor" center="#ffffff" />
                      </div>
                      <div class="count">
                        <span>{{athlete[runClass.gKey]}}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
              <div class="run-list">
                <div v-for="(run, idx) in runClass.gVal" :key="run.strava_id" class="run-single">

                  <div class="run-info">

                    <div class="run-title">
                      <span class="run-idx">{{idx+1}}</span>
                      <span class="run-ico" :class="run.race ? runClass.class_key : 'c_training'">
                        <template v-if="run.race"><BadgeRace /></template>
                        <template v-else><BadgeRun /></template>
                      </span>

                      <a :href="`https://www.strava.com/activities/${run.strava_id}/overview`" target="_new" class="run-name" :class="run.race ? runClass.class_key : 'c_training'">{{run.name}} <font-awesome-icon icon="fa-light fa-arrow-up-right-from-square" transform="shrink-4 up-6" /></a>
                    </div>
                    <div class="run-date">{{getDate(run.start_date_local)}}</div>
                  </div>
                  <div class="run-stats">
                    <div class="run-time" :class="run.race ? runClass.class_key : ''">{{ secsToHMS(run.elapsed_time)}}</div>
                    <div class="run-dist">{{ metersToDistanceUnits(run.distance, 'mi')}}</div>
                  </div>
                  <div v-if="props.currentUser" class="run-tools">
                    <a href="javascript:void(0);" class="action" @click="editRun(run)"><font-awesome-icon icon="fa-light fa-pencil" /></a>
                  </div>
                </div>
              </div>
            </AccordionTab>
            </template>
          </Accordion>

        </div>
      </div>
    <DynamicDialog ref="dynamic-dialog">
      <!-- content of the dialog goes here -->
    </DynamicDialog>
  </div>
</template>

<style lang="scss">
.p-toast-message-content {
  .m-detail {
    .m-info {
      display: flex;
      width: 150px;
      .m-name {
        flex: 1;
        font-weight: bold;
        text-align: right;
      }
      .m-count {
        text-align: right;
        min-width: 30px
      }
    }
  }
}
#case-header {
  .tools-cont {
    display: flex;
    justify-content: right;
    .last-run-date {
      font-size: 0.8rem;
    }
  }
  .update-tools {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: solid 1px #dddddd;
    background-color: #eeeeee;
    padding: 4px;
    border-radius: 6px;

    .p-button {
      padding: 2px 12px;
      background-color: #ffffff;
    }
  }
}

#case-summary {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  flex-wrap: wrap;

  .p-accordion .p-accordion-header:not(.p-disabled) .p-accordion-header-link:focus {
    outline: 0 none;
    outline-offset: 0;
    box-shadow: none;
  }
  .p-accordion {
    .p-accordion-header {
      .p-accordion-header-link {
        padding-right: 4px;
      }
    }
  }
  .run-class {
    display: flex;
    flex: 1;
    justify-content: space-between;
    .counts {
      flex-wrap: nowrap;
      display: flex;
      .class-count {
        position: relative;
        display: flex;
        width: 60px;
        justify-content: center;
        &.race {
          justify-content: flex-start;
        }
        .medal-bg {
          position: absolute;
          width: 60px;
          top: -16px;
        }

        .count {
          position: relative;
          z-index: 12;
          &.race {
            display: flex;
            .badge {
              display: inline-block;
              width: 25px;
              height: 25px;
              margin-right: 4px;
              svg {
                width: 100%;
                height: 100%;
              }
            }
          }
        }
      }
    }
  }
  .run-single {
    display: flex;
    justify-content: space-between;
    &:hover {
     background-color: #eeeeee;
    }
  }
  .class-body {
    padding: 12px;
    width: 100%;
  }
  .run-list {
    .run-info {
      flex: 1;
      .run-title {
        display: flex;
        .run-name {
          font-weight: 700;
          &.c_training {
            font-weight: 400;
          }
        }
        .run-idx {
          min-width: 20px;
          text-align: right;
          padding-right: 8px;
          font-weight: 200;
          color: #555555;
        }
        .run-ico {
          margin-right: 6px;
          margin-top: 2px;
          width: 22px;
          svg {
            width: 100%;
          }
        }
      }
      .run-date {
        padding-left: 22px;
      }
    }
    .run-tools {
      flex: 0 0 40px;
      display: flex;
      justify-content: flex-end;
    }

  }


  .idx {
    vertical-align: top;
    text-align: right;
    padding-right: 6px;
  }
  .run-date,
  .run-dist {
    font-weight: 300;
    font-size: 0.8em;
    color: #666666;
  }
  .run-time {
    &.race {
      color: #ff4e00;
    }
  }
}
</style>
