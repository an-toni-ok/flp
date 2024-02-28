<script setup>
import { usePlanningStore } from "../../../store/planning";

const store = usePlanningStore();
</script>

<template>
  <div class="content">
    <div class="description">
      <p>{{ store.DESCRIPTION }}</p>
      <p></p>
    </div>
    <div class="planning">
      <img class="image" src="/Planning.png" />
      <span class="planning-button-container">
        <button @click="store.nextPage" class="planning-button">
          Jetzt planen
        </button>
      </span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.content {
  height: max-content;

  .description {
    width: 500px;

    display: flex;
    flex-direction: column;

    text-align: left;
  }

  .planning {
    width: max-content;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-left: 60px;

    .image {
      margin-top: 100px;
      height: 400px;
      width: 600px;
    }

    .planning-button-container {
      margin-top: 10px;
    }
  }
}

@media only screen and (max-width: 1600px) {
  .content .description {
    width: 400px;
  }

  .content .planning {
    margin-left: 30px;

    .image {
      margin-top: 50px;
      height: 200px;
      width: 400px;
    }
  }
}
</style>