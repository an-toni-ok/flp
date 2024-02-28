<script setup>
import { onMounted, ref } from "vue";
import { usePlanningStore } from "../../../store/planning";
import { useServerStore } from "../../../store/server";
import { useCanvasStore } from "../../../store/canvas";
import axios from "axios";
import PlanningDescription from "./PlanningDescription.vue";
import PlanningAreas from "./PlanningAreas.vue";
import PlanningTechnologies from "./PlanningTechnologies.vue";
import PlanningProductionSteps from "./PlanningProductionSteps.vue";
import PlanningMachinePark from "./PanningMachinePark.vue";
import PlanningObjectives from "./PlanningObjectives.vue";
import PlanningLoadingScreen from "./PlanningLoadingScreen.vue";
import PlanningLayoutAlternatives from "./PlanningLayoutAlternatives.vue";
import PlanningLayoutDetails from "./PlanningLayoutDetails.vue";
import PlanningFooter from "./PlanningFooter.vue";

const store = usePlanningStore();
const serverStore = useServerStore();
const canvasStore = useCanvasStore();
const layoutDetailsRef = ref();

const getSessionId = () => {
  const path = serverStore.START_SESSION_PATH;
  axios.get(path, { withCredentials: true })
    .catch((error) => {
      console.error(error);
    });
};

const footerContinue = () => {
  if(store.page === 8) {
    layoutDetailsRef.value.recalculateObjectives();
  };
};

onMounted(() => {
  getSessionId();
  let canvasSize = {width: 1200, height: 600};
  console.log(window.innerWidth, window.innerHeight);
  if(window.innerWidth < 1600) {
    canvasSize.width = 750;
    canvasSize.height = 300;
  }
  canvasStore.setCanvasSize(canvasSize);
});
</script>

<template>
  <div class="content-container">
    <h2 v-if="store.page !== 6" class="headline">{{ store.headline }}</h2>
    <PlanningDescription v-if="store.page === 0"></PlanningDescription>
    <PlanningAreas v-else-if="store.page === 1"></PlanningAreas>
    <PlanningTechnologies v-else-if="store.page === 2"></PlanningTechnologies>
    <PlanningProductionSteps v-else-if="store.page === 3"></PlanningProductionSteps>
    <PlanningMachinePark v-else-if="store.page === 4"></PlanningMachinePark>
    <PlanningObjectives v-else-if="store.page === 5"></PlanningObjectives>
    <PlanningLoadingScreen v-else-if="store.page === 6"></PlanningLoadingScreen>
    <PlanningLayoutAlternatives v-else-if="store.page === 7"></PlanningLayoutAlternatives>
    <PlanningLayoutDetails v-else-if="store.page === 8" ref="layoutDetailsRef"></PlanningLayoutDetails>
    <p v-else>Error</p>
    <PlanningFooter v-if="store.page > 0" @continue="footerContinue"></PlanningFooter>
  </div>
</template>

<style lang="scss">
.content {
  display: flex;
  flex-direction: row;
  height: 100%;
  padding-bottom: 100px;
}

.content .canvas-container {
  border: solid 2px black;
}

.planning-button {
  border-radius: 8px;
  border: 2px solid transparent;
  border-color: black;
  color: var(--tha-red);
  padding: 0.2em 1.9em;
  font-size: 1.2em;
  font-weight: 600;
  font-family: inherit;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.25s;

  &:hover {
    border-color: var(--tha-red);
  }
}

.red-button {
  color: white;
  padding: 0.2em 1.9em;
  font-size: 1.2em;
  font-weight: 600;
  font-family: inherit;
  background-color: var(--tha-red);
  cursor: pointer;
}

.row {
  display: flex;
  flex-direction: row;
}

.round-button {
  width: 30px;
  height: 30px;
  margin-left: 10px;

  text-decoration: none;
  display: inline-block;
  outline: none;
  cursor: pointer;
  border-style: none;
  color: white;
  background-color: var(--tha-red);
  border-radius: 100%;
  overflow: none;
  text-align: center;
  padding: 0;

  &:before {
    content: "";
    display: inline-block;
    vertical-align: middle;
    padding-top: 100%;
  }

  .round-button-text {
    display: inline-block;
    vertical-align: middle;
    max-width: 90%;
    font-size: 20px;
  }
}

.round-button-container {
  height: 2.5em;
  font-size: 1.1em;
  display: flex;
  align-items: center;
  justify-content: center;
}

select:required:invalid {
  color: gray;
}

option[value="null"][disabled] {
  display: none;
}

option {
  color: black;
}

.input-field {
  -webkit-box-shadow: inset 0px 0px 0px 1px black;
  -moz-box-shadow: inset 0px 0px 0px 1px black;
  box-shadow: inset 0px 0px 0px 1px black;
  font-size: 1.1em;
  font-weight: 500;
  text-align: left;
  display: block;
  border: none;
  width: 7.2em;
  height: 2.5em;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 0.4em;
}

.input-select {
  font-size: 1.1em;
  font-weight: 500;
  height: 2.5em;
  padding-left: 0.4em;
  background-color: white;
  border: solid 1px black;
}

.input-title {
  font-weight: 600;
  font-size: 1.1em;
  height: 1.6em;
  text-align: left;
  margin-bottom: 1em;
  display: flex;
  align-content: center;
  align-items: center;
}

.input-column {
  margin-right: 30px;
  max-width: fit-content;
}

.input-element {
  margin-bottom: 15px;
}

.output-text-field {
  -webkit-box-shadow: inset 0px 0px 0px 1px black;
  -moz-box-shadow: inset 0px 0px 0px 1px black;
  box-shadow: inset 0px 0px 0px 1px black;
  font-size: 1.1em;
  font-weight: 600;
  text-align: left;
  display: block;
  min-width: max-content;
  height: 1.5em;
  padding: 0.5em;
  margin-top: 0px;
  margin-bottom: 0px;
}

.headline {
  font-size: 1.5em;
  font-weight: 700;
  text-align: left;
  margin-top: 24px;
  margin-bottom: 24px;
}

.modal-content {
  display: flex;
  flex-direction: column;
  text-align: left;

  .headline {
    margin-top: 0;
  }

  .modal-footer {
    display: flex;
    align-content: center;
    justify-content: right;
    margin-top: 50px;
  }
}
</style>

<style lang="scss" scoped>
.content-container {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>