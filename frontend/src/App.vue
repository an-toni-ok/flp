<script setup>
import Navbar from './components/Navbar.vue';
import TechnologyDropdownInput from './components/Inputs/TechnologyDropdownInput.vue';
import AreaOverlay from './components/Overlays/AreaOverlay.vue';
import AreaView from './views/AreaView.vue';
import DrawingArea from './components/DrawingArea.vue';
import PlanungView from './views/PlanungView.vue';
</script>

<template>
	<div class="site-layout">
		<!-- <DrawingArea /> -->
		<Navbar />
		<PlanungView />
			<!-- <TechnologyDropdownInput 
				:is-changeable="true"
				:is-deletable="true" /> -->
	</div>

</template>

<style scoped>
.site-layout {
	display: flex;
	width: 100%;
	height: 100%;
}
</style>
