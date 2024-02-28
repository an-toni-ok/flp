<script setup>
import { ref, watch } from 'vue';
const tooltip = ref();
const tooltipText = ref();
const tooltipRect = ref();

const props = defineProps({
    text: {
        type: String,
        required: true,
    },
    visible: {
        type: Boolean,
        required: true,
    },
    position: {
        type: Object,
        required: true
    }
});

watch(
    () => props.position,
    (position) => {
    const tooltipNode = tooltip.value.getNode();
    tooltipNode.position(position);
});

watch(
    () => props.visible,
    (visible) => {
    const tooltipNode = tooltip.value.getNode();
    if(visible === true) {
        tooltipNode.show();
    } else {
        tooltipNode.hide();
    }
});

watch(
    () => props.text,
    (text) => {
    const tooltipTextNode = tooltipText.value.getNode();
    const rectNode = tooltipRect.value.getNode();

    tooltipTextNode.text(text);
    rectNode.width(tooltipTextNode.width());
    rectNode.height(tooltipTextNode.height());
});

// Config for tooltip group
const configTooltip = {
    x: props.position.x,
    y: props.position.y,
    visible: props.visible
};

// Config for tootip text
const configTooltipText = {
    x: 0,
    y: 0,
    text: props.text,
    fontFamily: 'Calibri',
    fontSize: 15,
    lineHeight: 1.2,
    padding: 10,
    fill: 'black',
};

// Config for tooltip frame
const configTooltipRect = {
    x: 0,
    y: 0,
    stroke: 'black',
    strokeWidth: 1,
    fill: 'white',
    cornerRadius: 10,
};
</script>

<template>
    <v-layer>
        <v-group :config="configTooltip" ref="tooltip">
            <v-rect :config="configTooltipRect" ref="tooltipRect"></v-rect>
            <v-text :config="configTooltipText" ref="tooltipText"></v-text>
        </v-group>
    </v-layer>
</template>

<style scoped></style>