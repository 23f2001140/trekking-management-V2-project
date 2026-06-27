import { defineStore } from 'pinia'

export const useAuth = defineStore('auth', {
    state: () => ({
        user: null,
        token: null
    }),

    getters: {
        isLoggedIn (state) {
            return state.token !== null
        },
        
        role (state) {
            return state.user?.role
        }
    },
    actions: {
        login(user, token) {
        this.user = user
        this.token = token

        localStorage.setItem('user', JSON.stringify(user))
        localStorage.setItem('token', token)
        },

        logout() {
        this.user = null
        this.token = null
        localStorage.removeItem('user')
        localStorage.removeItem('token')
        },

        restore() {
            const user = JSON.parse(localStorage.getItem('user'))
            const token = localStorage.getItem('token')

            if (user && token) {
                this.user = user
                this.token = token
            }
        },
    },
})