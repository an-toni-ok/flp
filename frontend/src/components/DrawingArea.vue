<script setup>
import { onMounted, ref, watch } from 'vue';
import { Canvas, Rect } from 'fabric';

// Only has value after mount, use onMounted
const can_ref = ref(null)
const can_cont_ref = ref(null)
let color_area = "#4CAF50"
let color_r_area = "#D32F2F"
let color_machine = "#FF9800"
let canvas = undefined

function rect_gen(left, top, stroke_color, width=100, height=100) {
    var rect = new Rect({
        left: left,
        top: top,
        fill: "transparent",
        width: width,
        height: height,
    })
    rect.setControlVisible("mtr", false)
    rect.lockRotation = true
    rect.stroke = stroke_color
    rect.strokeUniform = true
    rect.strokeWidth = 10
    return rect
}

function setCanvasSize(canvas) {
    canvas.setDimensions({
            width: can_cont_ref.value.clientWidth,
            height: can_cont_ref.value.clientHeight
        }
    )
}

onMounted(() => {
    canvas = new Canvas(can_ref.value);
    setCanvasSize(canvas)

    const resizeObserver = new ResizeObserver(() => {
        setCanvasSize(canvas);
    })
    resizeObserver.observe(can_cont_ref.value);

    var rect = rect_gen(50, 50, color_area)
    canvas.add(rect)
    var rect2 = rect_gen(150, 150, color_r_area)
    canvas.add(rect2)
    var rect3 = rect_gen(250, 250, color_machine)
    canvas.add(rect3)
})
</script>

<template>
    <div class="canvas-content" ref="can_cont_ref">
        <canvas ref="can_ref">
        </canvas>
    </div>        

</template>

<style scoped>
.overflow-hider {
    display: flex;
    width: inherit;
    height: 100%;
    overflow: hidden;
}

.canvas-content {
    width: 100%;
    height: 100%;
}
</style>