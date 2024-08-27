<script setup>
import { useProcessesStore } from '@/stores/processes';
import { NumberInput, TechnologyDropdownInput } from '@/components/library/inputs';
import { TextButton } from '@/components/library/buttons';

const props = defineProps({
    action_type: {
        type: String,
        default: "erstellen"
    }
})

const processesStore = useProcessesStore();
</script>

<template>
    <div 
        class="data-layout" 
        v-show="processesStore.inputOverlayOpened">
        <NumberInput 
            name="Maschinenzeit (in s)"
            id="machinenzeit"
            v-model:value="processesStore.input_machine_time" />
        <NumberInput 
            name="Manuelle Zeit (in s)"
            id="manual-time"
            v-model:value="processesStore.input_manual_time" />
        <TechnologyDropdownInput 
            v-model:value="processesStore.input_technology"
            :is-deletable="true" />
        <TextButton 
            @click="processesStore.set"
            :text="action_type"/>
    </div>
</template>

<style scoped>
.data-layout {
    padding: 2rem;
    border: 1px solid var(--color-border);
}

.data-layout > *:not(:last-child) {
    margin-bottom: 0.5rem;
}

.data-layout > :deep(:last-child) {
    margin-top: 1rem;
}
</style>