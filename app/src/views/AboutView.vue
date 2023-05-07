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
  ['100k+', 'c_100kplus', '68', '98', 'ultra'],
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
                <table>
                    <tbody>
                    <tr v-for="(b, idx) in breaks" :key="b[0]">

                        <td class="m-name">
                          <MedalcaseBadge :class-name="b[1]" />
                            <div class="class-label">{{b[0]}}</div>
                        </td>
                        <td class="class-dist">
                            {{ selectedUnits === 'mi' ? `${b[2]}mi` : `${miToKm(b[2])}km` }}
                        </td>
                        <td class="class-dist">
                            <span v-if="idx < breaks.length-1">
                            {{ selectedUnits === 'mi' ? `${b[3]}mi` : `${miToKm(b[3])}km` }}
                            </span>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
            <p>&nbsp;</p>
            <p>&nbsp;</p>

        </div>
    </div>
    <div class="right-column"></div>


</template>

<style lang="scss">
.class-dist {
  text-align: right;
}
.m-name {
  text-align: center;
  font-weight: bold;
  width: 105px;
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
</style>
