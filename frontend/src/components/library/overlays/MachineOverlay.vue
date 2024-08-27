<script setup>
import { ref, computed } from 'vue';
import { useMachinesStore } from '@/stores/machines';
import { BaseOverlay } from '@/components/library/overlays';
import { MachineForm } from '@/components/library/forms';

const machinesStore = useMachinesStore();

const action_type = computed(() => {
    if (machinesStore.edit_id == 0 || !!machinesStore.edit_id) {
        return "editieren"
    }
    return "erstellen"
})
</script>

<template>
    <BaseOverlay
        v-model:opened="machinesStore.input_overlay_opened"
        :title="'Maschine ' + action_type">
        <MachineForm :action_type="action_type" />
    </BaseOverlay>
</template>

<style scoped>
</style>