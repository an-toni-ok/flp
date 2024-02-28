<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useSidebarStore } from "../../../store/sidebar";

const store = useSidebarStore();

const props = defineProps({
  to: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
    required: true,
  },
});

const route = useRoute();
const isActive = computed(() => route.path === props.to);
</script>

<template>
  <router-link :to="props.to" class="link" :class="{ active: isActive }">
    <font-awesome-icon class="icon" :icon="props.icon" />
    <Transition name="fade">
      <span v-if="!store.collapsed">
        <slot />
      </span>
    </Transition>
  </router-link>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s;
}

.fate-enter,
.fate-leave-to {
  opacity: 0;
}

.link {
  display: flex;
  align-items: center;

  cursor: pointer;
  position: relative;
  font-weight: 400;
  user-select: none;

  margin: 2px 0;
  padding: 6px;
  border-radius: 4px;
  height: 24px;

  color: white;
  text-decoration: none;
}

.link:hover {
  background-color: var(--sidebar-item-hover);
  transition: background-color 0.2s;
}

.link.active {
  background-color: var(--sidebar-item-active);
}
.link .icon {
  flex-shrink: 0;
  width: 25px;
  margin-right: 10px;
}
</style>