<script setup>
import axios from "axios";
import { ref, onMounted, toRaw, onUnmounted } from 'vue';
import { usePlanningStore } from '../../../store/planning';
import { useAreaStore } from '../../../store/areas';
import { useTechnologyStore } from "../../../store/technologies";
import { useProductionStepStore } from "../../../store/productionSteps";
import { useMachineStore } from '../../../store/machines';
import { useObjectiveStore } from "../../../store/objectives";
import { useCanvasStore } from "../../../store/canvas";
import { useServerStore } from "../../../store/server";
import ProgressBar from 'primevue/progressbar';

const planningStore = usePlanningStore();
const areaStore = useAreaStore();
const technologyStore = useTechnologyStore();
const productionStepStore = useProductionStepStore();
const machineStore = useMachineStore();
const objectiveStore = useObjectiveStore();
const canvasStore = useCanvasStore();
const serverStore = useServerStore();

let areas = areaStore.areas;
let restrictedAreas = areaStore.absoluteRAs();
let technologies = technologyStore.names;
let productionSteps = productionStepStore.productionSteps;
let machines = machineStore.machines;
let objectives = objectiveStore.objectives;
let targetCycleTime = objectiveStore.targetCycleTime;
let hourlyOperatorCost = objectiveStore.hourlyOperatorCost;
const controller = new AbortController();
const PLANNING_DATA_PATH = serverStore.PLANNING_DATA_PATH;
const CANCEL_PATH = serverStore.CANCEL_PATH;

let progressInterval;

const progress = ref(0);

const constructInputObject = async () => {
  // Construct the input object so it can be processessed by
  // the python script 
  let input = {
    areas: serverStore.mapAreas(toRaw(areas)),
    restricted_areas: serverStore.mapAreas(restrictedAreas),
    technologies: toRaw(technologies),
    production_steps: serverStore.mapProductionSteps(toRaw(productionSteps)),
    machines: serverStore.mapMachines(toRaw(machines)),
    objectives: serverStore.mapObjectives(toRaw(objectives)),
    target_cycle_time: toRaw(targetCycleTime),
    hourly_operator_cost: toRaw(hourlyOperatorCost)
  };

  // Save input data which is needed for rendering on the
  // layout details canvas
  let saveData = {
    areas: areas,
    restrictedAreas: restrictedAreas,
    technologies: technologies,
    productionSteps: productionSteps,
    machines: machines,
    objectives: objectives,
    targetCycleTime: targetCycleTime,
    hourlyOperatorCost: hourlyOperatorCost,
    pixelsPerMeter: canvasStore.areaPixelsPerMeter,
  };
  planningStore.inputData = removeReactivity(saveData);

  return input;
};

// Use JSON pattern to remove reactivity from vue refs
const removeReactivity = (ref) => JSON.parse(JSON.stringify(ref));

// Send planning data to the server and process the response
const sendPlanningData = async (payload) => {
  // Post data with axios, then save the layoutalternatives to the store
  await (axios.post(PLANNING_DATA_PATH, payload, { signal: controller.signal, withCredentials: true })
    .then((res) => {
      const outputArr = res.data.output_data;
      const lineId = res.data.line_id;
      let layoutAlternatives = [];

      planningStore.outputTechnologies = outputArr[0].technologies;

      for (const outputData of outputArr) {

        let outputMachines = serverStore.mapOutputMachines(outputData.machines);
        for (const [index, machine] of outputMachines.entries()) {
          if (machine.rotation === 0) {
            machine.width = machines[index].width;
            machine.height = machines[index].height;
          } else if (machine.rotation === 90) {
            machine.width = machines[index].height;
            machine.height = machines[index].width;
          }
        };

        let outputObjectives = serverStore.mapOutputObjectives(outputData.objectives);
        let outputOperators = serverStore.mapOutputOperators(outputData.operators);
        let outputTechnologies = outputData.technologies;

        let layoutAlternative = {
          objectives: outputObjectives,
          machines: outputMachines,
          operators: outputOperators,
          technologies: outputTechnologies,
          lineId: lineId
        };

        layoutAlternatives.push(layoutAlternative);
      };
      return (layoutAlternatives);
    })
    // Save processed data to the store
    .then((layoutAlternatives) => {
      planningStore.layoutAlternatives = layoutAlternatives;
    })
    .catch((error) => {
      if (error.code === "ERR_CANCELED") {
        console.log("request canceled");
      } else {
        console.error(error);
      }
    }));
};

// Update the progress bar
const updateProgress = async () => {
  await (axios.get(PLANNING_DATA_PATH, { signal: controller.signal, withCredentials: true })
    .then((res) => {
      progress.value = res.data.progress;
    })
    .catch((error) => {
      if (error.code === "ERR_CANCELED") {
        console.log("request canceled");
      } else {
        console.error(error);
      }
    }));
};

const setInputVariables = async () => {
  areas = areaStore.areas;
  restrictedAreas = areaStore.absoluteRAs();
  technologies = technologyStore.names;
  productionSteps = productionStepStore.productionSteps;
  machines = machineStore.machines;
  objectives = objectiveStore.objectives;
  targetCycleTime = objectiveStore.targetCycleTime;
  hourlyOperatorCost = objectiveStore.hourlyOperatorCost;
};

onMounted(async () => {
  await (setInputVariables());

  progressInterval = setInterval(updateProgress, 1000);
  await (constructInputObject()).then(async (inputObj) => {
    await (sendPlanningData(inputObj));
  }).then(() => {
    if (planningStore.page === 6) {
      planningStore.nextPage();
    };
  });
});

// Cancel https request when component is unmounted
onUnmounted(async () => {
  clearInterval(progressInterval);
  controller.abort();
  await (axios.get(CANCEL_PATH, { withCredentials: true }));
})
</script>

<template>
  <div class="content">
    <h2 class="headline">Ihr Layout wird für Sie optimiert. Bitte haben Sie etwas Geduld.</h2>
    <ProgressBar :value="progress" :pt="{
      root: { class: 'progress-bar' },
      value: { style: { background: '#f30147', transition: '0.25s' } },
    }" class="progress-bar"></ProgressBar>
  </div>
</template>

<style lang="scss" scoped>
.content {
  flex-direction: column;
  align-items: center;
}

.progress-bar {
  margin-top: 150px;
  background-color: lightgray;
  border-radius: 8px;
  height: 50px;
  width: 50%;
  font-size: 2em;
  color: white;
}

@media only screen and (max-height: 800px) {
  .progress-bar {
    margin-top: 50px;
  }
}

.headline {
  font-size: 2.5em;
  font-weight: 500;
  text-align: center;
  margin-top: 60px;
}
</style>