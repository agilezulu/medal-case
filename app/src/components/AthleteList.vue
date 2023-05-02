<script setup>
import { ref } from "vue";
import { medalStore, CLASSES } from "@/store";
import { storeToRefs } from "pinia"
import { FilterMatchMode } from 'primevue/api';
import MedalcaseLogo from "@/components/icons/MedalcaseLogo.vue";
import AthletePhoto from "@/components/AthletePhoto.vue";

const { athleteList } = storeToRefs(medalStore())
const { getAthletes } = medalStore();

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
});

getAthletes();
</script>

<template>
  <div id="athlete-list">

      <DataTable v-model:filters="filters" :value="athleteList" paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
                 currentPageReportTemplate="{first} to {last} of {totalRecords}"  paginator :rows="45" :rowsPerPageOptions="[45, 90, 150]"
                 :globalFilterFields="['firstname', 'lastname']" class="p-datatable-sm">

        <template #header>
          <div class="flex justify-content-between align-items-center table-header">
            <div class="">
              <div class="table-title">Medalcase Athletes</div>
            </div>
            <div class="">
              <span class="p-input-icon-left">
                  <i class="pi pi-search" />
                  <InputText v-model="filters['global'].value" placeholder="Search by name" />
              </span>
            </div>
          </div>
        </template>
        <template #empty> No athletes found. </template>
        <template #loading> Loading athletes. Please wait. </template>

        <Column field="firstname" header="Name" :sortable="true">
          <template #body="slotProps">
            <div class="athlete-name">
              <div class="photo-bg"><MedalcaseLogo border="#FD4B01" center="#ffffff" /></div>
              <AthletePhoto :photo="slotProps.data.photo" :size="70" />
              <router-link :to="{ name: 'athlete', params: { slug: slotProps.data.slug } }" class="name-link">{{slotProps.data.firstname}} {{slotProps.data.lastname}}</router-link>
            </div>
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
          <Column :field="runClass.key" :header="runClass.name" headerStyle="width: 75px;" >
            <template #body="slotProps">
              <div class="run-count" :class="runClass.key">
                <div class="medal-bg"><MedalcaseLogo :border="slotProps.data[runClass.key] ? 'currentColor' : '#dddddd'" :center="slotProps.data[runClass.key] ? '#ffffff' : '#ffffff'" /></div>
                <div class="medal-stats">
                  <div class="medal-count">{{slotProps.data[runClass.key]}}</div>
                </div>
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
  .p-datatable-header {
    padding: 8px;
    .table-header {
      .table-title {
        font-size: 1.2rem;
      }
    }
  }
  .athlete-name {
    position: relative;
    display: flex;
    align-items: center;
    .photo-bg {
      width: 49px;
      left: -7px;
      position: absolute;
      top: -12px;
    }
    .name-link {
      margin-left: 43px;
    }
  }
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
      justify-content: center;
    }
    .p-sortable-column {
      .p-column-header-content {
        justify-content: start;
      }
    }

    .run-count {
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      width: 100%;
      height: 40px;
      .medal-bg {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        display: flex;
        justify-content: center;
      }
      .medal-stats {
        z-index: 5;
      }
    }
  }
}
</style>
