<script setup>
import { RouterLink } from 'vue-router'
import { useAuth } from '@/stores/auth'
import { useFlash } from '@/stores/flash'
import router from '../../router'
import { ref, onMounted, computed } from 'vue'
import UserTrekCard from '@/components/UserTrekCard.vue'
const auth = useAuth()
const flash = useFlash()

const fullname = computed(() => auth.user? auth.user.fullname : '')
const treks = ref([])
const upcoming_treks = ref([])
const bookings_status = ref([])


async function getTrekDetails() {
  const res = await fetch(`http://127.0.0.1:5000/api/user`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth.token}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    treks.value = data.treks
    upcoming_treks.value = data.upcoming_treks
    bookings_status.value = data.bookings_status
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

async function bookTrek(id) {
  const res = await fetch(`http://127.0.0.1:5000/api/user/booking/${id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    flash.showFlash(data.message, 'success')
    await getTrekDetails()
  }
  else {
    flash.showFlash(data.message, 'danger')
  }   
}
</script>





<template>
<div>
    <h1><i class="fa-solid fa-user mt mt-4"></i> Dashboard
    <RouterLink :to="{name: 'user_mybookings'}" class="btn btn-success mt-4 float-end"><i class="fa-solid fa-book"></i> My Bookings | {{Object.keys(bookings_status).length}} </RouterLink> </h1>
    <p  class="text-muted">Welcome, {{ fullname }} !</p>
    <br>
    <br>
    <div class='d-flex justify-content-between align-items-center'>
        <h3><strong>Explore Treks</strong></h3>
    <!-- <form class="d-flex align-items-center gap-2" role="search" @submit.prevent>
        <select class="form-select" id="difficulty" name="difficulty">
            <option value="">Select Difficulty</option>
            <option value="Easy">Easy</option>
            <option value="Moderate">Moderate</option>
            <option value="Hard">Hard</option>
        </select>
        <input class="form-control w-auto" style="min-width: 250px;" type="search" placeholder="Search Location" aria-label="location" id="location" name="location" value="">
        <button class="btn btn-outline-success d-flex align-items-center gap-1" type="submit"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
    </form> -->
    </div>
    <br>
    <div v-if="treks.length > 0">
        <UserTrekCard v-for="trek in treks" :key="trek.id" :trek="trek" :booking_status="bookings_status[trek.id]" @book-trek="bookTrek(trek.id)" />
    </div>

    <div v-else>
        <h1 class="text-center mt-4"> Oops! No Treks Are Available At The Moment <i class="fa-regular fa-face-sad-tear"></i><br> Stay Tuned For Upcoming New Treks </h1>
    </div>
    <br>
    <div v-if="upcoming_treks.length > 0">
        <h3><strong>Upcoming Treks</strong></h3>
        <br>
        <UserTrekCard v-for="trek in upcoming_treks" :key="trek.id" :trek="trek" />
    </div>

</div>
</template>