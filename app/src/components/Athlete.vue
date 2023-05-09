<script setup>
import { onUnmounted, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { medalStore, CLASSES } from "@/store";
import { metersToDistanceUnits, getDate, secsToHMS } from "@/utils/helpers.js";
import {storeToRefs} from "pinia";
import { useConfirm } from "primevue/useconfirm";
import { useDialog } from "primevue/usedialog";
import { useToast } from "primevue/usetoast";
import { formatDate } from "@/utils/helpers.js";
import { socket, state } from "@/socket";
import PopOver from "@/components/PopOver.vue";
import RunEdit from "@/components/RunEdit.vue";
import AthleteMedalcase from "@/components/AthleteMedalcase.vue";
import AthletePhoto from "@/components/AthletePhoto.vue";
import MedalcaseLogo from "@/components/icons/MedalcaseLogo.vue";
import BadgeRace from "@/components/icons/BadgeRace.vue";
import BadgeRun from "@/components/icons/BadgeRun.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import RunsUpdate from "@/components/RunsUpdate.vue";

import ConnectionManager from "@/components/ConnectionManager.vue";

const props =  defineProps({
  currentUser: Boolean,
});

const { athlete, selectedUnits, units } = storeToRefs(medalStore());

const store = medalStore();
const route = useRoute();
const dialog = useDialog();
const toast = useToast();
const confirm = useConfirm();

const activeClasses = ref([]);
const dynamicDialogRef = ref(null);


const confirmDelete = () => {
  confirm.require({
    group: 'account',
    header: 'Confirm deletion of your Medalcase account',
    message: 'Are you sure you want to proceed? <br /> This will  <i><b>not</b></i> delete anything from your Strava account',
    icon: 'pi pi-exclamation-triangle',
    acceptIcon: 'pi pi-check',
    rejectIcon: 'pi pi-times',
    accept: () => {
      store.deleteAthlete().then(() => {
        toast.add({ severity: 'success', summary: 'Account deleted', detail: 'Thanks for stopping by! Your account has now been deleted', life: 5000 });
        store.doLogout();
      }, error => {
        console.log(error);
        toast.add({
          severity:'error',
          summary: error.response.name,
          detail: error.response.description, life: 3000 });
      });

    },
    reject: () => {
      toast.add({ severity: 'info', summary: 'Cancelled', detail: 'You have not deleted your account', life: 3000 });
    }
  });
};

const confirmDeleteRun = (run) => {
  confirm.require({
    group: 'account',
    header: `Remove: ${run.name}?`,
    message: 'Are you sure you want to proceed? <br /> You will not be able to re-sync just this run - you would have to delete your account and re-connect to rebuild all runs.',
    icon: 'pi pi-exclamation-triangle',
    acceptIcon: 'pi pi-check',
    rejectIcon: 'pi pi-times',
    accept: () => {
      store.deleteRun(run).then((response) => {
        store.refreshAthleteData(response);
        toast.add({ severity: 'success', summary: 'Run removed', detail: 'This run has been removed from Medalcase', life: 3000 });
      }, error => {
        console.log(error);
        toast.add({
          severity:'error',
          summary: error.name,
          detail: error.description, life: 3000 });
      });

    },
    reject: () => {
      toast.add({ severity: 'info', summary: 'Cancelled', detail: 'Run has not been removed', life: 3000 });
    }
  });
};

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

const resyncRun = (run) => {
  store.resyncRun(run).then((response) => {
    store.refreshAthleteData(response);
    toast.add({ severity: 'success', summary: 'Run updated', detail: 'This run has been re-synced from Strava data', life: 3000 });
    run.isLoading = false;
  }, error => {
    //console.log(error);
    run.isLoading = false;
    toast.add({
      severity:'error',
      summary: error.name,
      detail: error.description, life: 3000 });
  });
}
const fetchAthlete = () => {
  const athleteSlug = props.currentUser ? store.getSessionSlug : route.params.slug;
  if (athleteSlug) {
    store.getAthlete(athleteSlug).then((response) => {
      if (response.error){
        toast.add({ severity: 'error', summary: response.error.name, detail: response.error.description, life: 5000 });
      }
      else {
        //if (store.isOnboarding){
        //  updatesModal();
        //}
        activeClasses.value = store.athleteRuns ? CLASSES.filter((mclass) => store.athleteRuns[mclass.key]) : [];
      }
    });
  }
  else {
    toast.add({ severity: 'error', summary: "Error", detail: "Cannot find identifier for athlete", life: 5000 });
  }
}

const updatesModal = () => {
  dynamicDialogRef.value = dialog.open(RunsUpdate, {
    props: {
      header: "Scanning for new medals...",
      style: {
        width: '50vw',
      },
      breakpoints:{
        '960px': '75vw',
        '640px': '90vw'
      },
      modal: true
    },
    onClose: (closeMeta) => {
      console.log('onClose', closeMeta.data);
      if (closeMeta.data > 0) {
        toast.add({ severity: 'success', detail: "New medals added", life: 3000 });
        fetchAthlete();
      }
    }
  });
}

onMounted(() => {
  fetchAthlete();
});
onUnmounted(() => {
  socket.disconnect();
})
</script>

<template>
    <div v-if="store.isOnboarding" id="athlete-onboarding">
        <div class="container">
            <div class="left-column"></div>
            <div class="center-column">
                <div class="greet">
                  <div class="photo-logo">
                    <div class="pl-bg"><img src="/medalcase_logo.svg" /></div>
                    <div class="pl-img"><AthletePhoto :photo="athlete.photo" :size="100" /></div>
                  </div>
                  <div class="msg">Hi {{athlete.firstname}},
                    <br />
                    Welcome to Medalcase!
                  </div>
                </div>
                <p>Click below to scan all of your Strava runs for medals...</p>
                <Button label="Scan my runs" @click="updatesModal()"></Button>
            </div>
            <div class="right-column"></div>
        </div>
    </div>
    <div v-else id="athlete-medalcase">

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
                        <img v-if="athlete.country_code" :src="`/img/flags/${athlete.country_code}.svg`" class="a-flag"/>
                        <div v-if="currentUser" class="deleteme">
                            <a href="javascript:void(0);" @click="confirmDelete()"><font-awesome-icon icon="fa-light fa-trash-can" /> Delete Me</a>
                        </div>
                    </div>
                </div>

                <div class="tools-cont">
                    <div class="set-units"><SelectButton v-model="selectedUnits" :options="units" aria-labelledby="basic" /></div>
                    <div class="update-tools" v-if="currentUser" >
                        <div class="last-run-date">Last run: {{formatDate(athlete.last_run_date)}}</div>
                        <Button
                          @click="updatesModal()"
                          v-if="store.isLoggedIn"
                          severity="secondary"
                          outlined
                        >Update Medalcase <font-awesome-icon icon="fa-light fa-fw fa-arrows-rotate" fixed-width :spin="store.loadingLocal" /></Button>
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
                            <div class="run-dist">{{ metersToDistanceUnits(run.distance, selectedUnits)}}</div>
                          </div>
                          <div v-if="props.currentUser" class="run-tools">
                              <div class="update">
                                  <a href="javascript:void(0);" class="action" @click="resyncRun(run)"><font-awesome-icon icon="fa-light fa-fw fa-arrows-rotate" fixed-width :spin="run.isLoading" /></a>
                                  <a href="javascript:void(0);" class="action" @click="editRun(run)"><font-awesome-icon icon="fa-light fa-fw fa-pencil"  fixed-width /></a>
                              </div>
                              <div class="remove">
                                  <a href="javascript:void(0);" class="action" @click="confirmDeleteRun(run)"><font-awesome-icon icon="fa-light fa-fw fa-trash-can"  fixed-width /></a>
                              </div>
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
            <h3>No athlete found</h3>
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
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 30px;
  .center-column {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    .msg {
      margin-left: 12px;
    }
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
  .deleteme {
    font-size: 13px;
    margin-top: 8px;
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
    align-items: center;
    .set-units {
      padding: 12px;
    }
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
    .p-accordion-content {
      padding: 0;
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
    padding: 7px;
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
          height: 22px;
          flex: 0 0 22px;
          .badge {
            width: 100%;
            svg {
              width: 100%;
            }
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
      flex-direction: column;
      justify-content: flex-start;
      .update {
        display: flex;
      }
      .action {
        display: inline-block;
        margin: 0 4px;
      }
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
@media screen and (max-width: 480px){
  #case-summary {
    .run-single {
      flex-direction: column;
      .run-info {
        .run-date {
          padding-top: 6px;
        }
      }
    }
    .run-list {
      .run-tools {
        flex: 1;
        flex-direction: row-reverse;
        justify-content: flex-start;
        .action {
          margin: 0 12px;
          padding: 0 6px;
        }
      }
      .run-stats {
        display: flex;
        align-items: center;
        padding-left: 37px;
        .run-time {

        }
        .run-dist {
          padding-left: 12px;
        }
      }
    }
  }
}
</style>
