<script setup>
import { onMounted, ref, watch } from 'vue';
import { Canvas, Color, Point, Rect } from 'fabric';
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

function generate_area(left, top, area=false, width=0, height=0) {
    var rect = new Rect({
        left: left,
        top: top,
        fill: "transparent",
        width: width,
        height: height,
    })
    rect.setControlVisible("mtr", false);
    rect.lockRotation = true;
    if (area) {
        rect.stroke = color_area;
    } else {
        rect.stroke = color_r_area;
    }
    rect.strokeUniform = true;
    rect.strokeWidth = 10;
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
        let activeObjects = canvas.getActiveObjects()
        if (activeObjects.length) {
            if ((toolbarStore.isActive(Tool.Area) &&
            activeObjects[0].stroke == color_area)) {
                return
            }
            if ((toolbarStore.isActive(Tool.RestrictedArea) && activeObjects[0].stroke == color_r_area)) {
                return
            }
        }

        let new_area = undefined;
        switch (toolbarStore.activeTool) {
            // case Tool.Move.name:
            //     this.isDragging = true;
            //     this.selection = false;
            //     this.lastPosX = evt.clientX;
            //     this.lastPosY = evt.clientY;
            case Tool.Area.name:
                this.isCreating = true;
                var pointer = canvas.getPointer(evt, true);
                this.origX = pointer.x;
                this.origY = pointer.y;
                new_area = generate_area(pointer.x, pointer.y, true, 10, 10);
                canvas.add(new_area);
                canvas.setActiveObject(new_area);
                break;
            case Tool.RestrictedArea.name:
                this.isCreating = true;
                var pointer = canvas.getPointer(evt, true);
                this.origX = pointer.x;
                this.origY = pointer.y;
                new_area = generate_area(pointer.x, pointer.y, false)
                canvas.add(new_area);
                canvas.setActiveObject(new_area);
                break;
                }
        }
    });
    canvas.on('mouse:move', function(opt) {
        // if (this.isDragging) {
        //     var e = opt.e;
        //     var vpt = this.viewportTransform;
        //     vpt[4] += e.clientX - this.lastPosX;
        //     vpt[5] += e.clientY - this.lastPosY;
        //     this.requestRenderAll();
        //     this.lastPosX = e.clientX;
        //     this.lastPosY = e.clientY;
        // }
        var evt = opt.e;
        if (this.isCreating) {
            var pointer = canvas.getPointer(evt, true);
            let area = canvas.getActiveObject();
            if(this.origX > pointer.x){
                area.set({ left: Math.abs(pointer.x) });
            }
            if(this.origY > pointer.y){
                area.set({ top: Math.abs(pointer.y) });
            }

            area.set({ width: Math.abs(this.origX - pointer.x) });
            area.set({ height: Math.abs(this.origY - pointer.y) });


            canvas.renderAll();
        }
    });
    canvas.on('mouse:up', function(opt) {
        // on mouse up we want to recalculate new interaction
        // for all objects, so we call setViewportTransform
        if (toolbarStore.isActive(Tool.Delete)) {
            let area = canvas.getActiveObject();
            canvas.remove(area);
        }

        this.setViewportTransform(this.viewportTransform);
        this.isDragging = false;
        if (this.isCreating) {
            this.isCreating = false;
            this.origX = undefined;
            this.origY = undefined;
        }
        this.selection = true;
    });
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