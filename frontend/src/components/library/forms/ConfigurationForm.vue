<script setup>
import { useSettingsStore } from '@/stores/settings';
import { CheckboxInput, NumberInput } from '@/components/library/inputs';

const settingsStore = useSettingsStore();
</script>

<template>
    <div class="inputs">
        <div class="general-inputs">
            <h2>Optimierungskonfiguration</h2>
            <NumberInput 
                id="cycle_target_time"
                name="Zielzykluszeit in s"
                v-model:value="settingsStore.cycle_target_time"/>
            <NumberInput 
                id="hourly_operator_cost"
                name="Stündliche Werkerlöhne (&#8364;)"
                v-model:value="settingsStore.hourly_operator_cost"/>
        </div>
        <div class="checkboxes">
            <CheckboxInput 
                id="investion" 
                name="Investition"
                v-model:value="settingsStore.investion" />
            <CheckboxInput 
                id="piece_cost" 
                name="Stückkosten"
                v-model:value="settingsStore.piece_cost" />
            <CheckboxInput 
                id="area_usage" 
                name="Flächenverbrauch"
                v-model:value="settingsStore.area_usage" />
            <CheckboxInput 
                id="worker_amount" 
                name="Anzahl der Operatoren"
                v-model:value="settingsStore.worker_amount" />
        </div>
    </div>
</template>

<style scoped>
.inputs {
    display: flex;
    /* flex-direction: column; */
    /* justify-content: space-between; */
    gap: 4rem;
    padding: 1.5rem;
    border: 1px solid var(--color-border);
}

.checkboxes {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-end;
}

.general-inputs {
    margin-bottom: 4px;
}

.general-inputs > h2 {
    font-size: var(--font-size-h3);
    margin-bottom: 1.5rem;
}

.general-inputs > *:not(h2),
.checkboxes > *:not(h2) {
    margin-top: 0.5rem;
}
</style>