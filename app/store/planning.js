import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const usePlanningStore = defineStore("planning", () => {
    const page = ref(0);
    const headline = computed(() => {
        switch (page.value) {
            case 0:
                return "Beschreibung";
            case 1:
                return "Verfügbare Grundfläche";
            case 2:
                return "Verwendete Produktionstechnologien";
            case 3:
                return "Produktionsprozessreihenfolge";
            case 4:
                return "Maschinenpark";
            case 5:
                return "Zielgrößen der Optimierung";
            case 7:
                return "Folgende Layoutalternativen wurden gefunden:";
            case 8:
                return "Detailansicht Layout";
            default:
                return "";
        };
    });

    const nextPage = () => (iteratePage(1));
    const previousPage = () => (iteratePage(-1));
    const changePage = (newPage) => {
        if (newPage === 6 && page.value === 7) {
            newPage = 5;
        }
        if (newPage >= 0 && newPage <= 8) {
            page.value = newPage;
        };
    };
    const iteratePage = (direction) => {
        const newPage = page.value + direction;
        changePage(newPage);
    };

    // const DESCRIPTION = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " +
    //     "sed diam nonumy eirmod tempor invidunt ut labore et dolore " +
    //     "magna aliquyam erat, sed diam voluptua. At vero eos et accusam " +
    //     "et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea " +
    //     "takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor " +
    //     "sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor" +
    //     "invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua." +
    //     "At vero eos et accusam et justo duo dolores et ea rebum. Stet clita " +
    //     "kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.";

    const DESCRIPTION = "";

    let layoutAlternatives = [];
    let layoutIndex = 0;

    const euros = new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR',
    });

    const meters = new Intl.NumberFormat('de-DE', {
        style: 'unit',
        unit: 'meter',
    });

    let outputTechnologies = [""];

    const decimals = new Intl.NumberFormat('de-DE', {});

    const formatNumber = (value, unit) => {
        if (unit === undefined) {
            return value;
        };
        switch (unit) {
            case '€':
                return euros.format(value);
            case 'm':
                if (isNaN(value)) {
                    value = 0;
                };
                return meters.format(value);
            default:
                return decimals.format(value).concat(' ' + unit);
        };
    };

    const inputData = ref();
    return {
        page,
        headline,
        changePage,
        nextPage,
        previousPage,
        DESCRIPTION,
        layoutAlternatives,
        layoutIndex,
        outputTechnologies,
        formatNumber,
        inputData
    };
});