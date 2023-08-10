<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
  <button class="logout" @click="logout">Logout</button>

  <!-- sort and search methods for venues -->

  <select v-model="sortM" style="display:flex;position:absolute;top:20%;left:3%">
    <option value="alpabetically">Alphabetical</option>
    <option value="Capacity">Capacity</option>
  </select>
  <input class="search" type="text" v-model="searchValue" placeholder="Search" style="position:relative;left:10%">
  <div class="venuesuser">
    <h1>Venues</h1>


    <!-- sort and search methods for shows -->
    <select v-model="sortS" style="width:7%;position:absolute;top:20%;left:70%">
      <option value="alphabetically">Alphabetical</option>
      <option value="Capacity">Capacity</option>
    </select>
    <select v-model="showsearchCategory" style="width:7%;position:absolute;top:20%;left:85%">
      <option value="Time">Time</option>
      <option value="Movie">Movie</option>
      <option value="Capacity">Current_Capacity</option>
      <option value="tags">Tags</option>
    </select>
    <input v-if="showsearchCategory == 'Time'" class="search" type="datetime-local" v-model="showsearchValue" 
      placeholder="Search">
    <input v-if="showsearchCategory != 'Time'" class="search" type="text" v-model="showsearchValue" placeholder="Search"
      style="display:flex;position:absolute;top:25%;left:75%">

    <!-- iterating through filtered venues -->
    <div class="venueuser" v-for="venue in filteredvenues" :key="venue.id">
      <img :src="venue.image" alt="image" style="width:10%;">
      <h2>{{ venue.name }}</h2>

      <!-- iterating through filterd shows -->
      <button @click="getshow(venue.id)">Show</button>
      <div class="showsuser" v-for="sho in filteredshows" :key="show.id" v-if="venue_id == venue.id">
        <img :src="sho.image" alt="image" style="width:50%;height:50%;">
        <h4>{{ sho.movie }}</h4>
        <p>{{ sho.description }}</p>
        <p>Date:{{ sho.date }}</p>
        <p>{{ sho.current_capacity }}</p>
        <p>{{ sho.rating }}</p>

        <div class="bookdet" v-if="show_id == sho.id">
          <p>Available Bookings:{{ sho.current_capacity }}</p>
          <p v-if="book['quantity'] > sho.current_capacity" style="color: red;">No of SEATS should be less than
            Available
            seats</p>
          <label>Number <input type="number" placeholder="select No of SEATS" v-model="book['quantity']" /></label><br>
          <label>Price <input :value="sho.price" readonly /></label><br>
          <p style="display: none;"> {{ book['total']=book['quantity'] * sho.price }}</p>
          <p style="display: none;"> {{ book['venue'] = venue.name }}</p>
          <label>Total Price:<input v-model="book['total']" v-if="book['quantity'] != NaN" readonly /></label><br>
          <button @click="bookshow(sho)" v-if="book['quantity'] < sho.current_capacity">Confirm</button>


        </div>


        <button @click="this.show_id = sho.id">Book</button>
        <!-- Booking Details for the user  -->
      </div>
    </div>
  </div>
  <div class="venuesuser">
    <h1>My Bookings</h1>
    <div class="venueuser" v-for="book in filteredbookings" :key="book.id">
      <div>
        <h2>{{ book.movie }}</h2>
      </div>
      <div class="showsuser">
        <h3>{{ book.venue }}</h3>
        <p>{{ book.date }}</p>
        <p>{{ book.quantity }}</p>
        <p>RS{{ book.total }}</p>
      </div>
      <input type="number" v-model="book['rating']" placeholder="Rate the movie" />
      <button @click="rateshow(book)">RATE</button>
    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {

  .about {
    display: flex;
  }


  .logout {
    position: absolute;
    top: 40px;
    right: 40px;
    margin: 10px;
    padding: 10px;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: #fff;
    font-size: 18px;
  }

  .venuesuser {
    display: grid;
    grid-template-rows: auto;
    justify-content: space-around;
    align-items: center;
    margin: 20px;
    padding: 20px;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: #fff;
    font-size: 18px;
    overflow-y: scroll;
    height: 600px;
  }

  .venueuser {
    display: flex;
    background-color: white !important;
    flex-direction: row;
    ;
    justify-content: space-around;
    align-items: center;
    margin: 20px;
    padding: 10px;
    padding-bottom: 20px;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: black;
    font-size: 14px;
  }

  .showsuser {
    justify-content: space-around;
    align-items: center;
    margin: 10px;
    padding: 10px;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: #fff;
    font-size: 18px;
    position: relative;
  }

  .bookdet {
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    margin: 10px;
    padding: 10px;
    overflow-y: scroll;
    border-radius: 5px;
    background-color: white;
    color: black;
    font-size: 18px;
  }

  input {
    background: #ecf0f1;
    border: #ccc 1px solid;
    border-bottom: #ccc 2px solid;
    padding: 8px;
    width: 250px;
    color: black;
    margin-top: 10px;
    margin-bottom: 10px;
    font-size: 1em;
    border-radius: 4px;
  }

  .search {
    background: #ecf0f1;
    border: #ccc 1px solid;
    border-bottom: #ccc 2px solid;
    padding: 5px;
    width: 200px;
    color: black;
    margin-top: 1px;
    margin-bottom: 1px;
    font-size: 1em;
    border-radius: 4px;
    display: flex;
    position: relative;
    top: 60px;
    left: 150px;
  }

  button {
    background: #3498db;
    width: 125px;
    padding-top: 5px;
    padding-bottom: 5px;
    color: white;
    border-radius: 4px;
    border: #3498db 1px solid;

    margin-top: 20px;
    margin-bottom: 20px;
    float: left;
    margin-left: 16px;
    font-weight: 800;
    font-size: 0.8em;
    position: relative;
    top: 10px;

  }

  button:hover {
    background: #2CC06B;
  }

  select {
    outline: 10px red;
    border: 2px;
    border-radius: 4px;
    box-shadow: none;
    padding: 0 1em;
    color: white;
    background-color: #3498db;
    cursor: pointer;
    height: 25px;
  }

  /* Ratings widget */


}
</style>

<script>
import config from '../config'
import { reactive } from 'vue';
export default {
  data() {
    return {
      base_url: config.base_url,
      venue: [],
      show: [],
      venue_id: 0,
      show_id: null,
      book: { total: 0 },
      bookingslist: [],
      sortM: 'alphabetically',
      searchValue: '',
      showsearchValue: null,
      showsearchCategory: '',
      sortS: 'alphabetically',
    }
  },
  computed: {

    filteredvenues() {
      let tempvenue = this.venue

      // Process search input
      if (this.searchValue != '' && this.searchValue) {
        tempvenue = tempvenue.filter((item) => {
          return item.name
            .toUpperCase()
            .includes(this.searchValue.toUpperCase())
        })
      }

      // Filter out by cooking time
      // if (this.maxCookingTime)
      // tempvenue = tempvenue.filter((item) => {
      //   return (item.cookingTime <= this.maxCookingTime)
      // })

      // Sort by alphabetical order
      tempvenue = tempvenue.sort((a, b) => {
        if (this.sortM == 'alphabetically') {
          let fa = a.name.toLowerCase(), fb = b.name.toLowerCase()

          if (fa < fb) {
            return -1
          }
          if (fa > fb) {
            return 1
          }
          return 0

          // Sort by capacity
        } else if (this.sortM == 'Capacity') {
          return a.capacity - b.capacity
        }
      })

      // Show sorted array in descending or ascending order
      // if (!this.ascending) {
      //     tempvenue.reverse()
      // }

      return tempvenue
    },


    filteredshows() {
      let tempshow = this.show

      // Process search input

      if (this.showsearchCategory == 'Movie') {
        if (this.showsearchValue != '' && this.showsearchValue) {
          console.log("capacity", this.showsearchValue)
          tempshow = tempshow.filter((item) => {
            return item.movie
              .toUpperCase()
              .includes(this.showsearchValue.toUpperCase())
          })
        }
      }
      else if (this.showsearchCategory == 'Capacity') {
        if (this.showsearchValue != '' && this.showsearchValue) {
          tempshow = tempshow.filter((item) => {
            return (item.current_capacity <= Number(this.showsearchValue))
          })
        }
      }
      else if (this.showsearchCategory == 'tags') {
        if (this.showsearchValue != '' && this.showsearchValue) {
          tempshow = tempshow.filter((item) => {
            return item.tags
              .toUpperCase()
              .includes(this.showsearchValue.toUpperCase())
          })
        }
      }
      else if (this.showsearchCategory == 'Time') {
        if (this.showsearchValue != '' && this.showsearchValue) { 
          tempshow = tempshow.filter((item) => {
            console.log("time2",Date.parse(item.date.slice(0,25)), Date.parse(this.showsearchValue))
            return (Date.parse(item.date.slice(0,25)) >= Date.parse(this.showsearchValue))
          })
        }

      }

      // Filter out by cooking time
      // if (this.maxCookingTime)
      // tempshow = tempshow.filter((item) => {
      //   return (item.cookingTime <= this.maxCookingTime)
      // })

      // Sort by alphabetical order
      tempshow = tempshow.sort((a, b) => {
        if (this.sortS == 'alphabetically') {
          let fa = a.movie.toLowerCase(), fb = b.movie.toLowerCase()
          if (fa < fb) {
            return -1
          }
          if (fa > fb) {
            return 1
          }
          return 0

          // Sort by capacity
        } else if (this.sortS == 'Capacity') {
          return a.current_capacity - b.current_capacity
        }
      })

      // Show sorted array in descending or ascending order
      // if (!this.ascending) {
      //     tempshow.reverse()
      // }

      return tempshow
    },

    filteredbookings() {

      let tempbookings = this.bookingslist

      // Process search input
      // if (this.searchValue != '' && this.searchValue) {
      //   tempbookings = tempbookings.filter((item) => {
      //     return item.name
      //       .toUpperCase()
      //       .includes(this.searchValue.toUpperCase())
      //   })
      // }

      // Filter out by cooking time
      // if (this.maxCookingTime)
      // tempbookings = tempbookings.filter((item) => {
      //   return (item.cookingTime <= this.maxCookingTime)
      // })

      // Sort by alphabetical order
      // tempbookings = tempbookings.sort((a, b) => {
      //   if (this.sortM == 'alphabetically') {
      //     let fa = a.name.toLowerCase(), fb = b.name.toLowerCase()

      //     if (fa < fb) {
      //       return -1
      //     }
      //     if (fa > fb) {
      //       return 1
      //     }
      //     return 0

      //     // Sort by capacity
      //   } else if (this.sortM == 'Capacity') {
      //     return a.capacity - b.capacity
      //   }
      // })

      // Show sorted array in descending or ascending order
      // if (!this.ascending) {
      //     tempbookings.reverse()
      // }

      return tempbookings



    }




  },

  mounted() {
    this.bookingslist = []
    if (!this.$store.getters.isAuthenticated) {
      this.$router.push('/login')
    }
    this.getvenue()
    this.getbookings()
  },
  methods: {

    async getvenue() {
      this.venue = await this.$store.dispatch('getvenues')
      console.log("venues", this.venue)
    },

    logout() {
      this.$store.dispatch('logout')
      this.$router.push('/login')
    },

    async getshow(id) {
      this.venue_id = id
      console.log("id", id)
      this.show = await this.$store.dispatch('getshows', [id, 0])
      console.log("shows", this.show)
    },

    async bookshow(show) {
      this.book['show_id'] = show.id
      this.book['date'] = show.date
      this.book['movie'] = show.movie
      console.log("book", this.book)
      await this.$store.dispatch('book', this.book)
      console.log("booked", this.$store.getters.getbookings)
      this.bookingslist = this.$store.getters.getbookings
      this.getshow(this.venue_id)
    },

    async rateshow(book) {
      if (book.rating > 0 && book.rating < 6) {
        await this.$store.dispatch('rateshow', book)
        console.log("rated", this.$store.getters.getbookings)
      }
      else {
        alert("Please select a show and rate it")
      }


    },
    
    async getbookings() {
      this.bookingslist = await this.$store.dispatch('getbookings')
      console.log("bookings", this.bookingslist)
    },
  }
}
</script>