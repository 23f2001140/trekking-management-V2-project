<script setup>
import { computed } from 'vue'
import { useFlash } from '@/stores/flash'

const flash = useFlash()

const { trek } = defineProps({
  trek: {
    type: Object,
    required: true,
  },
  booking_status: {
    type: String
  },
})

const DifficultyColor = computed(() => {
  if (trek.difficulty === 'Easy') {
    return 'bg-success'
  } else if (trek.difficulty === 'Moderate') {
    return 'bg-warning'
  } else if (trek.difficulty === 'Hard') {
    return 'bg-danger'
  }
})

const StatusColor = computed(() => {
  if (trek.status === 'Open') {
    return 'bg-success'
  } else if (trek.status === 'Closed') {
    return 'bg-danger'
  }
  else if (trek.status === 'Pending') {
    return 'bg-warning'
  } else if (trek.status === 'Approved') {
    return 'bg-info'
  } else if (trek.status === 'Completed') {
    return 'bg-secondary'
  }
})

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}


const emit = defineEmits(['book-trek'])

function bookTrek() {
  emit('book-trek', trek.id)
}


  const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
  const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

</script>

<template>
       <div class="card mb-3 col-md-12 shadow-sm trek-card">
            <div class="row g-1">
                <div class="col-md-4 image-wrapper">
                <img :src="trek.image_url" class="img-fluid rounded-start h-100 trek-image" :alt="trek.name" style="object-fit: cover;">
                </div>
                <div class="col-md-8 d-flex flex-column justify-content-between">
                    <div class="card-body ">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h5 class="card-title"><strong>{{ trek.name }}</strong></h5>
                                <p class="card-text"><strong> <i class="fa-solid fa-location-dot"></i> Location: </strong>{{ trek.location }}</p>
                                <p class="card-text"><strong><i class="fa-solid fa-clock"></i> Duration: </strong>{{ trek.duration }} days</p>
                                <p class="card-text"><strong><i class="fa-solid fa-calendar-days"></i> Start Date: </strong>{{ formatDate(trek.start_date) }}</p>
                                <p class="card-text"><strong><i class="fa-solid fa-calendar-days"></i> End Date: </strong>{{ formatDate(trek.end_date) }}</p>
                            </div>
                            <div>
                            <p class="card-text"><strong> <i class="fa-solid fa-ticket"></i> Slots Available: </strong>{{ trek.available_slots }} slots</p>
                            <h5 class="card-text badge" :class="StatusColor"> <strong>Status: </strong>{{ trek.status === 'Approved' ? 'Upcoming' : trek.status }}</h5>
                            <p class="card-text"><strong> <i class="fa-solid fa-user-tie"></i> Assigned Staff: </strong>{{ trek.assigned_staff.fullname }}</p>
                            <h5 class="card-text mb-3">
                                <span class="badge" :class="DifficultyColor"><strong>Difficulty: </strong>{{ trek.difficulty }}</span>
                            </h5>
                            <p class="card-text"><strong> <i class="fa-solid fa-indian-rupee-sign"></i> Price:</strong>{{ trek.price }}</p>
                            </div>
                            <div v-if="booking_status">
                                <button class="btn btn-secondary" disabled>{{ booking_status }}</button>
                            </div>
                            <div v-else-if="trek.status === 'Open' && trek.available_slots > 0">
                                <button class="btn btn-primary" @click.prevent="bookTrek">Book Now</button>
                            </div>
                            <div v-else-if="trek.status === 'Open' && trek.available_slots === 0">
                                <button class="btn btn-secondary" data-bs-container="body" data-bs-toggle="popover" data-bs-placement="bottom" data-bs-content="This trek is currently fully booked. Availability may open if a booking is cancelled.">Fully Booked</button>
                            </div>
                            <div v-else-if="trek.status === 'Approved'">
                                <button class="btn btn-secondary" disabled>Upcoming</button>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer ">
                         <p class="card-text "><strong><i class="fa-solid fa-pen-to-square"></i> Description:</strong> {{ trek.description ? trek.description : 'No description provided' }}</p>
                    </div>
                </div>
            </div>
        </div>
</template>

<style scoped>
.trek-card {
    border-radius: 14px;
    transition: all 0.3s ease;
}

.trek-card:hover {
    transform: translateY(-6px);
    background-color: #f6fcf8;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
}

.image-wrapper {
    overflow: hidden;
    border-radius: 14px 0 0 14px;
}

.trek-image {
    transition: transform 0.35s ease;
}

.trek-card:hover .trek-image {
    transform: scale(1.06);
}

.btn {
    transition: transform 0.2s ease;
}

.btn:hover {
    transform: scale(1.04);
}
</style>