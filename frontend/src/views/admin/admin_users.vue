<script setup>
import {ref , onMounted, watch} from 'vue'
import router from '../../router'
import { useFlash } from '@/stores/flash'
import { useAuth } from '@/stores/auth'
const auth = useAuth()
const flash = useFlash()

const name_id = ref('')
const users = ref([])
const all_users = ref([])



async function getUsers() {
  const res = await fetch('http://127.0.0.1:5000/api/admin/users', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    all_users.value = data
    users.value = data
  }
  else {
    flash.showFlash(data.message, 'danger', true)
    auth.logout()
    router.push('/')
  }
}

onMounted(async () => {
 await getUsers()
})



async function blacklistUser(id) {
  const res = await fetch(`http://127.0.0.1:5000/api/admin/users/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify({
      is_blacklisted: true,
    }),
  })
  const data = await res.json()
  if (res.ok) {
    flash.showFlash(data.message, 'success')
    getUsers()
  }
  else {
    flash.showFlash(data.message, 'danger')
  }   
}

async function activateUser(id) {
  const res = await fetch(`http://127.0.0.1:5000/api/admin/users/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify({
      is_blacklisted: false,
    }),
  })
  const data = await res.json()
  if (res.ok) {
    flash.showFlash(data.message, 'success')
    getUsers()
  }
  else {
    flash.showFlash(data.message, 'danger')
  }   
}


function isNumber(value) {
  return !isNaN(value) && !isNaN(parseFloat(value));
}

watch(name_id, function () {
  if (name_id.value == '') {
    users.value = all_users.value
  }
  else if (isNumber(name_id.value)) {
    users.value = all_users.value.filter(function (user) {
      return user.id == name_id.value
    })
  }
  else {
    users.value = all_users.value.filter(function (user) {
      let user_name = user.fullname.toLowerCase()
      let typed_name = name_id.value.toLowerCase()
      return user_name.includes(typed_name)
    })
  }
})
</script>

<template>
<div>
  <h3 class="mt-4"> View All Users Of <strong>TREKCENTRAL</strong> <i class="fa-solid fa-user-group"></i></h3>
  <br>
  
  <form class="d-flex align-items-center gap-2" role="search" @submit.prevent>
    <input class="form-control w-50" type="search" placeholder="Search by Name or user id" aria-label="user" id="user" name="user" v-model="name_id" >
    <button class="btn btn-outline-success" type="submit">
      <i class="fa-solid fa-magnifying-glass"></i> Search
    </button>
  </form>
  
  <br>
  
  <div v-if="users.length > 0">
    <table class="table table-hover shadow-lg p-4">
        <thead class="table-primary">
            <tr>
                <th scope="col">User id</th>
                <th scope="col">Email</th>
                <th scope="col">Full Name</th>
                <th scope="col">Phone Number</th>
                <th scope="col">Account Status</th>
                <th scope="col">Action</th>
            </tr>
        </thead>

        <tbody v-for="{ id, email, fullname, phone, is_blacklisted } in users" :key="id" >
            <tr v-if="!is_blacklisted" class="table-success" >
                <th scope="row">{{ id }}</th>
                <td>{{ email }}</td>
                <td>{{ fullname }}</td>
                <td>{{ phone }}</td>
                <td>{{ is_blacklisted ? 'Blacklisted' : 'Active' }}</td>
                <td> <a class="btn btn-outline-danger" href="#" @click.prevent="blacklistUser(id)"> <i class="fa-regular fa-circle-xmark"></i> Blacklist </a> </td>
            </tr>
        </tbody>

        <tbody v-for="{ id, email, fullname, phone, is_blacklisted } in users" :key="'blacklisted-' + id" >
            <tr v-if="is_blacklisted" class="table-danger" >
                <th scope="row">{{ id }}</th>
                <td>{{ email }}</td>
                <td>{{ fullname }}</td>
                <td>{{ phone }}</td>
                <td>{{ is_blacklisted ? 'Blacklisted' : 'Active' }}</td>
                <td> <a class="btn btn-outline-success" href="#" @click.prevent="activateUser(id)"> <i class="fa-regular fa-circle-check"></i> Activate </a> </td>
            </tr>
        </tbody>

    </table>
</div>

<div v-else>
  <template v-if="all_users.length === 0">
    <h1 class="text-center mt-4">
        No Users Are There
        <i class="fa-regular fa-face-frown"></i>
    </h1>
  </template>
  <template v-else>
    <h1 class="text-center mt-4">
      No Users Found With This Name Or Id
      <i class="fa-regular fa-face-frown"></i>
    </h1>
  </template>
</div>

<br>
<br>
</div>
</template>