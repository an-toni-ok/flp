<script setup>
import { usePlanningStore } from "../../../store/planning";
import { useObjectiveStore } from "../../../store/objectives";

const planningStore = usePlanningStore();
const objectiveStore = useObjectiveStore();

const detailedView = (index) => {
    // Set layout alternative for the graphical depiction and then show the depiciton
    planningStore.layoutIndex = index;
    planningStore.changePage(8);
};
</script>

<template>
    <div class="content">
        <div v-for="(item, index) in planningStore.layoutAlternatives" class="layout-alternative">
            <div v-for="(objective, name) in item.objectives" :key="name" class="target-value-column">
                <p class="target-value-title"> {{ objectiveStore.output[name].title }}: </p>
                <p class="target-value"> {{ planningStore.formatNumber(objective, objectiveStore.output[name].unit) }}</p>
            </div>
            <button @click="detailedView(index)" class="red-button">Detailansicht</button>
        </div>
        <hr>
    </div>
</template>

<style lang="scss" scoped>
.content {
    display: flex;
    flex-direction: column;
}

.layout-alternative {
    display: flex;
    flex-direction: row;
    align-items: center;
    align-content: center;
    margin-right: 20px;
    border-bottom: 1px solid transparent;
    border-color: gray;
}

.target-value-column {
    display: flex;
    flex-direction: column;
    margin-right: 50px;
    margin-top: 20px;

    p {
        font-size: 1.1em;
        font-weight: 600;
        height: 1.6em;
    }

    .target-value-title {
        color: var(--tha-red);
        text-align: left;
        margin-top: 0;
        margin-bottom: 0;
    }

    .target-value {
        text-align: right;
        margin-top: 20px;
        margin-bottom: 20px;
    }
}
</style>