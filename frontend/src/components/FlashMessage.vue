<script setup>
import { useFlash } from '@/stores/flash'
const flash = useFlash()
</script>

<template>
  <div v-if="flash.message" :class="`alert alert-${flash.type} position-fixed top-0 start-50 translate-middle-x mt-3 d-flex align-items-center shadow-lg border-0 rounded-3 px-4 py-3`" style="z-index: 9999; min-width: 400px;" role="alert">
    <strong class="me-2">{{ flash.message }}</strong>

    <div v-if="flash.spinner" :class="`spinner-border spinner-border-sm text-${flash.type} ms-auto `" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>