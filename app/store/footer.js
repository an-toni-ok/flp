import { computed } from 'vue';
import { defineStore } from 'pinia';
import { usePlanningStore } from './planning';

export const useFooterStore = defineStore("footer", () => {
    const planningStore = usePlanningStore();
    const continueButtonText = computed(() => {
        if (planningStore.page === 5) {
            return "Layout Optimieren"
        } else if (planningStore.page === 8) {
            return "Zielgrößen neu berechnen"
        };
        return "Weiter";
    });

    const returnButtonText = computed(() => {
        if (planningStore.page === 6) {
            return "Abbrechen"
        }
        return "Zurück";
    });

    return { continueButtonText, returnButtonText };
});