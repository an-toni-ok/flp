import { reactive } from 'vue';
import { defineStore } from 'pinia';

export const useMachineStore = defineStore("machines", () => {
    const machines = reactive([]);

    const machineInputColumns = [
        { title: "Maschinentyp", type: "inputText", value: "machineType", placeholder: "Schweißzelle" },
        { title: "Technologie(n)", type: "selectArray", isArray: true, value: "technologies", selectValue: "technology", placeholder: "Schweißen" },
        { title: "Maschinenstundensatz", type: "inputCurrency", value: "hourlyMachineCost", placeholder: "100,00 €", unit: "€", min: 0, max: 1000000000 },
        { title: "Investitionskosten", type: "inputCurrency", value: "investmentCost", placeholder: "100.000,00 €", unit: "€", min: 0, max: 1000000000000 },
        { title: "Zusätzliche Maschinenzeit", type: "inputNumber", value: "additionalTime", placeholder: "10 s", unit: "s", min: 0, max: 1000000000 },
        { title: "Breite (x)", type: "inputNumber", value: "width", placeholder: "1 m", unit: "m", min: 0.1, max: 1000 },
        { title: "Länge (y)", type: "inputNumber", value: "height", placeholder: "1 m", unit: "m", min: 0.1, max: 1000 },
    ];

    return { machines, machineInputColumns };
});