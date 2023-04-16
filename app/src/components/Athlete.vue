<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { medalStore } from "@/store";
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

const { athlete } = storeToRefs(medalStore());
const store = medalStore();
const route = useRoute();
const dialog = useDialog();
const toast = useToast();

const buildRuns = () => {
  let newRuns = store.buildAthleteRuns();
  //console.log('UPDATED', newRuns);

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

      <div class="update-tools">
        <a href="javascript:void(0);"
            @click="buildRuns()"
            class="p-button p-component p-button-secondary p-button-outlined p-button-sm"
            v-if="store.isLoggedIn"
        >Update Medalcase <font-awesome-icon icon="fa-light fa-arrows-rotate" fixed-width /></a>
        <div class="last-run-date">{{formatDate(athlete.last_run_date)}}</div>
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
                    <div class="class-count">
                      <div class="medal-bg">
                        <MedalcaseLogo border="currentColor" center="#ffffff" />
                      </div>
                      <div class="count">
                        <span>{{athlete[runClass.gKey]}}</span>
                      </div>
                    </div>
                    <div class="class-count">
                      <div class="medal-bg">
                        <MedalcaseLogo border="currentColor" center="#ffffff" />
                      </div>
                      <div class="count">
                        <span :class="runClass.class_key"> {{athlete[`${runClass.gKey}_race`]}}</span>
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
@import "@/assets/mixins.scss";
$bordercolor1: #bbbbbb;
$backgroundcolor1: #dddddd;
$width1: 60px;
$borderwidth1: 4px;
$borderradius1: 0;

$bordercolor2: #ffbbbb;
$backgroundcolor2: #ffdddd;
$width2: 80px;
$borderwidth2: 4px;
$borderradius2: 4px;

.hex-holder {
  position: relative;
  @include hexagon(60px, #eeeeee, 2px, #aaaaaa);
}
#case-header {
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

        .medal-bg {
          position: absolute;
          width: 60px;
          top: -16px;
        }

        .count {
          position: relative;
          z-index: 12;
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
