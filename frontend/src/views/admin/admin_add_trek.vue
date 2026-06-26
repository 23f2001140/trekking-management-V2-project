<script setup>
import {ref , onMounted, watch} from 'vue'
import {RouterLink} from 'vue-router'
import router from '../../router'

const name = ref('')
const location = ref('')
const difficulty = ref('')
const price = ref('')
const description = ref('')
const available_slots = ref('')
const assigned_staff_id = ref('')
const start_date = ref('')
const end_date = ref('')
const status = ref('')
const image_url = ref('')
const staff = ref([])

const flashMessage = ref('')
const flashType = ref('')

function showFlash(message, type) {

  flashMessage.value = message
  flashType.value = type

  setTimeout(() => {
    flashMessage.value = ''
  }, 3000)
}

async function getStaff() {
  const res = await fetch('http://127.0.0.1:5000/api/staff', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    staff.value = data
  }
  else {
    showFlash(data.message, 'danger')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setTimeout(() => {
      router.push('/')
    }, 1300)
  }
}

onMounted(async () => {
 await getStaff()
})

watch(assigned_staff_id, (newValue) => {
  if (newValue == '') {
    status.value = ''
  }
})

const validateDate = () => {
  if (start_date.value > end_date.value) {
    showFlash('Start Date should be earlier than End Date', 'danger')
    end_date.value = ''
  }
}

async function addTrek() {
  if (name.value == '' || location.value == '' || difficulty.value == '' || price.value == '' || available_slots.value == '' || start_date.value == '' || end_date.value == '') {
    showFlash('Please fill all the required fields', 'danger')
    return
  }
  if (price.value < 0) {
    showFlash('Price should be greater than 0', 'danger')
    return
  }
  if (available_slots.value < 0) {
    showFlash('Available Slots should be greater than 0', 'danger')
    return
  }
  if (assigned_staff_id.value == '' && status.value != '') {
    showFlash('You can not select trek status if you have not assigned staff', 'danger')
    return
  }
  if (assigned_staff_id.value != '' && status.value == '') {
    showFlash('You have to select trek status if you have assigned staff', 'danger')
    return
  }
  const res= await fetch('http://127.0.0.1:5000/api/trek', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify({
      name: name.value,
      location: location.value,
      difficulty: difficulty.value,
      price: price.value,
      description: description.value,
      available_slots: available_slots.value,
      assigned_staff_id: assigned_staff_id.value,
      start_date: start_date.value,
      end_date: end_date.value,
      status: status.value,
      image_url: image_url.value,
    }),
  })
  const data = await res.json()
  if (res.ok) {
    showFlash(data.message, 'success')
    setTimeout(() => {
      router.push('/admin')
    }, 2000)
  }
  else {
    showFlash(data.message, 'danger')
  }   
}




</script>

<template>
  <div v-if="flashMessage" :class="`alert alert-${flashType} position-fixed top-0 start-50 translate-middle-x mt-3`" style="z-index: 9999; min-width: 400px;">
    {{ flashMessage }}
  </div>
<h1 class="text-center mt-4"> Add Trek <i class="fa-solid fa-cable-car"></i> </h1>
<br>

<form class="row g-3" @submit.prevent="addTrek">

  <div class="col-md-6">
    <label for="name" class="form-label"><strong>Name</strong></label>
    <input v-model="name" type="text" class="form-control" id="name" required>
  </div>

  <div class="col-md-6">
    <label for="location" class="form-label"><strong>Location</strong></label>
    <input v-model="location" type="text" class="form-control" id="location" required>
  </div>

  <div class="col-md-6">
    <label for="difficulty" class="form-label"><strong>Difficulty</strong></label>
    <select v-model="difficulty" class="form-select" id="difficulty" required>
      <option value="">-- Select Difficulty --</option>
      <option value="Easy">Easy</option>
      <option value="Moderate">Moderate</option>
      <option value="Hard">Hard</option>
    </select>
  </div>

  <div class="col-md-6">
    <label for="price" class="form-label"><strong>Price</strong></label>
    <input v-model="price" type="number" class="form-control" id="price" min="1" required>
  </div>

  <div class="col-md-6">
    <label for="description" class="form-label"><strong>Description</strong></label>
    <textarea v-model="description" class="form-control" id="description" rows="3"></textarea>
  </div>

  <div class="col-md-6">
    <label for="available_slots" class="form-label"><strong>Available Slots</strong></label>
    <input v-model="available_slots" type="number" class="form-control" id="available_slots" min="1"c required>
  </div>

  <div class="col-md-6">
    <label for="assigned_staff_id" class="form-label"><strong>Assign Staff To Trek</strong></label>
    <select v-model="assigned_staff_id" class="form-select" id="assigned_staff_id">
      <option value="">-- Select Staff --</option>
      <option v-for="{ id, fullname } in staff" :key="id" :value="id">{{ fullname }}</option>
    </select>
  </div>

  <div class="col-md-3">
    <label for="start_date" class="form-label"><strong>Start Date</strong></label>
    <input v-model="start_date" type="date" class="form-control" id="start_date" @change="validateDate" required>
  </div>

  <div class="col-md-3">
    <label for="end_date" class="form-label"><strong>End Date</strong></label>
    <input v-model="end_date" type="date" class="form-control" id="end_date" :min="start_date" required>
  </div>

  <div class="col-md-6">
    <label for="status" class="form-label"><strong>Status</strong></label>
    <select v-model="status" class="form-select" id="status" :disabled="!assigned_staff_id" :required="assigned_staff_id" >
      <option value="">-- Select Status --</option>
      <option value="Approved">Approved</option>
      <option value="Open">Open</option>
    </select>
  </div>

  <div class="col-md-6">
    <label for="image_url" class="form-label"><strong>Image URL</strong></label>
    <input v-model="image_url" type="url" class="form-control" id="image_url" placeholder="https://example.com/image.jpg">
  </div>

  <div class="col-md-12 text-center" v-if="image_url">
    <img :src="image_url" class="img-thumbnail mt-2 justify-content-center" style="max-height:250px;" alt="Image Preview">
  </div>

  <br>
  <div class="text-center mt-4">
    <button type="submit" class="btn btn-primary">Add Trek</button>
  </div>
<br>
<br>

</form>
</template>