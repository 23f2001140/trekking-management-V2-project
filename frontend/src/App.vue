<script setup>
import { RouterView } from 'vue-router'
import FlashMessage from './components/FlashMessage.vue'
import NavBar from './components/NavBar.vue'
</script>

<template>
  <FlashMessage />
  <NavBar />
  <div class="container">
    <br>
      <RouterView v-slot="{ Component, route }">
        <Transition name="page" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
        </Transition>
      </RouterView>
      <br>
  </div>
</template>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}


</style>
