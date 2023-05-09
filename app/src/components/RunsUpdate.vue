<script setup>
import { ref, onMounted, inject, onUnmounted, nextTick, computed } from "vue";
import { classLookup } from "@/store";
import { getJWT } from "@/utils/helpers.js";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import {useToast} from "primevue/usetoast";
const toast = useToast();
const dialogRef = inject("dialogRef");

const messageStreamContainer = ref(null);
const runUpdates = ref([]);
const processing = ref(true);

const socket = new WebSocket("wss://8vzirn1xee.execute-api.eu-west-1.amazonaws.com/prod");

socket.onopen = function() {
  console.log("wss successfully connected");
  processing.value = true;
  socket.send(JSON.stringify({"jwt": getJWT()}));
}

socket.onmessage = function(event) {
  let r = JSON.parse(event.data);
  let action = r.action;
  let value = r.value
  //console.log('response', event);
  if (!action){ return; }
  if (action === 'status'){
    if (value ===  'COMPLETE') {
      processing.value = false;
    }
    else if (value === 'PING'){
      console.log('ws keepalive');
    }
  }
  else if ( action === 'newrun' ) {
    runUpdates.value.push(value);
    nextTick();
    messageStreamContainer.value.scrollTop = messageStreamContainer.value.scrollHeight;
  }
  else if (action === 'error') {
    toast.add({
      severity: 'error',
      summary: value,
      life: 5000
    });
    processing.value = false;
    closeDialog();
  }
}
socket.onclose = function(event) {
  if (event.wasClean) {
    console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    console.log(`[close] Connection died: code=${event.code}`);
  }
  processing.value = false;
};

const medalSummary = computed(() => {
  const summary = runUpdates.value.reduce((obj, item) => {
    if (!obj[item.key]){
      obj[item.key] = {
        name: classLookup[item.key].name,
        seq: classLookup[item.key].seq,
        key: item.key,
        count: 0
      };
    }
    obj[item.key].count++;
    return obj;
  }, {});
  return Object.values(summary).sort((a, b) => {
    if (a.seq < b.seq) {
      return -1;
    }
    if (a.seq > b.seq) {
      return 1;
    }
    return 0;
  })
});

onMounted(() => {
  console.log('RunsUpdate');

  //updateRuns();
  /*
  stillLoading.value = true;
  //messageStreamContainer.value.scrollTop = messageStreamContainer.value.scrollHeight;
  interval = window.setInterval(() => {
    counter.value--;
    let mclass = CLASSES[Math.floor(Math.random() * CLASSES.length)];
    runStream.value.push({
      key: mclass.key,
      name: 'asd asdasdasd asd asdas dasdasd'
    });
    console.log('add run');
    nextTick();
    messageStreamContainer.value.scrollTop = messageStreamContainer.value.scrollHeight;
    if (counter.value <= 0){
      clearInterval(interval);
      stillLoading.value = false;
    }
  }, 1000);

   */


});

onUnmounted(() => {
  socket.close();
});

const closeDialog = () => {
  dialogRef.value.close(medalSummary.value.length);
};

</script>
<template>
    <div id="update-runs">
          <div class="update-status">
              <div v-if="processing">
                <LoadingSpinner />
                  <div class="tally" v-show="runUpdates.length > 0">
                      found: {{runUpdates.length}}
                  </div>
              </div>
              <div v-else>
                  <div class="update-summary">
                      <div v-if="medalSummary.length" class="s-block">
                        <div class="s-message">
                            Congratulations!!<br /> <b>{{runUpdates.length}}</b> New medals found:
                        </div>
                        <div v-for="medal in medalSummary" :key="medal.key" class="medal">
                            <div class="s-name" :class="medal.key">{{medal.name}}</div>
                            <div class="s-badge"><font-awesome-icon icon="fa-sharp fa-light fa-hexagon" size="xl" :rotation="90" :class="medal.key" /></div>
                            <div class="s-count">{{medal.count}}</div>
                        </div>
                      </div>
                      <div v-else class="s-block">
                          <div class="s-message">
                              No new medals found this time, keep on pushing!!
                          </div>
                      </div>
                      <Button label="Close" @click="closeDialog()"/>
                  </div>
              </div>
          </div>
          <div id="runs-stream-container" ref="messageStreamContainer">
              <ul class="runs">
                  <li v-show="processing && runUpdates.length === 0">processing...</li>
                  <li v-for="(run, idx) in runUpdates" :key="idx" class="single-run">
                      <font-awesome-icon icon="fa-sharp fa-light fa-hexagon" size="xl" :rotation="90" :class="run.key" />
                      <span class="run-name">{{run.name}}</span>
                  </li>
              </ul>
          </div>

  </div>
</template>



<style lang="scss">
@import "@/assets/variables.scss";
#update-runs {
  display: flex;
  flex-direction: row;

  .update-summary {
    display: flex;
    flex-direction: column;
    padding: 12px;
    .s-block {
      margin-bottom: 12px;
    }
    .medal {
      display: flex;
      .s-name {
        width: 60px;
        text-align: right;
        font-weight: 800;
      }
      .s-badge {
        width: 30px;
        text-align: center;
      }
      .s-count {
        min-width: 30px;
        text-align: right;
      }
    }

  }
  .update-status {
    display: flex;
    justify-content: center;

    width: 200px;
    .tally {
      text-align: center;
    }
  }
  #runs-stream-container {
    flex: 1;
    height: 260px;
    overflow-y: scroll;
    scroll-behavior: smooth;
  }
  .runs {
    margin-bottom: 32px;
    list-style-type: none;
    margin-left: 0;
    padding: 0;
    .single-run {
      display: flex;
      align-items: center;
      padding: 3px 0;
      .run-name {
        display: inline-block;
        padding-left: 4px;
      }
    }
  }
}
@media screen and (max-width: 730px){
  #update-runs {
    flex-direction: column;
    .update-status {
      flex: 1;
      width: 100%;
    }

    .runs-stream-container {

    }
  }
}
</style>
