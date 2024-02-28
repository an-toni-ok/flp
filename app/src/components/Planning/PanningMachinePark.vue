<script setup>
import { onMounted, onUnmounted, ref, computed } from "vue";
import { useTechnologyStore } from "../../../store/technologies";
import { useMachineStore } from "../../../store/machines";
import PlanningInputColumn from "./PlanningInputColumn.vue";
import Modal from "../Modal.vue";
import Notification from "../Notification.vue";
import InputError from "../../class/InputError";

const store = useMachineStore();
const machines = ref([]);
const modalActive = ref(false);
const notificationActive = ref(false);
const notificationMessage = ref("");
const inputColumns = store.machineInputColumns;
const technologies = useTechnologyStore().names;

const machineListEmpty = computed(() => {
    if (!machines.value.length > 0) {
        return true;
    } else {
        return false;
    }
});

const outputMachines = computed(() => {
    if (machines.value.length > 0) {
        return machines.value;
    } else {
        let outputMachine = emptyMachine();
        outputMachine[0].machineType = store.machineInputColumns[0].placeholder;
        outputMachine[0].technologies[0] = store.machineInputColumns[1].placeholder;

        return outputMachine;
    };
});

const emptyMachine = () => {
    return [{
        machineType: "",
        technologies: [""],
        hourlyMachineCost: null,
        investmentCost: null,
        additionalTime: null,
        width: null,
        height: null
    }];
};
const modalMachine = ref(emptyMachine());

const addTechnology = () => {
    modalMachine.value[0].technologies.push("");
};

const removeTechnology = () => {
    modalMachine.value[0].technologies.pop();
};

const toggleModal = () => {
    modalActive.value = !modalActive.value;
    let sleepTime = 0;

    if (!modalActive.value) {
        sleepTime = 300;
    };

    setTimeout(() => { modalMachine.value = emptyMachine(); }, sleepTime);
    console.log(machines.value)
    console.log(machines.value.length)
    console.log(outputMachines.value)
};

const toggleNotification = () => {
    notificationActive.value = !notificationActive.value;
};

const addMachine = () => {
    const newMachine = modalMachine.value[0];

    try {
        if (newMachine.machineType === "") {
            throw new InputError("Das Feld Maschinentyp darf nicht leer sein!");
        } else if (
            newMachine.width === null ||
            newMachine.width <= 0 ||
            newMachine.height === null ||
            newMachine.height <= 0
        ) {
            throw new InputError("Länge und Breite der Maschine müssen definiert sein!");
        } else {
            for (const technology of newMachine.technologies) {
                if (technology === "") {
                    throw new InputError("Es muss eine technologie aus der Liste gewählt werden!");
                };
            };

            for (const value in newMachine) {
                if (newMachine[value] === null) {
                    newMachine[value] = 0;
                };
            };
        };

        machines.value.push(newMachine);
        toggleModal();
    } catch (error) {
        if (error instanceof InputError) {
            notificationMessage.value = error.message;
            toggleNotification();
        } else {
            console.error(error.message);
        };
    };
};

const removeMachine = () => {
    machines.value.pop();
};

onMounted(() => {
    machines.value = store.machines;
    //console.log(machineListEmpty.value);
});

onUnmounted(() => {
    store.machines = machines.value;
});
</script>

<template>
    <div class="content">
        <div class="row">
            <PlanningInputColumn v-for="item in inputColumns" :key="item.id" :title="item.title" type="output"
                :list="outputMachines" :value="item.value" :isArray="item.isArray" :arrayObjectValue="item.arrayObjectValue"
                :selectList="technologies" :placeholder="item.placeholder" :unit="item.unit"
                :isPlaceholder="machineListEmpty">
            </PlanningInputColumn>
            <PlanningInputColumn type="button" :isPlaceholder="machineListEmpty" :isOutputMachine="true"
                :list="outputMachines" @add="toggleModal" @remove="removeMachine">
            </PlanningInputColumn>
        </div>
        <Modal @close="toggleModal" :modalActive="modalActive">
            <div class="modal-content">
                <h2 class="headline">Neue Maschine erstellen</h2>
                <div class="row">
                    <PlanningInputColumn v-for="item in inputColumns" :key="item.id" :title="item.title" :type="item.type"
                        :list="modalMachine" :value="item.value" :isArray="item.isArray" :selectList="technologies"
                        :selectValue=item.selectValue :placeholder="item.placeholder" :unit="item.unit" :min="item.min"
                        :max="item.max" @push="addTechnology" @pop="removeTechnology">
                    </PlanningInputColumn>
                </div>
                <div class="modal-footer">
                    <button @click="addMachine" class="planning-button">Maschine erstellen</button>
                </div>
            </div>
        </Modal>
        <Notification @close="toggleNotification" :notificationActive="notificationActive" :message="notificationMessage">
        </Notification>
    </div>
</template>

<style lang="scss" scoped>
.content {
    display: flex;
    flex-direction: column;
}

.planning-button {
    width: 17em;
    margin-right: 15px;
}
</style>