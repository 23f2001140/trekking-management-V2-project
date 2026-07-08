<script setup>
import {ref , onMounted, watch} from 'vue'
import router from '@/router'
import { useFlash } from '@/stores/flash'
import { useAuth } from '@/stores/auth'

const auth = useAuth()
const flash = useFlash()
const bookings = ref([])
const all_bookings = ref([])
const user_id = ref('')

async function getBookings() {
  const res = await fetch('http://127.0.0.1:5000/api/admin/bookings', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth.token}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    all_bookings.value = data
    bookings.value = data
  }
  else {
    flash.showFlash(data.message, 'danger')
    auth.logout()
    router.push('/')
  }
}

onMounted(async () => {
 await getBookings()
})

watch(user_id, function () {
  if (user_id.value == '') {
    bookings.value = all_bookings.value
  }
  else {
    bookings.value = all_bookings.value.filter(function (booking) {
      return booking.user_id == user_id.value
    })
  }
})

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

    <h1 class=" mt-4"><i class="fa-solid fa-history"></i>  View All Bookings (Latest First)  </h1>
    <br>
    <form class="d-flex align-items-center gap-2" role="search" @submit.prevent>
        <input class="form-control w-50" type="number" placeholder="Search Booking by User id" aria-label="user" id="user" name="user" v-model="user_id" >
        <button class="btn btn-outline-success" type="submit">
          <i class="fa-solid fa-magnifying-glass"></i> Search
        </button>
      </form>
    <br>
    <div v-if="bookings.length > 0">
    <table class="table table-hover shadow-lg p-4">
        <thead class="table-primary">
            <tr>
            <th scope="col">Booking id</th>
            <th scope="col">User id</th>
            <th scope="col">Username</th>
            <th scope="col">Trek id</th>
            <th scope="col">Trek Name</th>
            <th scope="col">Trek Location</th>
            <th scope="col">Booking Date</th>
            <th scope="col">Status</th>
            </tr>
        </thead>
        <tbody v-for="{ id, user_id, trek_id, booking_date, status , user_name, trek_name, trek_location } in bookings" :key="id" >
            <tr :class="status === 'Booked' ? 'table-success' : status === 'Cancelled' ? 'table-danger' : 'table-warning'">
                <th scope="row">{{ id }}</th>
                <td>{{ user_id }}</td>
                <td>{{ user_name }}</td>
                <td>{{ trek_id }}</td>
                <td>{{ trek_name }}</td>
                <td>{{ trek_location }}</td>
                <td>{{ formatDate(booking_date) }}</td>
                <td>{{ status }}</td>
            </tr>
        </tbody>
    </table>
    </div>
    <div v-else>
      <template v-if="all_bookings.length === 0">
        <h1 class="text-center mt-4">
            No Bookings Are There
            <i class="fa-regular fa-face-frown"></i>
        </h1>
        </template>
        <template v-else>
          <h1 class="text-center mt-4">
            No Bookings Found With This Id
            <i class="fa-regular fa-face-frown"></i>
          </h1>
        </template>
    </div>
</div>
</template>