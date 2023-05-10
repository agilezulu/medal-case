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
const sortMeta = [
  {field: "total_medals", order: -1},
  {field: "c_xtreme", order: -1},
  {field: "c_100mi", order: -1},
  {field: "c_100k_plus", order: -1},
  {field: "c_100k", order: -1},
  {field: "c_50mi", order: -1},
  {field: "c_50k", order: -1},
  {field: "c_marathon", order: -1},
  {field: "firstname", order: 1},
]

getAthletes();
</script>

<template>
  <div id="athlete-list">

      <DataTable v-model:filters="filters"
                 :value="athleteList"
                 sortMode="multiple"
                 :multiSortMeta="sortMeta"
                 paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
                 currentPageReportTemplate="{first} to {last} of {totalRecords}"
                 paginator :rows="50"
                 :rowsPerPageOptions="[50, 100, 200]"
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
              <AthletePhoto :photo="slotProps.data.photo" :size="50" />
              <router-link :to="{ name: 'athlete', params: { slug: slotProps.data.slug } }" class="name-link">{{slotProps.data.firstname}} {{slotProps.data.lastname}}</router-link>
              <img :src="`/img/flags/${slotProps.data.country_code}.svg`" class="a-flag"/>
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
          <Column :field="runClass.key" :header="runClass.name" headerStyle="width: 75px;" :sortable="true">
            <template #body="slotProps">
              <div class="run-count" :class="runClass.key">
                <div class="medal-bg"><MedalcaseLogo :border="slotProps.data[runClass.key] ? 'currentColor' : '#dddddd'" :center="slotProps.data[runClass.key] ? '#ffffff' : '#ffffff'" /></div>
                <div class="medal-stats" v-if="slotProps.data[runClass.key] > 0">
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
    .a-flag {
      max-width: 25px;
      max-height: 25px;
    }
    .hex-photo {
      position: relative;
      width: 50px;
      height: 50px;
      .photo-bg {
        width: 43px;
        left: 4px;
        position: absolute;
      }
      .a-photo.hexagon {
        left: 8px;
        top: -9px;
      }
    }

    .name-link {
      padding: 0 6px;
      flex: 1;
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
      top: -4px;
      left: 0;
      img {
        width: 100%;
      }
    }
    .total-count {
      z-index: 5;
      font-size: 15px;
    }

  }
  .p-datatable {
    .p-datatable-wrapper {
      overflow: visible;
      overflow-x: scroll;
      overflow-y: hidden;
      height: 100%;
    }
    .p-column-header-content {
      align-items: center;
      justify-content: center;
    }
    .p-sortable-column {
      .p-column-header-content {
        justify-content: start;
      }
      .p-sortable-column-badge {
        display: none;
      }
      &.p-highlight {
        color: #333333;

      }
      .p-sortable-column-icon {
        font-size: 12px;
        color: #333333;
        margin-left: 3px;
        margin-top: -10px;
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
        svg {
          height: 100%;
        }
      }
      .medal-stats {
        z-index: 5;
      }
    }
  }
}
</style>
