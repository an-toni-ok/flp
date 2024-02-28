import { computed } from 'vue';
import { defineStore } from 'pinia';
import { useSidebarStore } from './sidebar';

export const useHeaderStore = defineStore("header", () => {
    const sidebar = useSidebarStore();
    const HEADER_HEIGHT = 6.2;
    const headerHeight = computed(
        () => ''.concat(HEADER_HEIGHT, "em")
    );

    const headerMarginLeft = computed(
        () => ''.concat(sidebar.SIDEBAR_WIDTH, "px")
    );

    return { headerHeight, headerMarginLeft };
});