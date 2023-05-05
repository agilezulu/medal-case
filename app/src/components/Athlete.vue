<script setup>
import { onUnmounted, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { medalStore, classLookup, CLASSES } from "@/store";
import { metersToDistanceUnits, getDate, secsToHMS } from "@/utils/helpers.js";
import {storeToRefs} from "pinia";
import { useDialog } from "primevue/usedialog";
import { useToast } from "primevue/usetoast";
import { formatDate } from "@/utils/helpers.js";
import PopOver from "@/components/PopOver.vue";
import RunEdit from "@/components/RunEdit.vue";
import AthleteMedalcase from "@/components/AthleteMedalcase.vue";
import AthletePhoto from "@/components/AthletePhoto.vue";
import MedalcaseLogo from "@/components/icons/MedalcaseLogo.vue";
import BadgeRace from "@/components/icons/BadgeRace.vue";
import BadgeRun from "@/components/icons/BadgeRun.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import AthleteList from "@/components/AthleteList.vue";

const props =  defineProps({
  currentUser: Boolean,
});

const { athlete } = storeToRefs(medalStore());
const store = medalStore();
const route = useRoute();
const dialog = useDialog();
const toast = useToast();

const activeClasses = ref([]);
const polling = ref(null);
const dynamicDialogRef = ref(null);

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

const checkStatus = () => {

  polling.value = setInterval(() => {
    store.checkAthleteProcessing().then((response) => {
      console.log('Processing state:', response);
      if (response.error){
        toast.add({
          severity: 'error',
          summary: response.error.name,
          detail: response.error.description,
          life: 5000
        });
      }
      else if (response.is_processing){
        console.log('is processing');
      }
      else {
        const messages = formatMessages(response.data);
        toast.add({
          severity: messages.severity,
          summary: messages.summary,
          detail: messages.detail,
          life: 12000
        });
      }
    });
  }, 5000);
}

const buildRuns = () => {
  store.buildAthleteRuns().then((response) => {
    console.log('build response', response)
    if (response.error){
      toast.add({ severity: 'error', summary: response.error.name, detail: response.error.description, life: 5000 });
    }
    else {
      checkStatus();
    }
  });
}

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
    store.getAthlete(athleteSlug).then((response) => {
      if (response.error){
        toast.add({ severity: 'error', summary: response.error.name, detail: response.error.description, life: 5000 });
      }
      else {
        if (store.isOnboarding){
          buildRuns();
        }
        activeClasses.value = store.athleteRuns ? CLASSES.filter((mclass) => store.athleteRuns[mclass.key]) : [];
      }
    });
  }
  else {
    toast.add({ severity: 'error', summary: "Error", detail: "Cannot find identifier for athlete", life: 5000 });
  }
});
onUnmounted(() => {
  clearInterval(polling.value);
})
</script>

<template>
    <div v-if="store.isOnboarding" id="athlete-onboarding">
      <div>

        <div class="greet">
          <div class="photo-logo">
            <div class="pl-bg"><img src="/medalcase_logo.svg" /></div>
            <div class="pl-img"><AthletePhoto :photo="athlete.photo" :size="100" /></div>
          </div>
          <div>Hi {{athlete.firstname}},
            <br />
            Welcome to Medalcase!
          </div>
        </div>
        <p> Please stand by while we scan your runs, this might take a minute or so...</p>
        <div class="local-spinner">
          <LoadingSpinner />
        </div>
      </div>
    </div>
    <div v-else id="athlete-medalcase">
        <!--
      <div class="back-link">
        <router-link to="/" class="p-menuitem-link"><font-awesome-icon icon="fa-light fa-fw fa-chevron-left" size="lg" /> list</router-link>
      </div>
      -->
      <template v-if="athlete">
      <div id="case-header">
        <AthleteMedalcase :athlete="athlete" />
      </div>

        <div class="container">
          <div class="left-column"></div>
          <div class="center-column">

            <div id="action-bar">
                <div class="athlete-info">
                    <AthletePhoto :photo="athlete.photo" :size="80" />
                    <div class="inf">
                        <div class="a-name">{{athlete.firstname}} {{athlete.lastname}}</div>
                        <img :src="`/img/flags/${athlete.country_code}.svg`" class="a-flag"/>
                    </div>

                </div>

                <div v-if="currentUser" class="tools-cont">
                    <div class="update-tools">
                        <Button
                                @click="buildRuns()"
                                class="p-button p-component p-button-secondary p-button-outlined p-button-sm"
                                :class="{loading: store.loadingLocal}"
                                :disabled="store.loadingLocal"
                                v-if="store.isLoggedIn"
                        >Update Medalcase <font-awesome-icon icon="fa-light fa-arrows-rotate" fixed-width :spin="store.loadingLocal" /></Button>
                        <div class="last-run-date">Last run: {{formatDate(athlete.last_run_date)}}</div>
                    </div>
                </div>
            </div>
            <div id="case-summary" v-if="store.athlete.runs.length">


                <div class="class-body">

                  <Accordion class="accordion-custom" :multiple="true" :activeIndex="[0]">

                    <AccordionTab v-for="runClass in activeClasses" :key="runClass.key">
                      <template #header>
                        <div class="run-class" :class="runClass.key">
                          <div class="class-name">
                              <div class="name-label">{{ runClass.name }}</div>
                              <div class="class-pb">
                                  <div class="pb-title">PB</div>
                                  <div class="pb-val face-mono" :class="runClass.key">{{ secsToHMS(store.athleteRuns[runClass.key].pb)}}</div>
                              </div>
                          </div>
                          <div class="counts">
                            <PopOver :content="`${athlete[`${runClass.key}_race`]} <b>${runClass.name}</b> race${athlete[`${runClass.key}_race`] > 1 ? 's' : ''}`">
                            <div class="class-count race">
                              <div class="count race" :class="runClass.key">
                                <BadgeRace />
                                <span> {{athlete[`${runClass.key}_race`]}}</span>
                              </div>
                            </div>
                            </PopOver>
                            <PopOver :content="`${athlete[runClass.key]}  <b>${runClass.name}</b>  run${athlete[runClass.key] > 1 ? 's' : ''} in total`">
                              <div class="class-count" :class="runClass.key">
                                <div class="medal-bg">
                                  <MedalcaseLogo border="currentColor" center="#ffffff"/>
                                </div>
                                <div class="count">
                                  <span>{{athlete[runClass.key]}}</span>
                                </div>
                              </div>
                              </PopOver>
                          </div>
                        </div>
                      </template>

                      <div class="run-list">

                        <div v-for="(run, idx) in store.athleteRuns[runClass.key].gVal" :key="run.strava_id" class="run-single">

                          <div class="run-info">

                            <div class="run-title">
                              <span class="run-idx">{{idx+1}}</span>
                              <span class="run-ico" :class="run.race ? runClass.key : 'c_training'">
                                <template v-if="run.race"><BadgeRace /></template>
                                <template v-else><BadgeRun /></template>
                              </span>
                              <span class="run-name" :class="run.race ? runClass.key : 'c_training'" v-html="run.name"></span>
                            </div>
                            <div class="run-date">{{getDate(run.start_date_local)}} | <a :href="`https://www.strava.com/activities/${run.strava_id}/overview`" :class="runClass.key" class="vos" target="_new"><span>View on Strava <font-awesome-icon icon="fa-light fa-arrow-up-right-from-square" transform="shrink-4" /></span></a></div>
                          </div>
                          <div class="run-stats">
                            <div class="run-time face-mono" :class="[store.athleteRuns[runClass.key].pb === run.elapsed_time ? `class-pb ${runClass.key}_bg`: '']">{{ secsToHMS(run.elapsed_time)}}</div>
                            <div class="run-dist">{{ metersToDistanceUnits(run.distance, 'mi')}}</div>
                          </div>
                          <div v-if="props.currentUser" class="run-tools">
                            <a href="javascript:void(0);" class="action" @click="editRun(run)"><font-awesome-icon icon="fa-light fa-pencil" /></a>
                          </div>
                        </div>
                      </div>
                    </AccordionTab>

                  </Accordion>
                </div>
              </div>
          </div>
          <div class="right-column"></div>
        </div>
      </template>
      <template v-else>
          <div class="noathlete">
            <h3>No athele found</h3>
          </div>
      </template>
    </div>
    <DynamicDialog ref="dynamic-dialog">
      <!-- content of the dialog goes here -->
    </DynamicDialog>

</template>

<style lang="scss">
@import "@/assets/main.scss";
#athlete-onboarding {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  .local-spinner {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
.noathlete {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}
#athlete-medalcase {
  flex: 1;
  .popper {
    font-weight: 400;
  }

}
.greet {
  display: flex;
  align-items: center;
}

.back-link {
  margin-top: 12px;
}
#case-header {


}
#action-bar {
  position: relative;
  display: flex;
  justify-content: space-between;
  padding: 12px;
  .athlete-info {
    position: relative;
    display: flex;
    align-items: center;
    .inf {
      display: flex;
      flex-direction: column;
      margin-left: 8px;
      .a-flag {
        max-width: 50px;
        max-height: 30px;
      }
    }
    .a-name {
      font-weight: 800;
    }
  }
  .tools-cont {
    display: flex;
    justify-content: right;
    .last-run-date {
      font-size: 0.8rem;
    }
  }
  .update-tools {
    display: flex;
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
      &.loading {
        background-color: $color-action;
        color: #ffffff;
      }
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
    .class-name {
      display: flex;
      .name-label {
        width: 63px;
      }
    }
    .class-pb {
      display: flex;
      border: solid 1px #dddddd;
      border-radius: 12px;
      padding-right: 12px;
      align-items: center;
      background-color: #ffffff;
      overflow: hidden;
      .pb-title {
        background-color: #f5f5f5;
        padding-left: 9px;
        padding-right: 6px;
        font-size: 12px;
        display: flex;
        align-items: center;
        height: 100%;
        font-weight: 400;
        color: #aaaaaa;
      }
      .pb-val {
        padding-left: 6px;
        font-weight: 300;
        min-width: 77px;
        text-align: right;
        font-size: 14px;
      }
    }
    .counts {
      flex-wrap: nowrap;
      display: flex;
      .class-count {
        position: relative;
        display: flex;
        width: 50px;
        justify-content: center;
        z-index: 100;
        &.race {
          min-width: 56px;
        }
        .medal-bg {
          position: absolute;
          width: 44px;
          top: -13px;
        }

        .count {
          position: relative;
          z-index: 12;
          &.race {
            display: flex;
            justify-content: space-between;
            flex: 1;
            margin-right: 10px;
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
    border-bottom: solid 1px #eeeeee;
    margin-bottom: 12px;
    padding-bottom: 3px;
  }
  .class-body {
    padding: 12px;
    width: 100%;
  }
  .run-list {
    .run-info {
      flex: 1;
      .vos {
        font-size: 12px;
        display: inline-block;
        margin-left: 2px;
      }
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
    .run-stats {
      .run-time {
        text-align: right;
        padding: 0 12px;
        &.class-pb {
          border-radius: 18px;
          color: #ffffff;
        }
      }
      .run-dist {
        text-align: right;
        padding-right: 12px;
      }
    }
    .run-tools {
      flex: 0 0 20px;
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
  .run-date {
    margin-top: -7px;
    margin-left: 27px;
  }
  .run-time {
    &.race {
      color: #ff4e00;
    }
  }
}

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
</style>
