<script setup>
import { ref, toRaw, onMounted, onUnmounted } from "vue";
import { usePlanningStore } from "../../../store/planning";
import { useCanvasStore } from "../../../store/canvas";
import { useObjectiveStore } from "../../../store/objectives";
import { useServerStore } from "../../../store/server";
import PlanningTooltip from "./PlanningTooltip.vue";
import axios from "axios";

const planningStore = usePlanningStore();
const canvasStore = useCanvasStore();
const serverStore = useServerStore();
const objectiveStore = useObjectiveStore();
const layoutIndex = planningStore.layoutIndex;
const layout = planningStore.layoutAlternatives[layoutIndex];
const areas = ref(planningStore.inputData.areas);
const restrictedAreas = ref(planningStore.inputData.restrictedAreas);
const areaRects = ref([]);
const restrictedAreaRects = ref([]);
const machineRects = ref([]);
const machineRefs = ref([]);
const processArrows = ref([]);
const processArrowRefs = ref([]);
const operatorArrows = ref([]);
const operatorArrowRefs = ref([]);
const stage = ref();
const tooltipText = ref("");
const tooltipVisible = ref(false);
const tooltipPos = ref({ x: 0, y: 0 });
const controller = new AbortController();
const CANVAS_SIZE = canvasStore.CANVAS_SIZE;
const PIXELS_PER_METER = planningStore.inputData.pixelsPerMeter;
const OPERATOR_ARROW_OFFSET = 10;
const PLANNING_DATA_PATH = serverStore.PLANNING_DATA_PATH;
const CANCEL_PATH = serverStore.CANCEL_PATH;
let machines = layout.machines;
let operators = layout.operators;
let currentIndex = 0;
let startPos = { x: 0, y: 0 };

const recalculateObjectives = async () => {
    await (constructInputObject()).then(async (inputObj) => {
        await (sendPlanningData(inputObj));
    });
}
defineExpose({ recalculateObjectives });

// Set canvas size
const configKonva = {
    width: CANVAS_SIZE.width,
    height: CANVAS_SIZE.height
};

// Create a rectangle to represent a floor space on the canvas
const createAreaRect = async (space) => {
    return {
        config: {
            x: space.x * PIXELS_PER_METER,
            y: space.y * PIXELS_PER_METER,
            width: space.width * PIXELS_PER_METER,
            height: space.height * PIXELS_PER_METER,
            fill: '#d3d3d3',
            draggable: false,
            name: 'area',
        },
    };
};

// Create a rectangle to represent a machine in the depiction
const createMachineRect = async (machine) => {
    if (machine.x === undefined) {
        machine.x = 0;
    };
    if (machine.y === undefined) {
        machine.y = 0;
    };

    const width = machine.width * PIXELS_PER_METER;
    const height = machine.height * PIXELS_PER_METER;

    return {
        productionSteps: machine.productionSteps,

        config: {
            x: machine.x * PIXELS_PER_METER,
            y: machine.y * PIXELS_PER_METER,
            width: width,
            height: height,
            fill: '#f30147',
            stroke: 'black',
            strokeWidth: 2,
            draggable: true,
            name: 'machine',
        },
    };
};

// Load rectangles of floor spaces, restricted areas and machines to render them on the canvas
const loadRectangles = async () => {
    areaRects.value = [];
    restrictedAreaRects.value = [];
    machineRects.value = [];

    for (const area of areas.value) {
        areaRects.value.push(await (createAreaRect(area)));
    };

    for (const area of restrictedAreas.value) {
        restrictedAreaRects.value.push(await (canvasStore.createRestrictedAreaRect(area, PIXELS_PER_METER, false)));
    };

    for (const machine of machines) {
        machineRects.value.push(await (createMachineRect(machine)));
    };
};

// Create all arrows between machines
const loadArrows = async () => {
    processArrows.value = [];
    operatorArrows.value = [];

    // Create Process Arrows
    for (const machine1 of machineRects.value) {
        for (const machine2 of machineRects.value) {
            for (const prductionStep1 of machine1.productionSteps) {
                for (const productionStep2 of machine2.productionSteps) {
                    if (productionStep2 === prductionStep1 + 1 && machine1 !== machine2) {
                        processArrows.value.push(createArrow(machine1, machine2, false));
                    };
                };
            };
        };
    };

    // Create Operator Arrows
    for (const operator of operators) {
        for (const [index, machine] of operator.machines.entries()) {
            const hasNextMachine = typeof operator.machines[index + 1];
            if (hasNextMachine !== 'undefined') {
                operatorArrows.value.push(createArrow(machineRects.value[machine], machineRects.value[operator.machines[index + 1]], true))
            } else if (index !== 0) {
                operatorArrows.value.push(createArrow(machineRects.value[machine], machineRects.value[operator.machines[0]], true))
            };
        };
    };
};

// Returns the middle point of a rectangle
const getMiddle = (rectangle) => {
    const point = {};
    point.x = rectangle.x + rectangle.width / 2;
    point.y = rectangle.y + rectangle.height / 2;
    return point;
};

// Creates an arrow between two machine rectangles
const createArrow = (startMachine, endMachine, isOperatorArrow) => {
    let arrowStart = getMiddle(startMachine.config);
    let arrowEnd = getMiddle(endMachine.config);

    if (isOperatorArrow) {
        arrowStart.y += OPERATOR_ARROW_OFFSET;
        arrowEnd.y += OPERATOR_ARROW_OFFSET;
    };

    const newArrow = ({
        startMachine: startMachine,
        endMachine: endMachine,
        isOperatorArrow: isOperatorArrow,

        config: {
            points: [arrowStart.x, arrowStart.y, arrowEnd.x, arrowEnd.y],
            pointerLength: 10,
            pointerWidth: 10,
            fill: 'black',
            stroke: 'black',
            strokeWidth: 2,
            visible: canvasStore.arrowVisibility,
            dash: [10, 20],
            dashEnabled: isOperatorArrow
        }
    });
    return newArrow;
};

const handleDragstart = (index) => {
    currentIndex = index;
    startPos = machineRefs.value[index].getNode().absolutePosition();
    hideTooltip();
};

const handleDragmove = async (e) => {
    const node = e.target;
    const machineArr = stage.value.getNode().find('.machine');
    const restrictedAreaArr = stage.value.getNode().find('.restrictedArea');
    const obstacleArr = machineArr.concat(restrictedAreaArr);
    const oldStartPos = startPos;
    let newStartPos = oldStartPos;

    await (canvasStore.checkPosition(node, oldStartPos, obstacleArr, CANVAS_SIZE)).then(async (allowedDirection) => {
        newStartPos = await (canvasStore.setPosition(node, oldStartPos, allowedDirection, machineArr, machines, canvasStore.areaPixelsPerMeter));
    });

    startPos = newStartPos;

    machineRects.value[currentIndex].config.x = e.target.x();
    machineRects.value[currentIndex].config.y = e.target.y();
    updateArrows(processArrows.value, processArrowRefs.value);
    updateArrows(operatorArrows.value, operatorArrowRefs.value);
};

const handleDragend = (e) => {
    machines[currentIndex].x = e.target.x() / PIXELS_PER_METER;
    machines[currentIndex].y = e.target.y() / PIXELS_PER_METER;
};

// Update start and end positions of all arrows passed to this method
const updateArrows = (arrows, arrowRefs) => {
    for (const [index, arrow] of arrows.entries()) {
        let arrowStart = getMiddle(arrow.startMachine.config);
        let arrowEnd = getMiddle(arrow.endMachine.config);

        if (arrow.isOperatorArrow) {
            arrowStart.y += OPERATOR_ARROW_OFFSET;
            arrowEnd.y += OPERATOR_ARROW_OFFSET;
        };

        const points = [arrowStart.x, arrowStart.y, arrowEnd.x, arrowEnd.y];
        arrowRefs[index].getNode().setPoints(points);
    };
};

// Toggle arrow visibility
const toggleArrows = () => {
    canvasStore.arrowVisibility = !canvasStore.arrowVisibility;
    for (const arrow of processArrows.value) {
        arrow.config.visible = canvasStore.arrowVisibility;
    };
    for (const arrow of operatorArrows.value) {
        arrow.config.visible = canvasStore.arrowVisibility;
    }
};

// Update tooltip when mouse is over a machine
const updateTooltip = (index) => {
    const mousePos = stage.value.getNode().getPointerPosition();

    tooltipPos.value = {
        x: mousePos.x + 20,
        y: mousePos.y
    };
    tooltipText.value = (getTooltipText(machines[index]));
    tooltipVisible.value = true;
};

// Return tooltip text for a machine on the canvas
const getTooltipText = (machine) => {
    let text = "";
    text = text.concat(machine.machineType, "\n");
    for (const step of machine.productionSteps) {
        text = text.concat('  ', planningStore.outputTechnologies[step], "\n");
    };
    text = text.concat(
        '  Maschinenzeit: ', machine.machineTime, "\n",
        '  Manuelle Tätigkeit: ', machine.workContent, "\n",
        '  Zykluszeit: ', machine.cycleTime, "\n",
        '  Bediener: Werker ', machine.operator,
    );
    return text;
};

const hideTooltip = () => {
    tooltipVisible.value = false;
};

const updateLineGuides = (e) => {
    const node = e.target;

    const stageNode = stage.value.getNode();
    const nodeArr = stageNode.find('.machine');
    const restrictedNodeArr = stageNode.find('.restrictedArea');
    const areaNodeArr = stageNode.find('.area');

    for (const restrictedNode of restrictedNodeArr) {
        nodeArr.push(restrictedNode);
    };

    for (const areaNode of areaNodeArr) {
        nodeArr.push(areaNode);
    };

    canvasStore.updateLineGuides(node, nodeArr);
};

// Construct the input object so it can be processessed by
// the python script
const constructInputObject = async () => {
    const inputData = planningStore.inputData;
    let inputMachines = inputData.machines;

    for (const [index, machine] of inputMachines.entries()) {
        machine.x = machines[index].x;
        machine.y = machines[index].y;
    };

    let input = {
        areas: serverStore.mapAreas(toRaw(inputData.areas)),
        restricted_areas: serverStore.mapAreas(inputData.restrictedAreas),
        technologies: toRaw(inputData.technologies),
        production_steps: serverStore.mapProductionSteps(toRaw(inputData.productionSteps)),
        machines: serverStore.mapMachines(toRaw(inputMachines)),
        objectives: serverStore.mapObjectives(toRaw(inputData.objectives)),
        target_cycle_time: toRaw(inputData.targetCycleTime),
        hourly_operator_cost: toRaw(inputData.hourlyOperatorCost),
        line_id: layout.lineId
    };
    return input;
};

const sendPlanningData = async (payload) => {
    // Post data with axios, then save the layout
    await (axios.post(PLANNING_DATA_PATH, payload, { signal: controller.signal, withCredentials: true })
        .then((res) => {
            const outputData = res.data.output_data;

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

            layout.editedObjectives = outputObjectives;
            layout.machines = outputMachines;
            layout.operators = outputOperators;

            machines = layout.machines;
            operators = layout.operators;
        })
        .then(async () => {
            await (loadRectangles().then(() => {
                loadArrows();
            }));
        })
        .catch((error) => {
            if (error.code === "ERR_CANCELED") {
                console.log("request canceled");
            } else {
                console.error(error);
            }
        }));
};

onMounted(async () => {
    await (loadRectangles().then(() => {
        loadArrows();
    }));
});

onUnmounted(async () => {
    controller.abort();
    await (axios.get(CANCEL_PATH, { withCredentials: true }));
});
</script>

<template>
    <div class="content">
        <div class="canvas-container">
            <v-stage :config="configKonva" ref="stage">
                <v-layer @dragmove="updateLineGuides" @dragend="canvasStore.lineGuides = []" ref="rectLayer">
                    <v-rect v-for="item in areaRects" :key="item.id" :config="item.config"></v-rect>
                    <v-rect v-for="item in restrictedAreaRects" :key="item.id" :config="item.config"></v-rect>
                    <v-rect v-for="(item, index) in machineRects" :key="item.id" :config="item.config"
                        @dragstart="handleDragstart(index)" @dragmove="handleDragmove" @dragend="handleDragend"
                        @mousemove="updateTooltip(index)" @mouseout="hideTooltip" ref="machineRefs"></v-rect>
                    <v-arrow v-for="item in processArrows" :config="item.config" ref="processArrowRefs"></v-arrow>
                    <v-arrow v-for="item in operatorArrows" :config="item.config" ref="operatorArrowRefs"></v-arrow>
                    <v-line v-for="item in canvasStore.lineGuides" :config="item"></v-line>
                </v-layer>
                <PlanningTooltip :text="tooltipText" :visible="tooltipVisible" :position="tooltipPos"></PlanningTooltip>
            </v-stage>
        </div>
        <div class="side-content">
            <button class="planning-button arrow-button" @click="toggleArrows">{{ canvasStore.arrowButtonText }}</button>
            <div class="objectives-container">
                <div class="objectives">
                    <p class="objectives-type" v-if="layout.editedObjectives !== undefined">Optimierung</p>
                    <div v-for="(item, name) in layout.objectives" class="objectives-container">
                        <p class="objectives-title">{{ objectiveStore.output[name].title }}:</p>
                        <p class="objectives-value">{{ planningStore.formatNumber(item, objectiveStore.output[name].unit) }}
                        </p>
                    </div>
                </div>
                <div class="objectives" v-if="layout.editedObjectives !== undefined">
                    <p class="objectives-type">Bearbeitet</p>
                    <div v-for="(item, name) in layout.editedObjectives" class="objectives-container">
                        <p class="objectives-title">{{ objectiveStore.output[name].title }}:</p>
                        <p class="objectives-value">{{ planningStore.formatNumber(item, objectiveStore.output[name].unit) }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.canvas-container {
    width: max-content;
    height: max-content;
}

.side-content {
    display: flex;
    flex-direction: column;
    margin-left: 50px;

    .arrow-button {
        width: 12em;
        margin-bottom: 30px;
    }
}

.objectives-container {
    display: flex;
    flex-direction: row;
}

.objectives {
    display: flex;
    flex-direction: column;
    margin-right: 50px;

    p {
        font-size: 1.1em;
        font-weight: 600;
        height: 1.6em;
        text-align: left;
        margin-top: 0;
        margin-bottom: 0;
    }

    .objectives-type {
        color: var(--tha-red);
        margin-bottom: 10px;
    }

    .objectives-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 10px;

        .objectives-title {
            min-width: max-content;
        }

        .objectives-value {
            text-align: right;
        }
    }
}
</style>