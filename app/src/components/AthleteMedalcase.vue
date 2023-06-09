<script setup>
import {classRows, CLASSES, medalStore} from "@/store";
import MedalcaseLogo from "@/components/icons/MedalcaseLogo.vue";
import MedalcaseBadge from "@/components/icons/MedalcaseBadge.vue";
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
      <div class="hexgrid">
          <div class="main">
              <div class="container-hex">
                  <div class="mcase-class ">
                      <div class="medal-bg"><img src="/medalcase_logo.svg" alt="Athlete Medalcase Number" class="class-medal" /></div>
                      <div class="medal-stats total">
                          <span class="medal-count">{{totalMedals.runs}}</span>
                      </div>
                  </div>
                  <!-- :class="[ athlete[c.key] > 0 ? `${c.key}_bgbadge` : `${c.key}_bgbadge_notyet` ]"  -->
                  <div v-for="c in CLASSES" class="mcase-class" :key="c.key">
                      <div class="medal-bg"><img :src="`/img/${c.key}${athlete[c.key] > 0 ? '': '_notyet'}.png`" :alt="c.name" class="class-medal" /></div>
                      <div class="medal-stats badge">
                          <!--  :class="`${c.key}_badgecount`" -->
                          <div v-if="athlete[c.key] > 0" class="medal-count badge">{{athlete[c.key]}}</div>
                          <div v-else class="medal-count notyet">not yet</div>
                      </div>
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

$s: 170px;  /* size  */
$m: 2px;    /* margin */
$f: calc($s * 1.732 + 4 * $m - 1px);

.main {
  display:flex;
  padding: 12px 0 0 12px;
  .container-hex {
    font-size: 0;
    .mcase-class {
      position: relative;
      width: $s;
      margin: $m;
      height: calc($s * 1.1547);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size:initial;
      clip-path: polygon(0% 25%, 0% 75%, 50% 100%, 100% 75%, 100% 25%, 50% 0%);
      margin-bottom: calc($m - $s * 0.2885);
      background-color: #ffffff;
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;

      .medal-bg {
        position: absolute;
        left: 0;
        top: 0;
        right: 0;
        bottom: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        .class-medal {
          height: 100%;
        }
      }
      .medal-stats {
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
        color: #ffffff;
        bottom: 0;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        .medal-count {
          font-size: 30px;
          font-weight: 800;
          border-radius: 50%;
          width: 60px;
          height: 60px;
          display: flex;
          justify-content: center;
          align-items: center;
          &.badge {
            @supports (-webkit-text-stroke: 1px #333333) {
              -webkit-text-stroke: 1px #333333;
              -webkit-text-fill-color: #ffffff;
            }
            text-shadow: 2px 3px 6px #000000,  -2px 3px 6px #333333;
          }
          &.notyet {
            color: #888888;
            font-size: 16px;
            text-shadow: 2px 3px 6px #ffffff, -2px 3px 6px #ffffff;
          }
        }
      }
    }
    &::before {
      content: "";
      width: calc($s / 2 + $m);
      float: left;
      height: 120%;
      shape-outside: repeating-linear-gradient(#0000 0 calc($f - 3px), #000 0 $f);
    }
  }
}

.athlete-medalcase {
  position: relative;
  margin-bottom: 60px;
  display: flex;
  justify-content: center;
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
  }
  @media (max-width: 795px) {
    .athlete-medals {
      margin-bottom: 120px;
    }
  }
  @media (max-width: 549px) {
    margin-bottom: 200px;
  }
}
</style>
