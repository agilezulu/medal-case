<script setup>
import { onMounted, computed, ref, getCurrentInstance } from "vue";
import { useRoute } from "vue-router";
import { medalStore, CLASSES } from "@/store";
import { metersToDistanceUnits, getDate, secsToHMS } from "@/utils/helpers.js";
import {storeToRefs} from "pinia";
import { useDialog } from "primevue/usedialog";
import { useToast } from "primevue/usetoast";
import { groupBy } from "@/utils/helpers.js";
import RunEdit from "@/components/RunEdit.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const { loading, athlete } = storeToRefs(medalStore())
const store = medalStore();
const route = useRoute();
const dialog = useDialog();
const toast = useToast();

const classKeys = CLASSES.map(c => c.key);
//.sort((a, b) => classKeys.indexOf(a.gKey) - classKeys.indexOf(b.gKey)
const groupedRuns = computed(() => {
  let grouped = groupBy(store.athleteRuns, "class_key", ["class", "class_key"], "start_date_local");
  let groupedSorted = Object.entries(grouped).sort((a, b) => classKeys.indexOf(a.gKey) - classKeys.indexOf(b.gKey));
  return groupedSorted.map(gs => gs[1]);
});
const buildRuns = () => {
  store.buildAthleteRuns();
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
    onClose: (options) => {
      const data = options.data;
      console.log('CLOSED', data);
      if (data) {
        toast.add({ severity:'info', data, life: 3000 });
      }
    }
  });

}

onMounted(() => {
  store.getAthlete(route.params.slug);

});
</script>

<template>
  <div v-if="loading">
    <LoadingSpinner />
  </div>
  <div v-else>
    <div id="case-header">
      <!--
      Runs:
      <div>
        <SelectButton v-model="store.selectedUnits" :options="store.units" aria-labelledby="basic" />
      </div>
      -->
      {{athlete.firstname}}
      {{athlete.lastname}}

      <Button
          @click="buildRuns()"
          class="p-button-outlined p-button-secondary p-button-sm"
          v-if="store.isLoggedIn"
      >Build Medalcase <font-awesome-icon icon="fa-light fa-arrows-rotate" /></Button>
    </div>
    <div id="case-summary">

        <div class="class-body">
          <!--
          <div class="hex-holder">
                    <div class="hex"></div>
                    <div class="hex-content"></div>
                  </div>
          -->

          <Accordion class="accordion-custom" :multiple="true" :activeIndex="[0]">
            <template v-for="runClass in store.athleteRuns" :key="runClass.gKey">
            <AccordionTab>
              <template #header>
                <div class="run-class">
                  <div class="class-name">{{ runClass.class }}</div>
                  <div class="class-count">{{runClass.gCount}}  <sup :class="runClass.class_key"><font-awesome-icon icon="fa-light fa-medal" /> {{runClass.gRaceCount}}</sup></div>

                </div>
              </template>
              <div class="run-list">
                <div v-for="(run, idx) in runClass.gVal" :key="run.strava_id" class="run-single">

                  <div class="run-info">

                    <div class="run-title">
                      <span class="run-idx">{{idx+1}}</span>
                      <span class="run-ico" :class="run.race ? runClass.class_key : 'c_training'"><font-awesome-icon :icon="`fa-fw fa-light ${run.race? 'fa-medal' : 'fa-person-running'}`" /></span>
                      <a :href="`https://www.strava.com/activities/${run.strava_id}/overview`" target="_new" class="run-name" :class="run.race ? runClass.class_key : 'c_training'">{{run.name}} <font-awesome-icon icon="fa-light fa-arrow-up-right-from-square" transform="shrink-4 up-6" /></a>
                    </div>
                    <div class="run-date">{{getDate(run.start_date_local)}}</div>
                  </div>
                  <div class="run-stats">
                    <div class="run-time" :class="run.race ? runClass.class_key : ''">{{ secsToHMS(run.elapsed_time)}}</div>
                    <div class="run-dist">{{ metersToDistanceUnits(run.distance, 'mi')}}</div>
                  </div>
                  <div class="run-tools">
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
  .p-button {
    padding: 0px 12px;
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


  .run-class {
    display: flex;
    flex: 1;
    justify-content: space-between;
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
    width: 600px;
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
          padding-right: 6px;
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
  .run-type {
    margin: 12px;
    border: solid 1px #dddddd;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    flex: 1 1 0px;
    min-width: 360px;
    .class-header {
      display: flex;
      flex-direction: column;
      align-items: center;
      .run-class {
        width: 100%;
        text-align: center;
        line-height: 2;
        font-size: 1.2rem;
        font-weight: 800;
        background-color: #eeeeee;
      }
      .run-class-meta {
        display: flex;
        padding: 6px;
        flex-wrap: wrap;
        .meta {
          border: solid 1px #dddddd;
          border-radius: 12px;
          line-height: 1.5;
          margin-right: 12px;
          margin-bottom: 6px;
          .meta-key {
            background-color: #eeeeee;
            border-radius: 12px;
            border-right: solid 1px #dddddd;
            padding: 0 10px;
            font-weight: 800;
          }
          .meta-val {
            padding: 0 10px;
          }

        }
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
  .run-time {
    &.race {
      color: #ff4e00;
    }
  }
}
</style>
