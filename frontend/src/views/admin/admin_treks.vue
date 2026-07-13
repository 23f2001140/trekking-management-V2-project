<script setup>
import {ref , onMounted, watch} from 'vue'
import AdminTrekCard from '@/components/AdminTrekCard.vue'
import { useFlash } from '@/stores/flash'
import { useAuth } from '@/stores/auth'
import router from '../../router'
const auth = useAuth()
const flash = useFlash()

const difficulty = ref('')
const location = ref('')
const duration = ref('')
const all_treks = ref([])
const treks = ref([])

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
    all_treks.value = data
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

watch([difficulty, location, duration], function () {

  let temp_treks = []

  if (difficulty.value == '' && location.value == '') {
    temp_treks = all_treks.value
  }

  else if (difficulty.value != '' && location.value == '') {
    temp_treks = all_treks.value.filter(function (trek) {
      return trek.difficulty == difficulty.value
    })
  }

  else if (difficulty.value == '' && location.value != '') {
    temp_treks = all_treks.value.filter(function (trek) {
      let trek_location = trek.location.toLowerCase()
      let typed_location = location.value.toLowerCase()
      return trek_location.includes(typed_location)
    })
  }

  else {
    temp_treks = all_treks.value.filter(function (trek) {
      let trek_location = trek.location.toLowerCase()
      let typed_location = location.value.toLowerCase()
      let location_matches = trek_location.includes(typed_location)
      let difficulty_matches = (trek.difficulty == difficulty.value)
      return location_matches && difficulty_matches
    })
  }

  if (duration.value == '') {
    treks.value = temp_treks
  }
  else {
    treks.value = temp_treks.filter(function (trek) {
      return trek.duration <= duration.value
    })
  }
})



</script>

<template>
<div>
  <h1 class="mt-2"> View All Treks <i class="fa-solid fa-route"></i>
    <RouterLink class="btn btn-success mt-2 float-end" to="/admin/add_trek"> <i class="fa-solid fa-plus"></i> Add A New Trek</RouterLink>
  </h1>
  <form class="d-flex col-md-8 gap-2" role="search" @submit.prevent>
    <select class="form-select" id="difficulty" name="difficulty" v-model="difficulty">
      <option value="">Select Difficulty</option>
      <option value="Easy">Easy</option>
      <option value="Moderate">Moderate</option>
      <option value="Hard">Hard</option>
    </select>
    <input class="form-control w-auto" style="min-width: 200px;" type="search" placeholder="Search Duration " aria-label="duration" id="duration" name="duration" v-model="duration">
    <input class="form-control w-auto" style="min-width: 250px;" type="search" placeholder="Search Location " aria-label="location" id="location" name="location" v-model="location">
    <button class="btn btn-outline-success d-flex align-items-center gap-1" type="submit"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
  </form>
  <br>
  <br>
    <div v-if="treks.length > 0">
        <AdminTrekCard v-for="trek in treks" :key="trek.id" :trek="trek" />
    </div>
    <div v-else>
      <template v-if="all_treks.length === 0">
        <h1 class="text-center mt-4"> No Treks Created <i class="fa-regular fa-face-frown"></i></h1>
        <div class="text-center mt-4">
            <RouterLink class="btn btn-info mt-4 text-center" to="/admin/add_trek"> <i class="fa-solid fa-plus"></i> Click here to Create A New Trek</RouterLink>
        </div>
      </template>
      <template v-else>
        <h1 class="text-center mt-4"> No Matching Treks Found <i class="fa-regular fa-face-frown"></i></h1>
      </template>
    </div>
</div>
</template>