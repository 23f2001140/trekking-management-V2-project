<script setup>
import { useAuth } from '@/stores/auth'
import { ref, onMounted } from 'vue'
import { useFlash } from '@/stores/flash'
import { useRoute } from 'vue-router'
import router from '../../router'

const route = useRoute()
const flash = useFlash()
const auth = useAuth()

const fullname = auth.user.fullname

const trek_id = route.params.id

const name = ref('')
const location = ref('')
const difficulty = ref('')
const duration = ref('')
const available_slots = ref('')
const start_date = ref('')
const end_date = ref('')
const status = ref('')
const registered_users = ref([])
const cancelled_users = ref([])


async function getTrekDetails() {
  const res = await fetch(`http://127.0.0.1:5000/api/staff/trek/${trek_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth.token}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    name.value = data.trek.name
    location.value = data.trek.location
    difficulty.value = data.trek.difficulty
    duration.value = data.trek.duration
    available_slots.value = data.trek.available_slots
    start_date.value = data.trek.start_date
    end_date.value = data.trek.end_date
    status.value = data.trek.status === 'Approved' ? '' : data.trek.status
    registered_users.value = data.registered_users
    cancelled_users.value = data.cancelled_users
  }
  else {
    flash.showFlash(data.message, 'danger')
    auth.logout()
    router.push('/')
  }
}
onMounted(async () => {
 await getTrekDetails()
})


async function updateStatus() {
    const res = await fetch(`http://127.0.0.1:5000/api/staff/trek/${trek_id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${auth.token}`
        },
        body: JSON.stringify({
            status: status.value
        })
    })
    const data = await res.json()
    if (res.ok) {
        flash.showFlash(data.message, 'success', true, 1000)
    }
    else {
        flash.showFlash(data.message, 'danger')
    }
}

async function updateSlots() {
    const res = await fetch(`http://127.0.0.1:5000/api/staff/trek/${trek_id}`, {
    method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${auth.token}`
        },
        body: JSON.stringify({
            available_slots: available_slots.value
        })
    })
    const data = await res.json()
    if (res.ok) {
        flash.showFlash(data.message, 'success', true, 1000)
    }
    else {
        flash.showFlash(data.message, 'danger')
    }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<template>
    <div>   
        <h1>Manage Trek And View Participants
            <RouterLink :to="{ name: 'staff' }" class="btn btn-success mt-2 float-end ms-2"><i class="fa-solid fa-arrow-left"></i> Go Back </RouterLink>
        </h1>
        <p>Hello, {{ fullname }}! Here you can view participants and update the status and slots of the trek.</p>
        <br>
        <div class="row g-3 d-flex justify-content-between">
            <div class="card shadow-sm p-4" style="width: 18rem; border-radius: 14px;">
                <div class="card-header">
                    {{ name }}
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">Location: {{ location }}</li>
                    <li class="list-group-item">Difficulty: {{ difficulty }}</li>
                    <li class="list-group-item">Duration: {{ duration }} days</li>
                    <li class="list-group-item">Start Date: {{ formatDate(start_date) }}</li>
                    <li class="list-group-item">End Date: {{ formatDate(end_date) }}</li>
                </ul>
            </div>
            <div class="col-md-3">
                <form action=""  @submit.prevent="updateStatus">
                    <label for="status" class="form-label"><strong>Change Status</strong></label>
                        <select v-model="status" class="form-select" id="status" name="status" required>
                            <option value="">-- ChangeStatus --</option>
                            <option value="Open">Open</option>
                            <option value="Closed">Closed</option>
                            <option value="Started">Started</option>
                            <option value="Completed">Completed</option>
                        </select>
                        <button type="submit" class="btn btn-primary mt-2">Update Status</button>
                    </form>
            </div>
            <div class="col-md-3">
                <form action="" @submit.prevent="updateSlots">
                        <label for="available_slots" class="form-label"><strong>Available Slots</strong></label>
                        <input v-model="available_slots" type="number" class="form-control" id="available_slots" name="available_slots" required>
                        <button type="submit" class="btn btn-primary mt-2">Update Slots</button>
                </form>
            </div>
            <template v-if='registered_users.length>0 || cancelled_users.length>0'>
                <h3><strong>Participants</strong></h3>
                    <br>
                    <table class="table table-hover shadow-lg p-4">
                        <thead class="table-primary">
                            <tr>
                            <th scope="col">Name</th>
                            <th scope="col">Phone Number</th>
                            <th scope="col">Booked On</th>
                            <th scope="col">Status</th>
                            </tr>
                        </thead>
                        <tbody v-for="{ id, user , booking_date, status } in registered_users" :key="id" >
                            <tr class="table-success" >     
                                <th scope="row">{{ user.fullname }}</th>
                                <td>{{ user.phone }}</td>
                                <td>{{ formatDate(booking_date) }}</td>
                                <td>{{ status }}</td>
                            </tr>
                        </tbody>
                        <tbody v-for="{ id, user , booking_date, status } in cancelled_users" :key="id" >
                            <tr class="table-danger" >     
                                <th scope="row">{{ user.fullname }}</th>
                                <td>{{ user.phone }}</td>
                                <td>{{ formatDate(booking_date) }}</td>
                                <td>{{ status }}</td>
                            </tr>
                        </tbody>
                    </table>
            </template>
            <template v-else>
                <h1 class="text-center mt-4"> No Participants Yet <i class="fa-regular fa-face-sad-tear"></i></h1>
            </template>

        </div>
        <br>
        <br>
    </div>
</template>