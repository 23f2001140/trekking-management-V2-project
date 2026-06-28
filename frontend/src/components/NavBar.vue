<script setup>
import { RouterLink } from 'vue-router'
import router from '../router'

import { useFlash } from '@/stores/flash'
import { useAuth } from '@/stores/auth'
const flash = useFlash()
const auth = useAuth()

const logout = () => {
  auth.logout()
  flash.showFlash('You have been logged out', 'success')
  router.push('/')
}

</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">

      <RouterLink class="navbar-brand fw-bold" style="color: #2c7a4b;" :to="auth.isLoggedIn ? `/${auth.role}` : '/'"> TrekCentral</RouterLink>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <!-- Logged Out -->
          <template v-if="!auth.isLoggedIn">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/"> Login </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/register"> Register </RouterLink>
            </li>

          </template>

          <!-- Admin -->
          <template v-else-if="auth.role === 'admin'">

            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'admin'}"> Home </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'admin_users'}"> Users </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'admin_staff'}"> Staff </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'admin_treks'}"> Treks </RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'admin'}"> Bookings </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'admin'}"> Profile </RouterLink>
            </li>

            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout"> Logout </a>
            </li>

          </template>

          <!-- Staff -->
          <template v-else-if="auth.role === 'staff'">

            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'staff'}"> Home </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'staff_profile'}"> Profile </RouterLink>
            </li>

            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout"> Logout </a>
            </li>

          </template>

          <!-- User -->
          <template v-else>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'user'}"> Home </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'user_profile'}  "> Profile </RouterLink>
            </li>
            
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name: 'user_bookings'}  "> Bookings </RouterLink>
            </li>


            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout"> Logout </a>
            </li>

          </template>

        </ul>

      </div>
    </div>
  </nav>

</template> 

