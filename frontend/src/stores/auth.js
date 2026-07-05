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
            const stored_user = localStorage.getItem('user')
            const token = localStorage.getItem('token')

            if (!stored_user || !token) {
               this.user = null
               this.token = null
               return
            }
            try {
                this.user = JSON.parse(stored_user)
                this.token = token
            } catch (e) {
                this.logout()
            }
        },
    },
})