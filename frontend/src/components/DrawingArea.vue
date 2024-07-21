<script setup>
import { onMounted, ref, watch } from 'vue';
import { Canvas, Rect } from 'fabric';
import { useToolbarStore } from '@/stores/toolbar';
import { Tool } from '@/util';

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

const toolbarStore = useToolbarStore();

onMounted(() => {
    canvas = new Canvas(can_ref.value);
    setCanvasSize(canvas)

    const resizeObserver = new ResizeObserver(() => {
        setCanvasSize(canvas);
    })
    resizeObserver.observe(can_cont_ref.value);

    // Zoom
    // Button inputs
    watch(
        () => toolbarStore.zoom,
        (zoom) => {
            canvas.zoomToPoint(new Point(canvas.width / 2, canvas.height / 2), zoom / 100);
        }
    );
    // Mouse wheels
    // Based on http://fabricjs.com/fabric-intro-part-5
    canvas.on('mouse:wheel', function(opt) {
        var delta = opt.e.deltaY;
        var old_zoom = (toolbarStore.zoom / 100);
        var new_zoom = Math.round((old_zoom * (0.999 ** delta)) * 10) * 10
        toolbarStore.setZoom(new_zoom);
        canvas.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, new_zoom / 100);
        opt.e.preventDefault();
        opt.e.stopPropagation();
    });

    // Moving around the canvas
    // Based on http://fabricjs.com/fabric-intro-part-5
    canvas.on('mouse:down', function(opt) {
        var evt = opt.e;
        if (toolbarStore.isActive(Tool.Move)) {
            this.isDragging = true;
            this.selection = false;
            this.lastPosX = evt.clientX;
            this.lastPosY = evt.clientY;
        }
    });
    canvas.on('mouse:move', function(opt) {
        if (this.isDragging) {
            var e = opt.e;
            var vpt = this.viewportTransform;
            vpt[4] += e.clientX - this.lastPosX;
            vpt[5] += e.clientY - this.lastPosY;
            this.requestRenderAll();
            this.lastPosX = e.clientX;
            this.lastPosY = e.clientY;
        }
    });
    canvas.on('mouse:up', function(opt) {
        // on mouse up we want to recalculate new interaction
        // for all objects, so we call setViewportTransform
        this.setViewportTransform(this.viewportTransform);
        this.isDragging = false;
        this.selection = true;
    });
    
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