<script setup>
import { medalStore, CLASSES } from "@/store";
import { storeToRefs } from "pinia";
import { metersToDistanceUnits, getDate, secsToHMS } from "@/utils/helpers.js";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const { athleteList, loading } = storeToRefs(medalStore())
const { getAthletes } = medalStore();

getAthletes();
</script>

<template>
  <div id="athlete-list">
    <h2 class="green">Medalcase Athletes</h2>
    <div v-if="loading"><LoadingSpinner /></div>
    <div v-else>
      <DataTable :value="athleteList" stripedRows tableStyle="min-width: 50rem" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]"
                 paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
                 currentPageReportTemplate="{first} to {last} of {totalRecords}">
        <Column field="firstname" header="Name" headerStyle="text-align: left;" :sortable="true">
          <template #body="slotProps">
            <router-link :to="{ name: 'athlete', params: { slug: slotProps.data.slug } }">{{slotProps.data.firstname}} {{slotProps.data.lastname}}</router-link>
          </template>
        </Column>
        <template v-for="runClass in CLASSES" :key="runClass.key">
          <Column :field="runClass.key" :header="runClass.name" headerStyle="text-align: right;" >
            <template #body="slotProps">
              <div class="run-count">
                <span>{{slotProps.data[runClass.key] || '-'}}</span>
              </div>
            </template>
          </Column>
        </template>
      </DataTable>
    </div>
  </div>
</template>

<style lang="scss">
#athlete-list {
  .p-datatable {
    .p-column-header-content {
      align-items: center;
      display: block;
    }

    .run-count {
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style>
