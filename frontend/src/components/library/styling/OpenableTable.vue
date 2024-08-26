<script setup>
import { IconArrowDown } from '@/components/icons';
import { IconButton } from '@/components/library/buttons';
import { computed } from 'vue';

const props = defineProps({
    name: {
        type: String,
        required: true,
    }
});

const model = defineModel({
    type: Boolean,
    required: true
});

const help_text = computed(() => {
    let state = model.value ? 'schließen' : 'öffnen';
    return `Die Tabelle ${props.name} ${state}`;
})
</script>

<template>
    <div class="wrapper">
        <div :class="['header', model ? '' : 'close-header' ]">
            <IconButton 
                :text="help_text"
                tooltip-position="bottom"
                @click="model = !model">
                <IconArrowDown />
            </IconButton>
            <h3>{{ name }}</h3>
        </div>
        <div v-show="model" class="toggleable-table">
            <slot></slot>
        </div>
    </div>
</template>

<style scoped>
.wrapper {
    width: 100%;
}

.header {
    display: flex;
    align-items: center;
    justify-content: flex-start;
}

.header > h3 {
    width: 100%;
    height: 2.5rem;
    line-height: 2.5rem;
    padding-left: 1rem;
    border-top: 1px solid var(--color-border);
    border-right: 1px solid var(--color-border);
}

.close-header > h3 {
    border-bottom: 1px solid var(--color-border);
}

.toggleable-table {
    margin-top: -1px;
}
</style>