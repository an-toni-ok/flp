import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useAreaStore = defineStore("areas", () => { 
    const areas = ref([]);
    const restrictedAreas = ref([]);

    // Return array of restricted areas with absolute positions
    const absoluteRAs = () => {
        let absRAs = [];
        for (const [areaIndex, area] of restrictedAreas.value.entries()) {
            const areaX = areas.value[areaIndex].x;
            const areaY = areas.value[areaIndex].y;

            for(const restrictedArea of area) {
                absRAs.push({
                    x: areaX + restrictedArea.x,
                    y: areaY + restrictedArea.y,
                    width: restrictedArea.width,
                    height: restrictedArea.height,
                })
            };
        };
        return absRAs;
    };

    const areaInputColumns = [
        { title: "Breite (x)", type: "inputNumber", value: "width", placeholder: "1 m", unit: "m", min: 0.1, max: 1000 },
        { title: "Länge (y)", type: "inputNumber", value: "height", placeholder: "1 m", unit: "m", min: 0.1, max: 1000 }
    ];

    return { areas, restrictedAreas, absoluteRAs, areaInputColumns };
});