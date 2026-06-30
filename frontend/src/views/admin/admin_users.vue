<script setup>
import {ref , onMounted} from 'vue'
import router from '../../router'
import { useFlash } from '@/stores/flash'
import { useAuth } from '@/stores/auth'
const auth = useAuth()
const flash = useFlash()

const search = ref('')
const users = ref([])



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
</script>

<template>
<div>
<div v-if="users">
    <h3 class="mt-4"> View All Users Of <strong>TREKCENTRAL</strong> <i class="fa-solid fa-user-group"></i></h3>
    <br>

    <form class="d-flex align-items-center gap-2" role="search" @submit.prevent>
        <input class="form-control w-50" type="search" placeholder="Search by Name or user id" aria-label="user" id="user" name="user" v-model="search" >
        <button class="btn btn-outline-success" type="submit">
            <i class="fa-solid fa-magnifying-glass"></i> Search
        </button>
    </form>

    <br>

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
    <h1 class="text-center mt-4">
        No Users Are There
        <i class="fa-regular fa-face-frown"></i>
    </h1>
</div>

<br>
<br>
</div>
</template>