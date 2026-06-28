<script setup>
import {ref , onMounted} from 'vue'
import AdminTrekCard from '@/components/AdminTrekCard.vue'
import { useFlash } from '@/stores/flash'
import { useAuth } from '@/stores/auth'
const auth = useAuth()
const flash = useFlash()

const treks = ref('')

async function getTrekDetails() {
  const res = await fetch(`http://127.0.0.1:5000/api/admin/treks`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth.token}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    treks.value = data
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
    <div v-if="treks">
    <h1 class="mt-2"> View All Treks <i class="fa-solid fa-route"></i>
        <RouterLink class="btn btn-success mt-2 float-end" to="/admin/add_trek"> <i class="fa-solid fa-plus"></i> Add A New Trek</RouterLink>
    </h1>
        <br>
        <br>
        <AdminTrekCard v-for="trek in treks" :trek="trek" />
    </div>
    <div v-else>
        <h1 class="text-center mt-4"> No Treks Created <i class="fa-regular fa-face-frown"></i></h1>
        <div class="text-center mt-4">
            <RouterLink class="btn btn-info mt-4 text-center" to="/admin/add_trek"> <i class="fa-solid fa-plus"></i> Click here to Create A New Trek</RouterLink>
        </div>
    </div>
</div>
</template>