import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useSidebarStore = defineStore("sidebar", () => {
    const collapsed = ref(false);
    const toggleSidebar = () => (collapsed.value = !collapsed.value);

    const SIDEBAR_WIDTH = 180;
    const SIDEBAR_WIDTH_COLLAPSED = 38;
    const sidebarWidth = computed(
        () => ''.concat(collapsed.value ? SIDEBAR_WIDTH_COLLAPSED : SIDEBAR_WIDTH, "px")
    );

    return { collapsed, toggleSidebar, SIDEBAR_WIDTH, SIDEBAR_WIDTH_COLLAPSED, sidebarWidth };
});