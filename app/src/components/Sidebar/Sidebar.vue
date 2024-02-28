<script setup>
import { useSidebarStore } from "../../../store/sidebar";
import { useHeaderStore } from "../../../store/header";
import SidebarLink from "./SidebarLink.vue";

const store = useSidebarStore();
const headerStore = useHeaderStore();
const links = [
  { to: "/", icon: "fa-solid fa-pen-ruler", text: "Planung" },
  { to: "/tutorial", icon: "fa-solid fa-circle-info", text: "Tutorial" },
  { to: "/methodik", icon: "fa-solid fa-wrench", text: "Methodik" },
  { to: "/kontakt", icon: "fa-solid fa-envelope", text: "Kontakt" },
];
</script>

<template>
  <div class="sidebar" :style="{
    width: store.sidebarWidth,
    'margin-top': headerStore.headerHeight,
  }">
    <h2>
      <span v-if="store.collapsed" class="sidebar-collapsed">
        <div>Nav</div>
      </span>
      <span v-else>Navigation</span>
    </h2>

    <div v-for="item in links" :key="item.to">
      <SidebarLink :to="item.to" :icon="item.icon">
        {{ item.text }}
      </SidebarLink>
    </div>

    <span class="collapse-icon" :class="{ 'rotate-180': store.collapsed }" @click="store.toggleSidebar">
      <font-awesome-icon icon="fa-solid fa-angles-left" />
    </span>
  </div>
</template>

<style>
:root {
  --sidebar-item-hover: #f14878;
  --sidebar-item-active: #9b042f;
}
</style>

<style scoped>
.sidebar {
  color: white;
  background-color: var(--tha-red);

  float: left;
  position: fixed;
  z-index: 3;
  top: 0;
  left: 0;
  bottom: 0;

  padding: 10px;

  transition: 0.3s ease;

  display: flex;
  flex-direction: column;
}

.sidebar-collapsed {
  font-size: 0.8em;
}

.collapse-icon {
  position: absolute;
  bottom: 0;
  padding: 13px;

  color: rgba(245, 245, 245, 0.699);

  transition: 0.2s linear;
}

.rotate-180 {
  transform: rotate(180deg);
  transition: 0.2s linear;
}
</style>