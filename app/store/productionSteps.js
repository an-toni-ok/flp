import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useProductionStepStore = defineStore("productionSteps", () => {
    const productionSteps = ref([{
        order: 1,
        technology: "",
        machineTime: null,
        manualTime: null,
    }]);
    
    const productionStepInputColumns = [
        { title: "Reihenfolge", type: "output", value: "order" },
        { title: "Technologie", type: "select", value: "technology", placeholder: "Schweißen" },
        { title: "Maschinenzeit", type: "inputNumber", value: "machineTime", placeholder: "10 s", unit: "s", min: 0, max: 1000000000},
        { title: "Manuelle Tätigkeit", type: "inputNumber", value: "manualTime", placeholder: "10 s", unit: "s", min: 0, max: 1000000000},
        { type: "button" }
    ];

    return { productionSteps, productionStepInputColumns };
});