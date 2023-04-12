<script setup>
import { ref, onMounted, computed } from "vue";
import { medalStore } from "@/store";
import { metersToDistanceUnits, getDate, secsToHMS } from "@/utils/helpers.js";
import {storeToRefs} from "pinia";
import { groupBy } from "@/utils/helpers.js";

const { loading, medalcase } = storeToRefs(medalStore())

const { getRuns, athleteRuns } = medalStore();

const groupedRuns = computed(() => {
  return groupBy(athleteRuns, "class_key", ["class", "class_key"], "start_date_local");
})

onMounted(() => {
  getRuns();
});
</script>

<template>
  <div v-if="loading">
    Loading...
  </div>
  <div v-else>

    <div id="case-header">
      <!--
      Runs:
      <div>
        <SelectButton v-model="store.selectedUnits" :options="store.units" aria-labelledby="basic" />
      </div>
      -->
      {{medalcase.athlete.firstname}}
      {{medalcase.athlete.lastname}}
    </div>
    <div id="case-summary">

        <div class="class-body">
          <!--
          <div v-for="runClass in athleteRuns" :key="runClass.gKey" class="r-category col-12">
            <div class="run-class">
              <div class="class-name">{{ runClass.class }}</div>
              <div class="class-count">{{runClass.gCount}}</div>
            </div>
            <div class="grid">
              <div v-for="run in runClass.gVal" :key="run.strava_id" class="run-single col-12 md:col-6 lg:col-3">

                <div class="run-title">
                  <div class="run-title"><a :href="`https://www.strava.com/activities/${run.strava_id}/overview`" target="_new">{{run.name}}</a></div>
                  <div class="run-date">{{getDate(run.start_date_local)}}</div>
                </div>
                <div class="run-stats">
                <div class="run-time" :class="{ race: run.race }">{{ secsToHMS(run.elapsed_time)}}</div>
                <div class="run-dist">{{ metersToDistanceUnits(run.distance, 'mi')}}</div>
                </div>
              </div>
            </div>
          </div>
          -->

          <Accordion class="accordion-custom" :multiple="true" :activeIndex="[0]">
            <template v-for="runClass in groupedRuns" :key="runClass.gKey">
            <AccordionTab>
              <template #header>
                <div class="run-class">
                  <div class="class-name">{{ runClass.class }}</div>
                  <div class="class-count">{{runClass.gCount}}</div>
                </div>
              </template>
              <div class="run-list">
                <div v-for="(run, idx) in runClass.gVal" :key="run.strava_id" class="run-single col-12 md:col-6 lg:col-3">

                  <div class="run-info">

                    <div class="run-title">
                      <span class="run-idx">{{idx+1}}</span>
                      <a :href="`https://www.strava.com/activities/${run.strava_id}/overview`" target="_new" class="run-name" :class="runClass.class_key">{{run.name}} <i class="pi pi-external-link" style="font-size: 0.6rem; top: -7px;"></i></a>
                    </div>
                    <div class="run-date">{{getDate(run.start_date_local)}}</div>
                  </div>
                  <div class="run-stats">
                    <div class="run-time" :class="run.race ? runClass.class_key : ''">{{ secsToHMS(run.elapsed_time)}}</div>
                    <div class="run-dist">{{ metersToDistanceUnits(run.distance, 'mi')}}</div>
                  </div>
                </div>
              </div>
            </AccordionTab>
            </template>
          </Accordion>


          <!--
          <DataTable v-model:expandedRowGroups="expandedRowGroups" :value="athleteRuns" tableStyle="min-width: 50rem"
                     expandableRowGroups rowGroupMode="subheader" groupRowsBy="class_key"
                     sortMode="single" sortField="distance" :sortOrder="1">

            <Column field="name" header="Name">
              <template #body="slotProps">
                <div class="run-title"><a :href="`https://www.strava.com/activities/${slotProps.data.strava_id}/overview`" target="_new">{{slotProps.data.name}}</a></div>
                <div class="run-date">{{getDate(slotProps.data.start_date_local)}}</div>
              </template>
            </Column>
            <Column field="elapsed_time" header="Time">
              <template #body="slotProps">
                <div class="run-time" :class="{ race: slotProps.data.race }">{{ secsToHMS(slotProps.data.elapsed_time)}}</div>
                <div class="run-dist">{{ metersToDistanceUnits(slotProps.data.distance, 'mi')}}</div>
              </template>
            </Column>
            <template #groupheader="slotProps">
              <pre>{{slotProps}}</pre>
              <span class="vertical-align-middle font-bold line-height-3">{{ slotProps.data.class }}</span>
            </template>
          </DataTable>
          -->
        </div>
      </div>

  </div>
</template>

<style lang="scss">
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
      .run-title {
        display: flex;

        .run-name {
          font-weight: 700;
        }
        .run-idx {
          min-width: 20px;
          text-align: right;
          padding-right: 8px;
          font-weight: 200;
          color: #555555;
        }
      }
      .run-date {
        padding-left: 22px;
      }
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
