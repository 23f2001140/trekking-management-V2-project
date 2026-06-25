<script setup>
import { RouterLink } from 'vue-router'
import router from '../router'
import {ref} from 'vue'

const password = ref('')
const email = ref('')
const pmessage = ref('')
const flashMessage = ref('')
const flashType = ref('')

const validatePassword = () => {
  if (password.value == '') {
      pmessage.value = ''
  }
  else if (password.value.length < 6) {
      pmessage.value = 'Password must be at least 6 characters long'
  }
  else {
      pmessage.value = ''
  }
}
function showFlash(message, type) {

  flashMessage.value = message
  flashType.value = type

  setTimeout(() => {
    flashMessage.value = ''
  }, 3000)
}
async function loginUser() {
  const res= await fetch('http://127.0.0.1:5000/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email.value,
      password: password.value,
    }),
  })
  const data = await res.json()
  if (res.ok) {
    showFlash(data.message, 'success')
    setTimeout(() => {
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      if (data.user.role == 'admin') {
        router.push('/admin')
      }
      else {
        router.push('/user')
      }
    } , 1000)
  }
  else {
    showFlash(data.error, 'danger')
  }
}
</script>

<template>
<div v-if="flashMessage" :class="`alert alert-${flashType} position-fixed top-0 start-50 translate-middle-x mt-3`" style="z-index: 9999; min-width: 400px;">
  {{ flashMessage }}
</div>
<div class="container d-flex justify-content-center align-items-center mt-5">
  <div class="card shadow-lg p-4" style="max-width: 420px; border-radius: 16px;">
    <div class="card-body">

      <h1 class="text-center fw-bold mb-1" style="color: #2c7a4b;">TrekCentral</h1>
      <p class="text-center text-muted mb-4">Your one-stop destination for all things trekking!</p>

      <h2 class="text-center fs-4 fw-semibold mb-3">Login</h2>

      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label for="email" class="form-label">Email:</label>
          <input v-model="email" type="email" id="email" name="email" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password:</label>
          <input v-model="password" type="password" id="password" name="password" class="form-control" @input="validatePassword" required>
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-success">Login</button>
        </div>
      </form>

      <hr class="my-3">
      <p class="text-center mb-0">
        Don't have an account?
        <RouterLink to="/register" class="btn btn-outline-primary btn-sm ms-1">Register here</RouterLink>
      </p>

    </div>
  </div>
</div>
</template>