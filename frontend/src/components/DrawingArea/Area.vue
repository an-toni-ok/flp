<script setup>
import { onMounted, ref } from 'vue';

const props = defineProps({
    width: {
        type: Number,
        required: true
    },
    height: {
        type: Number,
        required: true
    },
    posX: {
        type: Number,
        required: true
    },
    posY: {
        type: Number,
        required: true
    }
})

const area = ref(undefined)

onMounted(() => {
    area.value.style.width = props.width
    area.value.style.height = props.height
    area.value.style.top = props.posY + "px"
    area.value.style.left = props.posX + "px"
})
</script>

<template>
    <div class="area" ref="area"></div>
</template>

<style scoped>
.area {
    position: absolute;
    top: 0;
    left: 0;
    height: 100px;
    width: 100px;
    background-color: black;
}
</style>