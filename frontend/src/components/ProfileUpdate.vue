<script setup>
import { ref , onMounted } from 'vue'
import { useAuth } from '@/stores/auth'
import { useFlash } from '@/stores/flash'

const auth = useAuth()
const flash = useFlash()
const fullname = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const new_password = ref('')
const cnpassword = ref('')
const message = ref('')
const pmessage = ref('')

onMounted(() => {
  const modalEl = document.getElementById('updateProfileModal')
  modalEl.addEventListener('shown.bs.modal', function () {
    fullname.value = auth.user ? auth.user.fullname : ''
    email.value = auth.user ? auth.user.email : ''
    phone.value = auth.user ? auth.user.phone : ''
    password.value = ''
    new_password.value = ''
    cnpassword.value = ''
    message.value = ''
    pmessage.value = ''
  })
})
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
  if (new_password.value == '') {
      pmessage.value = ''
  }
  else if (new_password.value.length < 6) {
      pmessage.value = 'Password must be at least 6 characters long'
  }
  else {
      pmessage.value = ''
  }
}


async function updateProfile() {
  if (new_password.value != cnpassword.value) {
    flash.showFlash('Passwords do not match', 'danger')
    return
  }
  const res= await fetch(`http://127.0.0.1:5000/api/update_profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify({
      fullname: fullname.value,
      email: email.value,
      phone: phone.value,
      password: password.value,
      new_password: new_password.value,
      cnpassword: cnpassword.value,
    }),
  })
  const data = await res.json()
  if (res.ok) {
    flash.showFlash(data.message, 'success')
    auth.login(data.user, auth.token)
    password.value = ''
    new_password.value = ''
    cnpassword.value = ''

    const modalEl = document.getElementById('updateProfileModal')
    const modalInstance = window.bootstrap.Modal.getInstance(modalEl) || new Modal(modalEl)
    modalInstance.hide()
  }
  else {
    flash.showFlash(data.message, 'danger')
    password.value = ''
    new_password.value = ''
    cnpassword.value = ''
  }
}

</script>

<template>
<div class="modal fade" id="updateProfileModal" tabindex="-1" aria-labelledby="UpdateProfileModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-md">
        <div class="modal-content">
            <div class="modal-header text-white" style="background-color: #2c7a4b;">
                <h1 class="modal-title fs-5" id="UpdateProfileModalLabel"> <i class="fa-solid fa-user-plus"></i> Update Profile </h1>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="updateProfile">
                  <div class="mb-3">
                    <label for="fullname" class="form-label">Full Name:</label>
                    <input v-model="fullname" type="text" id="fullname" name="fullname" class="form-control" required>
                  </div>
                  <div class="mb-3">
                    <label for="email" class="form-label">Email:</label>
                    <input v-model="email" type="email" id="email" name="email" class="form-control" @blur="validateEmail"  required :disabled="auth.user.role=='staff'">
                  </div>
                  <div class="mb-3">
                      <p class="text-danger" v-if="message">{{ message }}</p>
                  </div>
                  <div class="mb-3">
                    <label for="phone" class="form-label">Phone Number:</label>
                    <input v-model="phone" type="text" id="phone" name="phone" class="form-control" required>
                  </div>
                  <div class="mb-3">
                    <label for="password" class="form-label">Password:</label>
                    <input v-model="password" id="password" name="password" type="password" class="form-control" required>
                  </div>
                  <div class="mb-3">
                    <label for="new_password" class="form-label">Change Password:</label>
                    <input v-model="new_password" id="new_password" name="new_password" type="password" class="form-control" @input="validatePassword">
                  </div>
                  <div class="mb-3">
                      <p class="text-danger" v-if="pmessage">{{ pmessage }}</p>
                  </div>
                  <div class="mb-3">
                    <label for="cnpassword" class="form-label">Confirm New Password:</label>
                    <input v-model="cnpassword" id="cnpassword" name="cnpassword" type="password" class="form-control" :required="new_password.length > 0">
                  </div>
                  <br>
                  <div class="modal-footer justify-content-center">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"> Cancel </button>
                    <button class="btn btn-success" type="submit"> Update Profile </button>
                  </div>
              </form>
            </div>
        </div>
    </div>
</div>
</template>