<script setup>
import {ref, onMounted, inject, onUnmounted, nextTick, computed, watch} from "vue";
import {classLookup, medalStore} from "@/store";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import {socket, state} from "@/socket";

const dialogRef = inject("dialogRef");
const store = medalStore();

const messageStreamContainer = ref(null);

const updateRuns = () => {
  state.processing = true;
  if (!state.connected){
    socket.connect();
  }
  socket.emit('update', {}, () => {
    //
    state.processing = false;
    //socket.disconnect();
  });
}

watch(state.runUpdates, () => {
  console.log('store.runUpdates changed!');
  nextTick();
  messageStreamContainer.value.scrollTop = messageStreamContainer.value.scrollHeight;

}, {deep:true});

const medalSummary = computed(() => {
  const summary = state.runUpdates.reduce((obj, item) => {
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

  updateRuns();
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
  socket.disconnect();
});

const closeDialog = () => {
  dialogRef.value.close();
  store.runUpdates = [];
};

</script>
<template>
    <div id="update-runs">
          <div class="update-status">
              <template v-if="state.processing">
                <LoadingSpinner />
              </template>
              <template v-else>
                  <div class="update-summary">
                      <div v-if="medalSummary.length" class="s-block">
                        <div class="s-message">
                            Congratulations!!<br /> New medals found:
                        </div>
                        <div v-for="medal in medalSummary" :key="medal.key" class="medal">
                            <div class="s-name" :class="medal.key">{{medal.name}}</div>
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

              </template>
          </div>
          <div class="runs-stream-container" ref="messageStreamContainer">
              <ul class="runs">
                  <li v-show="state.processing && state.runUpdates.length === 0">processing...</li>
                  <li v-for="(run, idx) in state.runUpdates" :key="idx" class="single-run">
                      <font-awesome-icon icon="fa-sharp fa-solid fa-hexagon" size="xl" :rotation="90" :class="run.key" />
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
      .s-message {
        font-size: 18px;
      }
    }
    .medal {
      display: flex;
      .s-name {
        width: 60px;
        text-align: right;
        font-weight: 800;
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
  }
  .runs-stream-container {
    flex: 1;
    height: 260px;
    overflow-y: scroll;
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
