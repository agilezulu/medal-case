<script setup>
import { ref, onMounted, inject } from "vue";
import { medalStore, CLASSES } from "@/store";
import {metersToDistanceUnits, metersToDistanceValue, secsToHMS, metersFromDistanceUnits} from "@/utils/helpers.js";
import { useToast } from "primevue/usetoast";

const runToEdit = ref(0);
const dialogRef = inject("dialogRef");
const store = medalStore();
const toast = useToast();

onMounted(() => {
  runToEdit.value = JSON.parse(JSON.stringify(dialogRef.value.data.run));

  runToEdit.value.hms = secsToHMS(runToEdit.value.elapsed_time);
  let timeUnits = runToEdit.value.hms.split(':');
  runToEdit.value.hh = parseInt(timeUnits[0], 10);
  runToEdit.value.mm = parseInt(timeUnits[1], 10);
  runToEdit.value.ss = parseInt(timeUnits[2], 10);
  runToEdit.value.dist_edit_unit = store.selectedUnits;
  runToEdit.value.dist_edit = metersToDistanceValue(runToEdit.value.distance);
  //console.log('runToEdit', runToEdit.value);
});

const closeDialog = () => {
  dialogRef.value.close();
};
const saveRun = () => {
    store.updateRun(runToEdit.value).then((response) => {
      dialogRef.value.close(response);
    }, error => {
      console.log('saveRun error', error);
      toast.add({
        severity:'error',
        summary: error.response ? error.response.name : 'Error',
        detail: error.response ? error.response.description : JSON.stringify(error),
        life: 3000 });
    });
}
</script>
<template>
  <div id="edit-run" class="card">
    <div class="field grid">
      <label for="run_name" class="col-12 mb-2 md:col-2 md:mb-0">Title</label>
      <div class="col-12 md:col-10">
        <InputText type="text" v-model="runToEdit.name" id="run_name" />
      </div>
    </div>
    <div class="field grid">
      <label for="run_class" class="col-12 mb-2 md:col-2 md:mb-0">Event</label>
      <div class="col-12 md:col-10 set-distance">
        <Dropdown v-model="runToEdit.class_key" :options="CLASSES" optionLabel="name" optionValue="key" id="run_class" placeholder="Select a run distance" class="outline-none" />
        <div class="distance">
            <div class="dist">
              <div>{{ metersToDistanceUnits(runToEdit.distance, 'mi') }}</div>
              <div>{{ metersToDistanceUnits(runToEdit.distance, 'km') }}</div>
            </div>
            <div class="inf">Strava<br />distance</div>
        </div>
      </div>
    </div>
      <div class="field grid">
          <label for="run_class" class="col-12 mb-2 md:col-2 md:mb-0">Distance</label>
          <div class="col-12 md:col-10 set-time">
              <div class="formgrid grid">
                  <div class="field col-4">
                      <InputText type="text" v-model="runToEdit.dist_edit" id="run_hh" />
                  </div>
                  <div class="field col-4">
                      <Dropdown v-model="runToEdit.dist_edit_unit" :options="store.units" id="run_units" class="outline-none" />
                  </div>
              </div>
          </div>
      </div>
    <div class="field grid">
        <label for="run_class" class="col-12 mb-2 md:col-2 md:mb-0">Time</label>
        <div class="col-12 md:col-10 set-time">
            <div class="formgrid grid">
                <div class="field col-4">
                    <label for="run_hh">Hours</label>
                    <InputText type="text" v-model="runToEdit.hh" id="run_hh" />
                </div>
                <div class="field col-4">
                    <label for="run_mm">Minutes</label>
                    <InputText type="text" v-model="runToEdit.mm" id="run_mm" />
                </div>
                <div class="field col-4">
                    <label for="run_ss">Seconds</label>
                    <InputText type="text" v-model="runToEdit.ss" id="run_ss" />
                </div>
              </div>
            <div class="muted">Current value: {{runToEdit.hms}}</div>
          </div>
      </div>

    <div class="field grid">
      <label for="run_class" class="col-12 mb-2 md:col-2 md:mb-0">Type</label>
      <div class="col-12 md:col-10 set-type">
        <span>Training</span> <InputSwitch v-model="runToEdit.race" class="btn-action" /> <span>Race</span>
      </div>
    </div>
    <div class="field grid">
      <div class="col-12 mb-2 md:col-2 md:mb-0"></div>
      <div class="col-12 md:col-10">
          <div class=" flex">
        <Button label="Cancel" severity="secondary" class="btn"  outlined @click="closeDialog()"/>
        <Button label="Save" class="btn btn-action"  @click="saveRun() "/>
      </div>
        <div class="muted">This will only update Medalcase, not Strava</div>
      </div>
    </div>
  </div>
</template>



<style lang="scss">
@import "@/assets/variables.scss";
#edit-run {
  .p-inputtext {
    width: 100%;
  }
  .p-dropdown {
    .p-inputtext {
      padding: 5px 9px;
    }
  }
  .btn {
    margin-right: 12px;
  }
  label {
    font-weight: 700;
  }
  .set-type {
    display: flex;
    justify-content: space-between;
    width: 182px;
    align-items: center;
  }
  .set-time {
    label {
      font-size: 12px;
      font-weight: 400;
      margin-bottom: 0;
    }
    .formgrid {
      .field {
        margin-bottom: 4px;
      }
    }
  }
  .set-distance {
    display: flex;
    align-items: center;
    .distance {
      display: flex;
      font-size: 12px;
      border: solid 1px #dddddd;
      margin-left: 12px;
      line-height: 1.5;
      .dist {
        padding: 1px 6px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: center;
      }
      .inf {
        background-color: #eeeeee;
        display: flex;
        align-items: center;
        padding: 0 6px;
      }
    }
  }
}
</style>
