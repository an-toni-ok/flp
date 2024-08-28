<script setup>
import { IconArrowLeft, IconArrowRight, IconConfirm } from '@/components/icons';
import { IconButton } from '@/components/library/buttons';

const props = defineProps({
    complete: {
        type: Boolean,
        default: false
    }
})

defineEmits(['next', 'prev'])
</script>

<template>
    <div class="progress-buttons">
        <IconButton 
            text="Zurück" 
            tooltip-position="top"
            @click="$emit('prev')">
            <IconArrowLeft />
        </IconButton>
        <IconButton 
            text="Weiter" 
            tooltip-position="top"
            :wide="true"
            @click="$emit('next')">
            <IconArrowRight v-if="!complete" />
            <IconConfirm v-if="complete" />
        </IconButton>
    </div>
</template>

<style scoped>
.progress-buttons {
    display: flex;
    justify-content: flex-end;
    z-index: 3;
}

.progress-buttons > :deep(button:last-child) {
    /* Remove double border */
    margin-left: -1px;
}
</style>