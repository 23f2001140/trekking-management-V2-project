<script setup>
import {ref , onMounted, computed} from 'vue'
import {RouterLink} from 'vue-router'
import router from '../../router'
import { useFlash } from '@/stores/flash'
import { useAuth } from '@/stores/auth'

const auth = useAuth()
const flash = useFlash()

const fullname = computed(() => auth.user? auth.user.fullname : '')
const treks = ref('')
const users = ref('')
const staff = ref('')
const bookings = ref('')

const chart_labels = ref([])
const chart_count = ref([])
const chartCanvas = ref(null)
let myChart = null

const revenue = ref([])
const revenueCanvas = ref(null)
let myRevenueChart = null

async function getAdminDashboard() {
  const res = await fetch('http://127.0.0.1:5000/api/admin', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
  })
  const data = await res.json()
  if (res.ok) {
    treks.value = data.treks
    users.value = data.user_count
    staff.value = data.staff_count
    bookings.value = data.bookings

    chart_labels.value = data.chart_labels
    chart_count.value = data.chart_count
    revenue.value = data.revenue
    renderChart()
    renderRevenueChart()
  }
  else {
    flash.showFlash(data.message, 'danger')
    auth.logout()
    router.push('/')
  }
}

function renderChart() {
  if (myChart) {
    myChart.destroy()
  }

  myChart = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels: chart_labels.value,
      datasets: [{
        label: 'Treks Popularity',
        data: chart_count.value,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          max: 5,
          ticks: {
            stepSize: 1
          },
          title: {
            display: true,
            text: 'Total Bookings',
            font: {
              size: 16,
              weight: 'bold'
            }
          }
        },
        x: {
          title: {
            display: true,
            text: 'Treks',
            font: {
              size: 16,
              weight: 'bold'
            }
          }
        }
      }
    }
  })
}

function renderRevenueChart() {
  if (myRevenueChart) {
    myRevenueChart.destroy()
  }

  myRevenueChart = new Chart(revenueCanvas.value, {
    type: 'bar',
    data: {
      labels: chart_labels.value,
      datasets: [{
        label: 'Revenue (₹)',
        data: revenue.value,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Revenue (₹)',
            font: {
              size: 16,
              weight: 'bold'
            }
          }
        },
        x: {
          title: {
            display: true,
            text: 'Treks',
            font: {
              size: 16,
              weight: 'bold'
            }
          }
        }
      }
    }
  })
}

onMounted(async () => {
 await getAdminDashboard()
})

const semail = ref('')
const sfullname = ref('')
const sphone = ref('')
const spassword = ref('')
const scpassword = ref('')
const smessage = ref('')
const spmessage = ref('')

const validateEmail = () => {
    if (semail.value == '') {
        smessage.value = ''
    }
    else if (!semail.value.includes('@') || !semail.value.includes('.')) {
        smessage.value = 'Please enter a valid email address'
    }
    else {
        smessage.value = ''
    }
}

const validatePassword = () => {
  if (spassword.value == '') {
      spmessage.value = ''
  }
  else if (spassword.value.length < 6) {
      spmessage.value = 'Password must be at least 6 characters long'
  }
  else {
      spmessage.value = ''
  }
}

async function AddStaff() {
  if (spassword.value != scpassword.value) {
    flash.showFlash('Passwords do not match', 'danger')
    return
  }
  const res= await fetch('http://127.0.0.1:5000/api/admin/staff', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify({
      email: semail.value,
      password: spassword.value,
      cpassword: scpassword.value,
      fullname: sfullname.value,
      phone: sphone.value,
    }),
  })
  const data = await res.json()
  if (res.ok) {
    flash.showFlash(data.message, 'success')
    semail.value = ''
    spassword.value = ''
    scpassword.value = ''
    sfullname.value = ''
    sphone.value = ''
    const modalEl = document.getElementById('addStaffModal')
    const modalInstance = window.bootstrap.Modal.getInstance(modalEl) || new Modal(modalEl)
    modalInstance.hide()
    await getAdminDashboard()
  }
  else {
    flash.showFlash(data.message, 'danger')
  }
}
</script>

<template>
<div>
<h1><i class="fa-solid fa-gauge-high"></i> Dashboard
<RouterLink :to="{ name: 'admin_add_trek' }" class="btn btn-success mt-2 float-end ms-2"><i class="fa-solid fa-plus"></i> New Trek </RouterLink>
<button class="btn btn-success mt-2 float-end ms-2" data-bs-toggle="modal" data-bs-target="#addStaffModal"> <i class="fa-solid fa-user-plus"></i> Add Staff </button></h1>
<p class="text-muted">Welcome, {{fullname }} !</p>
<div class="modal fade" id="addStaffModal" tabindex="-1" aria-labelledby="addStaffModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-md">
        <div class="modal-content">
            <div class="modal-header text-white" style="background-color: #2c7a4b;">
                <h1 class="modal-title fs-5" id="addStaffModalLabel"> <i class="fa-solid fa-user-plus"></i> Add New Staff </h1>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="AddStaff">
                  <div class="mb-3">
                    <label for="email" class="form-label">Staff Email:</label>
                    <input v-model="semail" type="email" id="email" name="email" class="form-control" @blur="validateEmail" required>
                  </div>
                  <div class="mb-3">
                      <p class="text-danger" v-if="smessage">{{ smessage }}</p>
                  </div>
                  <div class="mb-3">
                    <label for="fullname" class="form-label">Full Name:</label>
                    <input v-model="sfullname" type="text" id="fullname" name="fullname" class="form-control" required>
                  </div>
                  <div class="mb-3">
                    <label for="phone" class="form-label">Phone Number:</label>
                    <input v-model="sphone" type="text" id="phone" name="phone" class="form-control" required>
                  </div>
                  <div class="mb-3">
                    <label for="password" class="form-label">Password:</label>
                    <input v-model="spassword" id="password" name="password" type="password" class="form-control" @input="validatePassword" required>
                  </div>
                  <div class="mb-3">
                      <p class="text-danger" v-if="spmessage">{{ spmessage }}</p>
                  </div>
                  <div class="mb-3">
                    <label for="cpassword" class="form-label">Confirm Password:</label>
                    <input v-model="scpassword" id="cpassword" name="cpassword" type="password" class="form-control" required>
                  </div>
                  <br>
                  <div class="modal-footer justify-content-center">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"> Cancel </button>
                    <button class="btn btn-success" type="submit"> Add Staff </button>
                  </div>
              </form>
            </div>
        </div>
    </div>
</div>
<div class="row mb-4 mt-4 d-flex justify-content-center align-items-center">
  <div class="col-sm-3">
    <div class="card text-bg-dark mb-3">
      <RouterLink :to="{ name: 'admin_treks' }" class="text-decoration-none text-white">
        <div class="card-body">
          <h5 class="card-title fa-solid fa-map"></h5>
          <h2 class="card-text">{{treks}}</h2>
          <h5 class="card-title"><strong>Total Treks</strong></h5>
        </div>
       </RouterLink>
    </div>
  </div>
  <div class="col-sm-3">
    <div class="card text-bg-success mb-3">
      <RouterLink :to="{ name: 'admin_users' }" class="text-decoration-none text-white">
        <div class="card-body">
          <h5 class="card-title fa-solid fa-users"></h5>
          <h2 class="card-text"><strong>{{ users }}</strong></h2>
          <h5 class="card-title"><strong>Registered Users</strong></h5>
        </div>
    </RouterLink>
    </div>
  </div>
  <div class="col-sm-3">
    <div class="card text-bg-info mb-3">
      <RouterLink :to="{ name: 'admin_staff' }" class="text-decoration-none text-dark">
        <div class="card-body">
          <h5 class="card-title fa-solid fa-users-gear"></h5>
          <h2 class="card-text"><strong>{{ staff }}</strong></h2>
          <h5 class="card-title"><strong>Trek Staff</strong></h5>
        </div>
    </RouterLink>
    </div>
  </div>
  <div class="col-sm-3">
    <div class="card text-bg-warning mb-3">
      <RouterLink :to="{ name: 'admin_bookings' }" class="text-decoration-none text-dark">
        <div class="card-body">
          <h5 class="card-title fa-solid fa-list-check"> </h5>
          <h2 class="card-text"><strong>{{ bookings }}</strong></h2>
          <h5 class="card-title"><strong>Total Bookings</strong></h5>
        </div>
    </RouterLink>
    </div>
  </div>
</div>
<div class="mt-4"  style="width: 70%; margin: 10px auto;">
    <h3>Treks Popularity <i class="fa-solid fa-chart-column"></i></h3>
    <canvas ref="chartCanvas"></canvas>
</div>
<div class="mt-4"  style="width: 70%; margin: 10px auto;">
    <h3>Revenue <i class="fa-solid fa-indian-rupee-sign"></i></h3>
    <canvas ref="revenueCanvas"></canvas>
</div>
</div>
</template>