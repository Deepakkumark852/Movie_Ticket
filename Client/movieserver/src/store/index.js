import { createStore } from 'vuex'
import { isValidJwt, EventBus, uservalid, adminvalid } from '../utils'
import { authenticate, getuser, getadmin, updateadmin, updateuser,deleteuser,deleteadmin, getvenues, getshows, book, adminauthenticate, addvenue, freeslots, addshow, register, adminregister, getvenuesbyadmin, ableshow, delshow, delvenue, editshow, rateshow, editvenue, generatecsv,getchart,getbookings } from '../api'


export default createStore({

    state: {
        jwt: window.localStorage.getItem('jwt'),
        bookings: window.localStorage.getItem('bookings')
    },

    mutations: {
        setjwt(state, jt) {
            state.jwt = jt
            state.bookings = ""
            window.localStorage.setItem('jwt', jt)
            console.log('jwt set done', state.jwt)
            window.localStorage.setItem('bookings', [])
        },
        setbooking(state, showid) {
            console.log('showid', showid)
            if (state.bookings == "" || state.bookings == null) {
                state.bookings = [showid]
            }
            else {
                state.bookings = JSON.parse(state.bookings)
                state.bookings.push(showid)
            }
            window.localStorage.setItem('bookings', JSON.stringify(state.bookings))
            state.bookings = JSON.stringify(state.bookings)
        }
    },

    actions: {

        // ................................................ USER and ADMIN .......................................................

        async getuser(context,) {
            const response = await getuser(context.state.jwt)
            // console.log('response', response.data)
            return response.data
        },

        async getadmin(context,) {
            const response = await getadmin(context.state.jwt)
            return response.data
        },

        login(context, userData) {
            console.log('login action triggered', userData)
            return authenticate(userData)
                .then((response) => {
                    // console.log('response', response.data['token'])
                    context.commit('setjwt', response.data['token'])
                }
                )
                .catch(error => {
                    console.log('Error Authenticating: ', error)
                    EventBus.emit('failedAuthentication', error)
                })
        },

        register(context, userData) {
            return register(userData)
                .catch(error => {
                    console.log('Error Registering: ', error)
                    EventBus.emit('failedRegister', error)
                })
        },

        adminregister(context, userData) {
            return adminregister(userData)
                .catch(error => {
                    console.log('Error Registering: ', error)
                    EventBus.emit('failedRegister', error)
                })
        },

        logout(context) {
            context.commit('setjwt', '')
        },

        adminlogin(context, userData) {
            console.log('login action triggered', userData)
            return adminauthenticate(userData)
                .then((response) => {
                    // console.log('response', response.data['token'])
                    context.commit('setjwt', response.data['token'])
                }
                )
                .catch(error => {
                    console.log('Error Authenticating: ', error)
                    EventBus.emit('failedAuthentication', error)
                })
        },

        updateuser(context, userdata) {
            return updateuser(userdata, context.state.jwt)
        },

        updateadmin(context, admindata) {
            return updateadmin(admindata, context.state.jwt)
        },

        deleteuser(context) {
            return deleteuser(context.state.jwt)
        },

        deletadmin(context) {
            return deleteadmin(context.state.jwt)
        },

        async generatecsv(context) {
            var jt = context.state.jwt
            const response = await generatecsv(jt)
            return response.data[0]
        },

        // ...........................................................VENUE...............................................................


        async getvenues(context) {
            var venues = []
            var jt = context.state.jwt
            const response = await getvenues(jt)
            venues = response.data['0']['venue']
            console.log("venues", response.data)
            return venues
        },

        async getvenuesbyadmin(context) {
            var venues = []
            var jt = context.state.jwt
            const response = await getvenuesbyadmin(jt)
            venues = response.data['0']['venue']
            console.log("venues", response.data)
            return venues
        },

        async addvenue(context, venue) {
            return addvenue(venue, context.state.jwt)
        },

        async editvenue(context, venued) {
            return editvenue(venued, context.state.jwt)
        },

        async delvenue(context, venued) {
            return delvenue(venued, context.state.jwt)
        },

        // ...........................................................SHOW...............................................................


        async freeslots(context, showd) {
            var slots = []
            const response = await freeslots(showd, context.state.jwt)
            slots = response.data['0']['free_slots']
            return slots
        },

        async getshows(context, venueid) {
            console.log("venueid", venueid)
            var shows = []
            const response = await getshows(venueid, context.state.jwt)
            shows = response.data['0']['show']
            console.log("shows", shows)
            return shows
        },

        async addshow(context, showd) {
            return addshow(showd, context.state.jwt).then((response) => {
                if (response.data[1] != 200) {
                    EventBus.emit('failedAddShow', response.data[0]['message'])
                }
            })
        },

        async ableshow(context, showd) {
            return ableshow(showd, context.state.jwt)
        },

        async editshow(context, showd) {
            return editshow(showd, context.state.jwt)
        },

        async delshow(context, showd) {
            return delshow(showd, context.state.jwt)
        },

        // ...........................................................BOOKING...............................................................

        async book(context, showid) {
            return book(showid, context.state.jwt).then((response) => {
                context.commit('setbooking', showid)
            }
            )
        },

        async rateshow(context, showid) {
            return rateshow(showid, context.state.jwt)
        },

        async getchart(context, showid) {
            let chart = []
            const response = await getchart(showid, context.state.jwt)
            chart = response.data['0']['booking']
            console.log("chart", chart)
            return chart
        },

        async getbookings(context) {
            var bookings = []
            const response = await getbookings(context.state.jwt)
            bookings = response.data['0']['booking']
            console.log("bookings", bookings)

            return bookings
        }

    },

    getters: {

        isAuthenticated(state) {
            console.log("Tttttt", uservalid(state.jwt))
            return (isValidJwt(state.jwt) && uservalid(state.jwt))

        },

        isadminAuthenticated(state) {
            return (isValidJwt(state.jwt) && adminvalid(state.jwt))

        },

        getjwt(state) {
            return state.jwt
        },

        getbookings(state) {
            if (state.bookings == "" || state.bookings == null) {
                return []
            }
            console.log('state.bookings', state.bookings, typeof (state.bookings))
            let book = JSON.parse(state.bookings)
            return JSON.parse(state.bookings)
        },

    }
})