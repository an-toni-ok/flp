<script setup>
import { useHeaderStore } from "../../../store/header";

const store = useHeaderStore();
</script>

<template>
  <div class="logo">
    <p class="tha">THA</p>
    <p class="flp">FLP@THA</p>
  </div>
</template>

<style scoped>
.logo {
  position: relative;
  line-height: 0.2;
  display: inline-block;
  vertical-align: middle;
  right: 0;
  width: 10%;
  margin-right: 10px;
}

.logo .tha {
  font-size: 2.5em;
  font-weight: 800;
}

.logo .flp {
  font-size: 1.8em;
}
</style>