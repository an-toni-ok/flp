<script setup>
import Navbar from './components/Navbar.vue';

const prev_session_token = localStorage.getItem("session")
if (Boolean(prev_session_token)) {
	// load previous session token
	document.cookie = prev_session_token
} else {
	// persist current session token
	localStorage.setItem("session", document.cookie)
}
</script>

<template>
	<div class="site-layout">
		<!-- <DrawingArea /> -->
		<Navbar />
		<RouterView />
		<!-- <PlanungView /> -->
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
