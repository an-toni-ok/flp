import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useObjectiveStore = defineStore("objectives", () => {
    const investTitle = "Investition";
    const unitCostsTitle = "Stückkosten";
    const spaceConsumptionTitle = "Flächenverbrauch";
    const numberOfWorkersTitle = "Anzahl der Werker";

    const objectives = ref({
        investment: false,
        unitCosts: false,
        spaceConsumption: false,
        numberOfWorkers: false
    });

    const targetCycleTime = ref(null);
    const hourlyOperatorCost = ref(null);

    const output = {
        investment: {
            title: investTitle,
            unit: "€"
        },
        unitCosts: {
            title: unitCostsTitle,
            unit: "€"
        },
        spaceConsumption: {
            title: spaceConsumptionTitle,
            unit: "m²"
        },
        numberOfWorkers: {
            title: numberOfWorkersTitle,
            unit: ""
        },
    }; 

    const objectiveInputColumns = [
        { title: investTitle, type: "checkbox", value: "investment" },
        { title: unitCostsTitle, type: "checkbox", value: "unitCosts" },
        { title: spaceConsumptionTitle, type: "checkbox", value: "spaceConsumption" },
        { title: numberOfWorkersTitle, type: "checkbox", value: "numberOfWorkers" }
    ];

    return { objectives, output, objectiveInputColumns, targetCycleTime, hourlyOperatorCost };
});