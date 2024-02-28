<script setup>
import { useFooterStore } from "../../../store/footer";
import { usePlanningStore } from "../../../store/planning";

const store = useFooterStore();
const planningStore = usePlanningStore();

const emit = defineEmits(['continue']);

const continueButtonClick = () => {
    emit('continue');
    planningStore.nextPage();
}
</script>

<template>
  <footer class="footer-container">
    <div class="planning-button-container">
      <button class="planning-button" @click="planningStore.previousPage"> {{ store.returnButtonText }} </button>
    </div>
    <div v-if="planningStore.page !== 7 && planningStore.page !== 6" class="planning-button-container">
      <button class="planning-button" @click="continueButtonClick">{{ store.continueButtonText }}</button>
    </div>
  </footer>
</template>

<style scoped lang="scss">
.footer-container {
  z-index: 2;
  height: 100px;

  position: absolute;
  bottom: 0px;
  width: 100%;

  display: flex;
  align-items: center;
  justify-content: right;
}

.planning-button-container {
  width: max-content;
  margin-right: 50px;

  .planning-button {
    width: 320px;
  }
}
</style>