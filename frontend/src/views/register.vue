<script setup>
import { RouterLink } from 'vue-router'
import {ref} from 'vue'
import router from '../router'
import { useFlash } from '@/stores/flash'

const flash = useFlash()


const email = ref('')
const fullname = ref('')
const phone = ref('')
const password = ref('')
const cpassword = ref('')
const message = ref('')
const pmessage = ref('')

const validateEmail = () => {
    if (email.value == '') {
        message.value = ''
    }
    else if (!email.value.includes('@') || !email.value.includes('.')) {
        message.value = 'Please enter a valid email address'
    }
    else {
        message.value = ''
    }
}

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
async function registerUser() {
  if (password.value != cpassword.value) {
    flash.showFlash('Passwords do not match', 'danger')
    return
  }
  const res= await fetch('http://127.0.0.1:5000/api/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email.value,
      password: password.value,
      cpassword: cpassword.value,
      fullname: fullname.value,
      phone: phone.value,
    }),
  })
  const data = await res.json()
  if (res.ok) {
    flash.showFlash(data.message, 'success', true , 1000)
    setTimeout(() => {
      router.push('/')} , 1000)
  }
  else {
    flash.showFlash(data.message, 'danger')
  }
}


</script>

<template>
<div class="container d-flex justify-content-center align-items-center mt-5">
  <div class="card shadow-lg p-4" style="width: 100%; max-width: 480px; border-radius: 16px;">
    <div class="card-body">

      <h1 class="text-center fw-bold mb-1" style="color: #2c7a4b;">TrekCentral</h1>
      <p class="text-center text-muted mb-4">Register your account by filling out the form below:</p>

      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label for="email" class="form-label">Email:</label>
          <input v-model="email" type="email" id="email" name="email" class="form-control" @blur="validateEmail" required>
        </div>
        <div class="mb-3">
            <p class="text-danger" v-if="message">{{ message }}</p>
        </div>
        <div class="mb-3">
          <label for="fullname" class="form-label">Full Name:</label>
          <input v-model="fullname" type="text" id="fullname" name="fullname" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="phone" class="form-label">Phone Number:</label>
          <input v-model="phone" type="text" id="phone" name="phone" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password:</label>
          <input v-model="password" id="password" name="password" type="password" class="form-control" @input="validatePassword" required>
        </div>
        <div class="mb-3">
            <p class="text-danger" v-if="pmessage">{{ pmessage }}</p>
        </div>
        <div class="mb-3">
          <label for="cpassword" class="form-label">Confirm Password:</label>
          <input v-model="cpassword" id="cpassword" name="cpassword" type="password" class="form-control" required>
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-success">Register</button>
        </div>
      </form>

      <hr class="my-3">
      <p class="text-center mb-0">
        Already have an account?
        <RouterLink to="/" class="btn btn-outline-primary btn-sm ms-1">Login here</RouterLink>
      </p>

    </div>
  </div>
</div>
</template>