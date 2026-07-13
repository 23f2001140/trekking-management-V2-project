<script setup>
import { useAuth } from '@/stores/auth'
import { useFlash } from '@/stores/flash'
import router from '../../router'
import { ref, onMounted, computed } from 'vue'
import UserMyBookings from '@/components/UserMyBookings.vue'
import { RouterLink } from 'vue-router'
const auth = useAuth()
const flash = useFlash()

const fullname = computed(() => auth.user? auth.user.fullname : '')
const ongoing_bookings = ref([])
const past_bookings = ref([])


async function exportCSV() {
  
  const res = await fetch(`http://127.0.0.1:5000/api/user/export_csv`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    flash.showFlash(data.message, 'success')
    
  }
  else {
    flash.showFlash(data.message, 'danger')
    
  }   
}

async function getBookings() {
  const res = await fetch(`http://127.0.0.1:5000/api/user/booking`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth.token}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    ongoing_bookings.value = data.ongoing
    past_bookings.value = data.past

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

async function CancelTrek(id) {
  if (!confirm('Are you sure you want to cancel this booking? This action cannot be undone.')) {
    return
  }
  const res = await fetch(`http://127.0.0.1:5000/api/user/booking/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    flash.showFlash(data.message, 'success')
    await getBookings()
  }
  else {
    flash.showFlash(data.message, 'danger')
  }   
}

</script>

<template>
<div>
    <h1><i class="fa-solid fa-user mt mt-4"></i> My Bookings
    <RouterLink :to="{name: 'user'}" class="btn btn-success mt-4 float-end"><i class="fa-solid fa-arrow-left"></i> Go Back </RouterLink>
    <button class="btn btn-outline-success mt-4 float-end me-2" @click="exportCSV"> <i class="fa-solid fa-file-csv"></i> {{'Export History' }} </button>
    </h1>
    <p  class="text-muted">Hello, {{ fullname }} ! Here you can view your booking records.</p>
    <br>
    <br>
    <div v-if="ongoing_bookings.length > 0">
        <h3><strong>Ongoing Bookings</strong></h3>
        <br>
        <UserMyBookings v-for="booking in ongoing_bookings" :key="booking.id" :trek="booking.trek" :booking_status="booking.status" :booking_date="booking.booking_date" @cancel-trek="CancelTrek(booking.id)" />
        </div>
    <br>
    <div v-if="past_bookings.length > 0">
        <h3><strong>Past Bookings</strong></h3>
        <br>
        <UserMyBookings v-for="booking in past_bookings" :key="booking.id" :trek="booking.trek" :booking_status="booking.status" :booking_date="booking.booking_date" />
    </div>
    <br>
    <div v-if ="ongoing_bookings.length === 0 && past_bookings.length === 0">
        <h1 class="text-center mt-4"> No Bookings Found <i class="fa-regular fa-face-sad-tear"></i><br> Start Your Journey With Us With Your First Booking </h1>
    <br>
        <div class="text-center mt-4">
        <RouterLink :to="{name: 'user'}" class="btn btn-success"> <i class="fa-solid fa-book"></i> Book Your First Trek</RouterLink>
        </div>
    </div>
</div>
</template>