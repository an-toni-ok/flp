<script setup>
import Toolbar from '@/components/Toolbar.vue'
import AreaOverlay from '@/components/Overlays/AreaOverlay.vue';
import DrawingArea from '@/components/DrawingArea.vue';

</script>

<template>
    <div class="main-display">
        <div class="overlay">
            <Toolbar />
        </div>
        <DrawingArea />
        <AreaOverlay :is-create="true" />
    </div>
</template>

<style scoped>
.overlay {
    position: relative;
    /* margin: var(--site-margin-tb) var(--site-margin-lr); */
    z-index: 3;
}

.main-display {
    width: 100%;
    height: 100vh;
	overflow: hidden;
}
</style>