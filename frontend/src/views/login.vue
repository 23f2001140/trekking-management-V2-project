<script setup>
import { RouterLink } from 'vue-router'
import router from '../router'
import {ref} from 'vue'
import { useFlash } from '@/stores/flash'
import { useAuth } from '@/stores/auth'

const auth = useAuth()

const flash = useFlash()

const password = ref('user123')
const email = ref('user2@gmail.com')
const pmessage = ref('')


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
    flash.showFlash(data.message, 'success', true, 1000)
    setTimeout(() => {
      auth.login(data.user, data.access_token)
      if (auth.role == 'admin') {
        router.push('/admin')
      }
      else if (auth.role == 'staff') {
        router.push('/staff')
      }
      else {
        router.push('/user')
      }
    } , 1000)
  }
  else {
    flash.showFlash(data.message, 'danger')
  }
}
</script>

<template>
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