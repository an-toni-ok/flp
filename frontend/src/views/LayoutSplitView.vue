<script setup>
import { ProgressButton } from '@/components/library/buttons';
import { InputHeading } from '@/components/library/heading';

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    number: {
        type: Number,
        required: true
    },
    totalNumber: {
        type: Number,
        default: 4
    }
})

defineEmits(['prev', 'next'])
</script>

<template>
    <div class="expand">
        <div class="view-content">
            <div class="view-data">
                <div class="view-data-header">
                    <!-- <div class="view-data-name">
                        <h1>{{ title }}</h1>
                        <p>{{ number }} von {{ totalNumber }}</p>
                    </div> -->
                    <InputHeading 
                        :title="title" 
                        :nr="number"
                        :max="totalNumber"/>
                    <slot name="header-buttons"></slot>
                </div>

                <slot name="table"></slot>
            </div>
            <ProgressButton
                @prev="$emit('prev')"
                @next="$emit('next')" />
        </div>
        <div class="side-content">
            <slot name="side-content"></slot>
        </div>
    </div>
    <slot name="overlay"></slot>
</template>

<style scoped>
.expand {
	width: 100%;
    height: 100%;
    display: inline-flex;
    overflow: hidden;
}

.view-content {
    width: fit-content;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-block: var(--site-margin-tb);
    padding-inline: var(--site-margin-lr);
    border-right: 1px solid var(--color-border);
    background-color: var(--color-background);
}

.view-data-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: calc(var(--input-height) + var(--tool-area-padding));
    gap: 4rem;
}

.view-data-name {
    display: flex;
    align-items: flex-end;
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    gap: 2rem;
    padding: var(--tool-area-padding) 1.5rem;
}

.view-data-name > h1 {
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
}

.view-data-name > p {
    line-height: 1;
    font-size: 0.8rem;
}

.side-content {
    width: 100%;
    height: 100%;
    padding-right: var(--overlay-closed-width);
}
</style>