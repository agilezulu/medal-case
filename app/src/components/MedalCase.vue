<script setup>
import { medalStore } from "@/store";
import { onMounted, computed } from "vue";
import { metersToDistanceUnits, getDate, secsToHMS } from "@/utils/helpers.js";
import ChartBar from "@/components/ChartBar.vue";

const store = medalStore();

onMounted(() => {
  store.getRuns();
});
</script>

<template>
  <div id="case-header">
    Runs: {{store.runs.totals.runs}} - {{ metersToDistanceUnits(store.runs.totals.distance, 'mi')}}mi
    <div>
      <SelectButton v-model="store.selectedUnits" :options="store.units" aria-labelledby="basic" />
    </div>
  </div>
  <div id="case-summary">
    <!--
    <div class="run-type by-mile">
      <ChartBar />

      <table>
        <tbody>
          <tr v-for="dist in store.runsByMile" :key="dist.mile">
            <td>{{dist.mile}}</td>
            <td>{{dist.count}}</td>
          </tr>
        </tbody>
      </table>

    </div>
    -->
    <div v-for="runclass in store.classes" :key="runclass.getter" class="run-type" :class="runclass.classname">
      <div class="class-header">
        <div class="run-class">{{runclass.name}}</div>
        <div class="run-class-meta">
          <div class="meta"><span class="meta-key">Total</span><span class="meta-val">{{store.runs.classes[runclass.classname].tot}}</span></div>
          <template v-if="runclass.classname === 'ultra'">
            <div v-for="(value, key) in store.runs.classes.ultra.subclass" class="meta">
              <span class="meta-key">{{key}}</span><span class="meta-val">{{value}}</span>
            </div>
          </template>
        </div>
      </div>
      <div class="class-body">
        <table>
          <tbody>
          <tr v-for="(run, index) in store[runclass.getter]" :key="run.id">
            <td class="idx">{{index+1}}</td>
            <td>
              <div class="run-title"><a :href="`https://www.strava.com/activities/${run.id}/overview`" target="_new">{{run.name}}</a></div>
              <div class="run-date">{{getDate(run.start_date_local)}}</div>
            </td>
            <td>
              <div class="run-time" :class="{ race :run.race }">{{ secsToHMS(run.elapsed_time)}}</div>
              <div class="run-dist">{{ metersToDistanceUnits(run.distance, 'mi')}}</div>
            </td>
          </tr>
          </tbody>
        </table>
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
    .class-body {
      padding: 12px;
      max-height: 500px;
      overflow-y: scroll;
    }
  }
  .run-title {
    font-weight: 600;
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
