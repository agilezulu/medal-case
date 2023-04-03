<script setup>
import { medalStore } from "@/store";
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

const store = medalStore();
const labels = store.runsByMile.map(run => run.mile);
const data = store.runsByMile.map(run => run.count);

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const chartData = {
  labels: labels,
  datasets: [ { data: data } ]
};
const chartOptions = {
  responsive: true,
  indexAxis: 'y',

};
</script>
<template>
  <Bar
      id="my-chart-id"
      :options="chartOptions"
      :data="chartData"
      :height="600"
  />
</template>
