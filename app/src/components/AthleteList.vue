<script setup>
import { medalStore, CLASSES } from "@/store";
import { storeToRefs } from "pinia";
const { athleteList } = storeToRefs(medalStore())
const { getAthletes } = medalStore();

getAthletes();
</script>

<template>
  <div id="athlete-list">
    <h2 class="green">Medalcase Athletes</h2>

      <!--
                 paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
                 currentPageReportTemplate="{first} to {last} of {totalRecords}"  paginator :rows="45" :rowsPerPageOptions="[45, 90, 150]" -->
      <DataTable :value="athleteList">

        <Column field="firstname" header="Name" headerStyle="text-align: left;" :sortable="true">
          <template #body="slotProps">
            <router-link :to="{ name: 'athlete', params: { slug: slotProps.data.slug } }">{{slotProps.data.firstname}} {{slotProps.data.lastname}}</router-link>
          </template>
        </Column>
        <Column field="total_medals" header="Total" :sortable="true">
          <template #body="slotProps">
            <div class="athelete-total">
              <div class="total-bg"><img src="/medalcase_logo.svg" /></div>
              <div class="total-count">{{slotProps.data.total_medals}}</div>
            </div>

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
</template>

<style lang="scss">
$total-size: 50px;
#athlete-list {
  .athelete-total {
    display: flex;
    position: relative;
    width: $total-size;
    height: $total-size;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-weight: 800;
    .total-bg {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      img {
        width: 100%;
      }
    }
    .total-count {
      z-index: 5;
    }

  }
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
