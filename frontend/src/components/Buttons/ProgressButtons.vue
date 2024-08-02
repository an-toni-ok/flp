<script setup>
import IconArrowLeft from '../icons/IconArrowLeft.vue';
import IconArrowRight from '../icons/IconArrowRight.vue';
import IconConfirm from '../icons/IconConfirm.vue';
import ToolIconButton from '../Toolbar/ToolIconButton.vue';

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
        <ToolIconButton help_text="Go Back" @click="$emit('prev')">
            <IconArrowLeft />
        </ToolIconButton>
        <button aria-label="Continue" @click="$emit('next')">
            <IconArrowRight v-if="!complete" />
            <IconConfirm v-if="complete" />
        </button>
    </div>
</template>

<style scoped>
.progress-buttons {
    display: flex;
    justify-content: flex-end;
    z-index: 3;
}

button {
    display: flex;
    width: 10rem;
    height: var(--measurement);
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-left: -1px;
}

button > * {
    width: var(--tool-area-height);
    height: var(--tool-area-height);
}
</style>