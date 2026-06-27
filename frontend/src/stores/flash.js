import { defineStore } from 'pinia'

export const useFlash = defineStore('flash', {
  state: () => ({
    message: '',
    type: '',
    spinner: false,
    timeout: 3000
  }),
  actions: {
    showFlash(message, type='', spinner=false, timeout=3000) {
      this.message = message
      this.type = type
      this.spinner = spinner

      setTimeout(() => {
        this.message = ''
        this.type = ''
        this.spinner = false
      }, timeout)
    }
  }
})