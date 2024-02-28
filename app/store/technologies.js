import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useTechnologyStore = defineStore("technologies", () => {
    const technologies = ref([{ technology: "" }]);
    
    const names = computed(() => {
        const names = [];
        for (const technology of technologies.value) {
            names.push(technology.technology);
        };
        return names;
    });

    const technologyInputColumns = [
        { title: "Technologiename", type: "inputText", value: "technology", placeholder: "Schweißen" },
        { type: "button" }
    ];

    return { technologies, names, technologyInputColumns };
});