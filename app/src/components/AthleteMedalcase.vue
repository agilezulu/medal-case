<script setup>
import { classRows, CLASSES } from "@/store";
import MedalcaseLogo from "@/components/icons/MedalcaseLogo.vue";
import {computed} from "vue";
const props = defineProps({
  athlete: Object,
  required: true
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

</script>

<template>
  <div class="athlete-medalcase">
    <div class="athlete-info">
      {{athlete.firstname}}
      {{athlete.lastname}}
    </div>
    <div  class="athlete-medals">

      <div class="mcase-row">
        <div class="mcase-class">
          <div class="medal-bg"><img src="/medalcase_logo.svg" class="class-medal" /></div>
          <div class="medal-stats">
            <span class="medal-name">Total</span>
            <span class="medal-count">{{totalMedals.runs}}</span>
            <span class="medal-count-race">({{totalMedals.races}})</span>
          </div>
        </div>
      </div>
      <div v-for="(row, idx) in classRows" class="mcase-row" :key="idx">
        <div v-for="c in row" class="mcase-class" :class="c.key" :key="c.key">
          <div class="medal-bg">
            <img v-if="c.key === 'c_marathon'" src="/c_marathon.svg" />
            <MedalcaseLogo v-else :border="athlete[c.key] ? 'currentColor' : '#999999'" :center="athlete[c.key] ? '#ffffff' : '#dddddd'" />
          </div>
          <div class="medal-stats">
            <div class="medal-count">{{athlete[c.key]}}</div>
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
  margin-top: $stack-margin-top;
  .athlete-medals {
    display: flex;
    flex-direction: column;
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
            border: solid 3px #666666;
            background-color: rgba(255,255,255,0.5);
            height: 34px;
            width: 105px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
          }
          .medal-name {
            font-size: 1.2rem;
            font-weight: 800;
          }
        }
      }
    }
  }
}
</style>
