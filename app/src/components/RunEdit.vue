<script setup>
import { ref, onMounted, inject } from "vue";
import { medalStore, CLASSES } from "@/store";
import { metersToDistanceUnits } from "@/utils/helpers.js";
import { useToast } from "primevue/usetoast";

const runToEdit = ref(0);
const dialogRef = inject("dialogRef");
const store = medalStore();
const toast = useToast();

onMounted(() => {
  runToEdit.value = JSON.parse(JSON.stringify(dialogRef.value.data.run));
  console.log('runToEdit', runToEdit.value);
});

const closeDialog = () => {
  dialogRef.value.close();
};
const saveRun = () => {
    store.updateRun(runToEdit.value).then((response) => {
      dialogRef.value.close(response.data);
    }, error => {
      toast.add({
        severity:'error',
        summary: error.response.data.name,
        detail: error.response.data.description, life: 3000 });
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
        <Dropdown v-model="runToEdit.class_key" :options="CLASSES" optionLabel="name" optionValue="key" id="run_class" placeholder="Select a run distance" class="w-full md:w-14rem outline-none" />
        <div class="distance">
          <div>{{ metersToDistanceUnits(runToEdit.distance, 'mi') }}</div>
          <div>{{ metersToDistanceUnits(runToEdit.distance, 'km') }}</div>
        </div>
      </div>
    </div>

    <div class="field grid">
      <label for="run_class" class="col-12 mb-2 md:col-2 md:mb-0">Type</label>
      <div class="col-12 md:col-10 set-distance">
        Training <InputSwitch v-model="runToEdit.race" /> Race
      </div>
    </div>
    <div class="field grid">
      <div class="col-12 mb-2 md:col-2 md:mb-0"></div>
      <div class="col-12 md:col-10 set-distance">
        <Button label="Cancel" severity="secondary" outlined @click="closeDialog()"/>
        <Button label="Save" @click="saveRun() "/>
      </div>
    </div>
  </div>
</template>



<style lang="scss">
#edit-run {
  .p-inputtext {
    width: 100%;
  }
  label {
    font-weight: 700;
  }
  .set-distance {
    display: flex;
    align-items: center;
    .distance {
      padding-left: 8px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
    }
  }
}
</style>
