<script setup>
import { computed } from 'vue';
import { useProcessesStore } from '@/stores/processes';
import { BaseOverlay } from '@/components/library/overlays';
import { ProcessForm } from '@/components/library/forms';

const processesStore = useProcessesStore();
const action_type = computed(() => {
    if (processesStore.edit_id == 0 || !!processesStore.edit_id) {
        return "editieren"
    }
    return "erstellen"
})
</script>

<template>
    <BaseOverlay
        v-model:opened="processesStore.inputOverlayOpened"
        :title="'Prozess ' + action_type">
        <ProcessForm :action_type="action_type" />
    </BaseOverlay>
</template>

<style scoped>
</style>