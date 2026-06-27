<script setup>
import { RouterView } from 'vue-router'
import FlashMessage from './components/FlashMessage.vue'
</script>

<template>
  <FlashMessage />
  <div class="container">
    <br>
    <RouterView />
  </div>
</template>

<style scoped>
</style>
