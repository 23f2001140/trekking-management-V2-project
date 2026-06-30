<script setup>
import { useAuth } from '@/stores/auth'
import { useFlash } from '@/stores/flash'
import router from '../../router'
import { ref, onMounted } from 'vue'
import StaffTrekCard from '@/components/StaffTrekCard.vue'
const auth = useAuth()
const flash = useFlash()


const fullname = auth.user.fullname
const total_p = 5
const assigned_treks = ref('')
const registered_users = ref('')

async function getTrekDetails() {
  const res = await fetch(`http://127.0.0.1:5000/api/staff`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth.token}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    console.log(data)
    assigned_treks.value = data.treks
    registered_users.value = data.registered_users
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

</script>


<template>
<div>
    <h1><i class="fa-solid fa-user-tie"></i> Dashboard
    <h4 class="float-end">Total Participants<i class='fa-solid fa-user-group'></i>: {{ total_p }} <br>  </h4></h1>
    <br>
    <h5 class="text-muted">Welcome, {{ fullname }}! Here you can view your assigned treks and manage bookings.</h5>
    <br>
    <div v-if="assigned_treks">
        <StaffTrekCard v-for="trek in assigned_treks" :key="trek.id" :trek="trek " :registered_users="registered_users[trek.id]" />
    </div>
    <div v-else>
        <h1 class="text-center mt-4"> No Treks Assigned to you <i class="fa-regular fa-face-sad-tear"></i><br>Kindly wait for admin to assign you a trek !</h1>
    </div>
    <br>
</div>

</template>