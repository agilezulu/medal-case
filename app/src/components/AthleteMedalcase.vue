<script setup>
import {classRows, CLASSES, medalStore} from "@/store";
import MedalcaseLogo from "@/components/icons/MedalcaseLogo.vue";
import {computed} from "vue";
import {secsToHMS, metersToDistanceUnits} from "@/utils/helpers.js";
import {storeToRefs} from "pinia";
import AthletePhoto from "@/components/AthletePhoto.vue";

const { selectedUnits } = storeToRefs(medalStore());
//const store = medalStore();

const props = defineProps({
  athlete: Object
})

const totalMedals = computed(() => {
  return CLASSES.reduce((acc, obj) => {
    let key = obj.key;

    if (props.athlete[`${key}_race`]) {
      acc.races += props.athlete[`${key}_race`];
    }
    if (props.athlete[key]) {
      acc.runs += props.athlete[key];
    }
    return acc;
  }, {
    runs: 0,
    races: 0
  });
});
const pbMarathon = computed(() => {
  let pb = 100000;
  props.athlete.runs.forEach((run) => {
    if (run.class_key === "c_marathon" && run.elapsed_time < pb) {
      pb = run.elapsed_time;
    }
  });
  return secsToHMS(pb);
});

</script>

<template>
  <div class="athlete-medalcase">
    <div class="athlete-info">
      <div class="photo-logo">
        <div class="pl-bg"><img src="/medalcase_logo.svg" /></div>
        <div class="pl-img"><AthletePhoto :photo="athlete.photo" :size="100" /></div>
      </div>
      <div class="info">
        <div class="a-name">{{athlete.firstname}} {{athlete.lastname}}</div>
        <div class="stats">
          <div class="a-stat">
            <div class="stat-name">Total runs</div>
            <div class="stat-value">{{athlete.total_runs}}</div>
          </div>
          <div class="a-stat">
            <div class="stat-name">Total distance</div>
            <div class="stat-value">{{metersToDistanceUnits(athlete.total_distance, selectedUnits)}}</div>
          </div>
          <div class="a-stat">
            <div class="stat-name">26.2 PB</div>
            <div class="stat-value">{{pbMarathon}}</div>
          </div>
        </div>
      </div>
    </div>

    <div  class="athlete-medals">
      <div class="mcase-row">
        <div class="mcase-class">
          <div class="medal-bg"><img src="/medalcase_logo.svg" class="class-medal" /></div>
          <div class="medal-stats total">
            <span class="medal-name">{{totalMedals.runs}}</span>
          </div>
        </div>
      </div>
      <div v-for="(row, idx) in classRows" class="mcase-row" :key="idx">
        <div v-for="c in row" class="mcase-class" :class="[ athlete[c.key] > 0 ? c.key : 'disabled' ]" :key="c.key">
          <div class="medal-bg">
            <!-- <img v-if="c.key === 'c_marathon'" src="/c_marathon.svg" /> -->
            <MedalcaseLogo :border="athlete[c.key] ? 'currentColor' : '#999999'" :center="athlete[c.key] ? '#ffffff' : '#dddddd'" />
          </div>
          <div class="medal-stats">
            <div class="medal-count" :class="`${c.key}_border`">{{athlete[c.key]}}</div>
            <div class="medal-name">{{c.name}}</div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
$medal-width: 200px;
$stack-margin-top: calc($medal-width / 4)-2;
$stack-margin-lr: calc($medal-width / 16);
.athlete-medalcase {
  position: relative;
  .athlete-info {
    display: flex;
    position: absolute;
    top: 12px;
    .photo-logo {

    }
    .info {
      margin-left: 8px;
    }
    .a-name {
      font-size: 1.3rem;
      font-weight: 800;
    }
    .stats {

      .a-stat {
        display: flex;
        align-items: center;

        .stat-name {
          font-weight: 800;
        }

        .stat-value {
          text-align: right;
          padding: 3px 8px;
        }
      }
    }
  }
  .athlete-medals {
    display: flex;
    flex-direction: column;
    padding-top: 55px;
    .bg-container {
      position: relative;
      flex: 1;
    }
    .medal-bg {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      display: flex;
      justify-content: center;
      .class-medal {
        width: 100%;
      }
      &.outer-bg {
        display: flex;
        justify-content: center;

        height: 700px;

        .class-medal {
          position: relative;

        }
      }
    }
    .mcase-row {
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      .mcase-class {
        display: flex;
        width: $medal-width;
        height: $medal-width;
        position: relative;
        justify-content: center;

        margin-top: -$stack-margin-top;
        margin-left: -$stack-margin-lr;
        margin-right: -$stack-margin-lr;


        .medal-stats {
          position: relative;
          display: flex;
          flex-direction: column;
          justify-content: flex-end;
          align-items: center;
          width: 100%;
          bottom: 34px;
          .medal-count {
            border-width: 5px;
            border-style: solid;
            background-color: rgba(255,255,255,0.5);
            height: 44px;
            width: 105px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.5rem;
            color: #333333;
          }
          .medal-name {
            font-size: 1.2rem;
            font-weight: 800;
          }
          &.total {
            justify-content: center;
            .medal-name {
              position: relative;
              font-size: 42px;
              font-weight: 800;
              top: 34px;
              color: #ffffff;
            }
          }
        }
        &.disabled {
          .medal-stats {
            color: #777777;
            justify-content: center;
            margin-top: 67px;
            .medal-count {
              display: none;
            }
          }
        }
      }
    }
  }
  @media (max-width: 549px) {
    .athlete-medals {
      .mcase-row {
        .mcase-class {
          margin-top: 0;
        }
      }
    }
  }
}
</style>
