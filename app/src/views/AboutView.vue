<script setup>
import { miToKm } from "@/utils/helpers";
import {storeToRefs} from "pinia";
import {medalStore} from "@/store";
import MedalcaseBadge from "@/components/icons/MedalcaseBadge.vue";
const { selectedUnits } = storeToRefs(medalStore());
const breaks = [
  ['26.2', 'c_marathon', '26', '29', 'marathon'],
  ['50k', 'c_50k', '29', '48', 'ultra'],
  ['50mi', 'c_50mi', '48', '58', 'ultra'],
  [ '100k', 'c_100k', '58', '68', 'ultra'],
  ['100k+', 'c_100k_plus', '68', '98', 'ultra'],
  ['100mi', 'c_100mi', '98', '110', 'ultra'],
  ['Xtreme', 'c_xtreme', '110', '1000', 'ultra'],
];

</script>
<template>
    <div class="left-column"></div>
    <div class="center-column">
        <div>
            <p>Medalcase is simply a place to recognise your grit.</p>
            <p>It will catalogue run distances of marathon or more and give you the kudos you deserve for getting it
                done.</p>
            <p>All data is pulled from the Strava API so, "if it ain't on Strava it never happened".</p>
            <p>There is flexibility built in when classifying runs to allow for GPS variations. You can also re-classify
                your own runs if our matching system gets it wrong - it's an honour thing.</p>
            <div>
                Here are the break points between medal classifications:<br/>

                <div class="distance-bands">
                    <div class="m-class" v-for="(b, idx) in breaks" :key="b[0]">
                        <div class="m-name">
                          <MedalcaseBadge :class-name="b[1]" />
                        </div>
                        <div class="class-dist">

                            <div class="band">
                            {{ selectedUnits === 'mi' ? `${b[2]}mi` : `${miToKm(b[2])}km` }}
                            <span v-if="idx < breaks.length-1">
                            <i class="pi pi-arrow-right"></i>&nbsp;{{ selectedUnits === 'mi' ? `${b[3]}mi` : `${miToKm(b[3])}km` }}
                            </span>
                            <span v-else><i class="pi pi-plus"></i></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <p>&nbsp;</p>
            <p>&nbsp;</p>

        </div>
    </div>
    <div class="right-column"></div>


</template>

<style lang="scss">
.class-dist {
  text-align: left;
}
.distance-bands {
  display: flex;
  flex-wrap: wrap;
  .m-class {
    display: flex;
    align-items: center;
    margin: 12px 12px 0 0;
    flex-direction: column;
    .class-dist {
      padding: 0 8px;
      .name {
        font-weight: 800;
        text-align: center;
      }
    }
    .m-name {
      text-align: center;
      font-weight: bold;
      position: relative;
      .class-label {
        position: absolute;
        width: 100%;
        text-align: center;
        bottom: 30px;
        font-weight: 800;
        color: #ffffff;
      }
    }
  }
}

</style>
