


<template>
  <button class="logout" @click="logout">Logout</button>
  <h1 style="position: relative;top:100px; left:5% ;font-size: 48px; color: azure;">venues</h1>
  <div class="venues">

    <!-- ..................................Iterating Through the venues .....................................-->
    <div class="venue" v-for="ven in venue">
      <img :src=ven.image style="width: 50%;">
      <h1 style="font-size:x-large;">{{ ven.name }}</h1>
      <p style="display: fixed !important; right: 5000px !important;">-{{ ven.description }}</p>
      <p>Capacity: {{ ven.capacity }}</p>
      {{ ven.location }}
      <button @click=" getshow(ven.id)">Show</button>

      <!-- ..................................Iterating Through the shows....................................... -->
      <div id="shows" class="shows" v-for="sho in show" v-if="ven.id == venue_id">
        <div>
          <img :src=sho.image style="width: 50%; height: 50%;">
        </div>
        <div>
          <p>{{ sho.movie }}</p><br>
          <p> Rs {{ sho.current_capacity }}</p>
        </div>
        <button @click="editshows(sho)">Edit</button>
        <p style="display: none;">{{ addshow['able']=sho.enabled }}</p><br>
        <button @click="ableshow(sho.id, sho.enabled)">{{ Enabled }}</button>
        <button @click="delshow(sho.id)">Delete</button>
      </div>
      <button @click="() => { addshow['display'] = !addshow['display']; venue_id = ven.id }">Add Show</button>

      <!-- ...........................................ADD Show to the Venue................................. -->

      <div v-show="addshow['display']" v-if="ven.id == venue_id">
        <label>Movie <input type="text" v-model="addshow['movie']" /></label><br>
        <label>Duration <input type="text" v-model="addshow['duration']" placeholder="HH:MM:SS" /></label><br>
        <label>Date <input type="date" v-model="addshow['date']" /></label><br>
        <button @click="freeslots()">Get Free Slots</button><br>
        <div v-if="freeslot.length>0 && Date.parse(freeslot[0][0])>= new Date()"><br><br>
          <label>Time <select v-model="addshow['slot']">
              <option v-for="slot in freeslot" :key="slot.id" :value="slot">{{ slot }}</option>
              <option :value="-1">Manual</option>
              <option v-if="freeslot.length == 0">No Free Slots</option>
            </select></label><br>
          <label v-if="addshow['slot'] == -1">Time <input type="time" v-model="addshow['slot']" /></label><br>
          <label>Price <input type="number" v-model="addshow['price']" /></label><br>
          <label>Image<input type="file" @change="onShowChange" /></label><br>
          <label>Tags<input type="text" v-model="addshow['tags']" /></label><br>
          <label>Description<input type="text" v-model="addshow['description']" /></label><br>
          <button @click="newshow(ven.id)">Confirm</button>
        </div>
      </div>
      <!-- ...................................................END Show................................. -->
      <div>
        <button @click="editvenues(ven)">EDIT</button>
        <button @click="delvenue(ven.id)">DELETE</button>
      </div>
    </div>
    <button @click="() => { addvenue['display'] = !addvenue['display']; }">add</button>

    <!-- .....................................................ADD Venue To the Admin.................................. -->
    <div v-show="addvenue['display']" style="align-items: center; align-content: center; text-align:center;">
      <label>Name: <input type="text" v-model="addvenue['name']" style="position: relative; left: 20px;" /></label><br>
      <label>Location <input type="text" v-model="addvenue['location']"
          style="position: relative; left: 13px;" /></label><br>
      <label>Capacity<input type="number" v-model="addvenue['capacity']"
          style="position: relative; left: 15px;" /></label><br>
      <label>Description<input type="text" v-model="addvenue['description']"
          style="position: relative; left:5px;" /></label><br>
      <label>Image<input type="file" @change="onFileChange" style="position: relative; left: 28px;" /></label><br>
      <button @click="newvenue()">Confirm</button>
    </div>
  </div>
  <!--........................................................END Venue.................................. ............-->

  <!-- .....................................................EDIT Venue.................................. ............-->
  <div class="editmenu" v-show="editvenue['display']">
    <label>Name: <input type="text" v-model="editvenue['name']" style="position: relative; left: 20px;" /></label><br>
    <label>Location <input type="text" v-model="editvenue['location']"
        style="position: relative; left: 13px;" /></label><br>
    <label>Capacity<input type="number" v-model="editvenue['capacity']"
        style="position: relative; left: 15px;" /></label><br>
    <label>Description<input type="text" v-model="editvenue['description']"
        style="position: relative; left:5px;" /></label><br>
    <label>Image<input type="file" @change="onFileChange" style="position: relative; left: 28px;" /></label><br>
    <button @click="editvenuee()">Confirm</button>
  </div>

  <!-- .....................................................EDIT Show.................................. ............-->

  <div class="editmenu" v-show="editshow['display']">
    <h1>Edit Menu</h1>
    <button style="position: relative; top: 50%; left: 50%;transform: translate(100%, -350%);"
      @click="() => editshow['display'] = !editshow['display']">X</button>
    <label>Movie <input type="text" v-model="editshow['movie']" /></label><br>
    <label>Duration <input type="text" v-model="editshow['duration']" /></label><br>
    <label style="position: relative; left: 30%;">Date <input type="date" v-model="editshow['date']" /></label><br>
    <button @click="editfreeslots()">Get Free Slots</button><br>
    <div v-if="freeslot.length > 0 && Date.parse(editshow['date']) > new Date()">
      <label>Time <select v-model="editshow['slot']">
          <option v-for="slot in freeslot" :key="slot.id" :value="slot">{{ slot }}</option>
          <option :value="-1">Manual</option>
          <option v-if="freeslot.length == 0">No Free Slots</option>
        </select></label>
      <label v-if="addshow['slot'] == -1">Time <input type="time" v-model="editshow['slot']" /></label>
    </div><br>
    <label>Price <input type="number" v-model="editshow['price']" /></label><br>
    <label style="position: relative; left: 20%;">Image <input type="file" @change="onShowChange" /></label><br>
    <label style="position: relative; left: 20%;">Tags <input type="text" v-model="editshow['tags']" /></label><br>
    <label style="position: relative; left: 20%;">Description <input type="text"
        v-model="editshow['description']" /></label><br>
    <button @click="edit()">Confirm</button>
  </div>
  <select v-model="chartvenue">
    <option v-for="ven in venue" :key="ven.id" :value="ven.id">{{ ven.name }}</option>
  </select>
    <button @click="getshowforchart()">Get Shows</button>
  <select v-if="chartvenue != -1" v-model="chartshow" @change="getchart()">
    <option v-for="sho in show" :key="sho.id" :value="sho.id">{{ sho.movie }}</option>
  </select><br>
  <br><br><br>
  
  <div class="charts" v-if="chartshow != -1">
    <Responsive class="w-full">
    <template #main="{ width }">
      <Chart
        direction="circular"
        :size="{ width, height: 400 }"
        :data="charts"
        :margin="{
          left: Math.round((width - 360)/2),
          top: 20,
          right: 0,
          bottom: 20
        }"
        :config="{ controlHover: false }"
        >
        <template #layers>
          <Pie
            :dataKeys="['movie','rating']"
            :pie-style="{ innerRadius: 100, padAngle: 0.05 }" />
        </template>
        <template #widgets>
          <Tooltip
          :config="{ showTotal: true }"
            hideLine
          />
        </template>
      </Chart>
    </template>
  </Responsive>

  </div>
  <!-- ..................................................Generate CSV ...................................... -->
  <button @click="generatecsv()">Report</button>
</template>

<script>
import axios from 'axios';
import { addvenue } from '../api';
import config from '../config';
import {ref, toRaw} from 'vue';
import { Chart, Responsive, Pie, Tooltip } from 'vue3-charts'
export default {
  components: { Chart, Responsive, Pie, Tooltip },
  data() {
    return {
      base_url: config.base_url,
      venue: [],
      show: [],
      venue_id: null,
      show_id: null,
      book: { total: 0 },
      bookingslist: [],
      addvenue: {
        name: "",
        location: "",
        capacity: "",
        description: "",
        image: null,
        display: false,
      },
      addshow: {
        movie: "",
        duration: "",
        date: "",
        slot: "",
        price: "",
        tags: "",
        description: "",
        able: true,
        image: null,
      },
      freeslot: [],
      abled: false,
      editshow: { display: false },
      editvenue: { display: false },
      charts:[],
      chartdisplay:false,
      chartvenue: null,
      chartshow: null,
     plByMonth: [ ]
    }
  },
  computed: {
    Enabled() {
      console.log("this is abled", this.abled)
      if (this.addshow['able']) {
        return "Disable"
      }
      else {
        return "Enable"
      }
    },

  },

  mounted() {
    this.bookingslist = []
    console.log("this is admin", this.$store.getters.isadminAuthenticated)
    if (!this.$store.getters.isadminAuthenticated) {
      this.$router.push('/login')
    }
    this.getvenue()

    // this.bookingslist=this.$store.getters.getbookings
    // console.log("bookings123",this.bookingslist[1])
  },

  methods: {



    logout() {
      this.$store.dispatch('logout')
      this.$router.push('/login')
    },

    onFileChange(e) {
      var file = e.target.files[0];
      var read = new FileReader();
      read.readAsDataURL(file);
      read.onloadend = () => {
        file = read.result;
        this.addvenue.image = file;
      }
    },

    onShowChange(e) {
      console.log("this is file", file);
      var file = e.target.files[0];
      var read = new FileReader();
      read.readAsDataURL(file)
      read.onloadend = () => {
        file = read.result;

        this.addshow.image = file;
      }
    },

    // ............................................... Venue  Details ........................................................

    async getvenue() {
      this.venue = await this.$store.dispatch('getvenuesbyadmin')
      console.log("venues", this.venue)
    },

    async newvenue() {
      console.log("this is addvenue", this.addvenue)
      for (const [key, value] of Object.entries(this.addvenue)) {
        if (value == "") {
          alert("Please fill all the fields")
          return
        }

      }
      this.$store.dispatch('addvenue', this.addvenue)
      this.getvenue()
      this.addvenue = {}
    },

    async editvenues(venue) {
      this.editvenue = venue
      console.log("this is editvenue", this.editvenue)
      this.editvenue['display'] = true
    },

    async editvenuee() {
      console.log("this is editvenue", this.editvenue)
      this.$store.dispatch('editvenue', this.editvenue)
      this.editvenue['display'] = false
    },

    async delvenue(id) {
      console.log("this is id", id)
      await this.$store.dispatch('delvenue', id)
      this.getvenue()
    },

    // ...................................................... Show Details.............................................................


    async getshow(id) {
      this.venue_id = id
      console.log("Tthis is id", id)
      this.show = await this.$store.dispatch('getshows', [id, 1])
    },

    async ableshow(id, enabled) {
      console.log("this is id", id)
      this.addshow['able'] = enabled
      if (this.addshow['able'] == "Enable") {
        this.addshow['able'] = "Disable"
      }
      else {
        this.addshow['able'] = "Enable"
      }
      await this.$store.dispatch('ableshow', id)
      this.getvenue()
    },

    async delshow(id) {
      console.log("this is id", id)
      await this.$store.dispatch('delshow', id)
      this.getvenue()
    },

    async freeslots() {
      this.addshow['venue_id'] = this.venue_id
      this.addshow['date'] = this.addshow['date'] + " 00:00:00"
      for (const [key, value] of Object.entries(this.addshow)) {
        if (key == "duration") {
          if (value.length != 8) {
            alert("Please enter a valid duration")
            return
          }
          if (Number(value.slice(0, 2) > 4 || Number(value.slice(3, 5) > 59) || Number(value.slice(6, 8) > 59))) {
            alert("Please enter a valid duration")
            return
          }
        }

      }
      console.log("this is addshow", this.addshow)
      this.freeslot = await this.$store.dispatch('freeslots', this.addshow)
      console.log("this is freeslot", this.freeslot)
    },

    async editfreeslots() {
      this.editshow['venue_id'] = this.venue_id
      this.editshow['date'] = this.editshow['date'] + " 00:00:00"
      console.log("this is editshow", this.addshow)
      this.freeslot = await this.$store.dispatch('freeslots', this.editshow)
      console.log("this is freeslot", this.freeslot)

    },

    async newshow() {
      console.log("this is addshow", this.addshow)
      for (const [key, value] of Object.entries(this.addshow)) {
        if (value == "") {
          alert("Please fill all the fields")
          return
        }

      }
      if (this.freeslot.length > 0) {
        if (this.addshow['slot'] != -1) {
          this.addshow['date'] = this.addshow['slot'][0]
          console.log("this is addshow2", this.addshow)
        }
        else {
          this.addshow['date'] = this.addshow['date'].slice(0, 11) + " " + this.addshow['time'] + ":00"
        }
      }
      else {
        this.addshow['date'] = this.addshow['date'].slice(0, 11) + " " + this.addshow['time'] + ":00"
      }
      console.log("this is addshow3", this.addshow)
      this.addshow['venue_id'] = this.venue_id
      this.$store.dispatch('addshow', this.addshow)
      this.getvenue()
      this.addshow = {}
    },

    async editshows(show) {
      this.editshow = show
      this.editshow['time'] = this.editshow['date'].slice(17, 25)
      var date = new Date(this.editshow['date']),
        mnth = ("0" + (date.getMonth() + 1)).slice(-2),
        day = ("0" + date.getDate()).slice(-2);
      this.editshow['date'] = [date.getFullYear(), mnth, day].join("-");
      this.editshow['duration'] = this.editshow['duration'].slice(17, 25)
      console.log("this is editshow", this.editshow)
      this.editshow['display'] = true
    },

    async edit() {
      console.log("this is editshow", this.editshow)
      if (this.freeslot.length > 0) {
        if (this.editshow['slot'] != -1) {
          this.editshow['date'] = this.editshow['slot'][0]
        }
        else {
          this.editshow['date'] = this.editshow['date'].slice(0, 11) + " " + this.editshow['time']
        }
      }
      else {
        this.editshow['date'] = this.editshow['date'].slice(0, 11) + " " + this.editshow['time']
      }
      this.editshow['venue_id'] = this.venue_id
      console.log("this is editshow", this.editshow)
      this.$store.dispatch('editshow', this.editshow)
      this.editshow['display'] = false
    },

    async generatecsv() {

      const csv = await this.$store.dispatch("generatecsv")
      console.log("sdfjdlkfj", csv)

      setTimeout(() => {

        axios.get(this.base_url + 'status/' + csv['task_id']).then((response) => {
          console.log("this is response", response.data['state'])
          if (response.data['state'] == "SUCCESS") {
            response = axios({
              url: this.base_url + 'getcsv',
              method: 'GET',
              responseType: 'blob', // important
              headers: {
                'content-type': 'application/json',
                'Authorization': 'Token ' + this.$store.getters.getjwt
              }
            }).then((response) => {
              console.log("this is response", response)
              const url = window.URL.createObjectURL(new Blob([response.data]));
              const link = document.createElement('a');
              link.href = url;
              link.setAttribute('download', 'file.csv'); //or any other extension
              document.body.appendChild(link);
              link.click();
            })
            console.log("this is response", response)
          }
          else {
            alert("Please try again")
          }
        })


      }, 7000)

    },

    async getchart() {
      console.log("this is chartshow", this.chartshow,this.charts)
      const id = this.chartshow
      this.charts = await this.$store.dispatch('getchart', id)
      console.log("this is chart", this.charts)
      this.charts['display'] = true
    },

  async getshowforchart(){
    this.charts['display'] = false
    this.show = this.getshow(this.chartvenue)
    console.log("this is show",this.show)
    this.venue_id =null
    this.charts['display'] = true
  },

  }


}
</script>
<style>
@media (min-width: 1024px) {
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

  .venues{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    justify-content: space-around;
    align-items: center;
    margin: 20px;
    padding: 20px;
    padding-top: 100px;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: #fff;
    font-size: 18px;
  }

  .venue {
    display: flex;
    background-color: white !important;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    margin: 20px;
    padding: 20px;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: black;
    font-size: 14px;
  }

  .shows {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin: 20px;
    padding: 20px;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: white;
    font-size: 18px;
  }

  .showdet {
    display: none;
    justify-content: space-around;
    align-items: center;
    margin: 20px;
    padding: 20px;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: white;
    font-size: 18px;
  }

  .venuedet {
    display: none;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    margin: 20px;
    padding: 20px;
    border-radius: 5px;
    background-color: white;
    color: black;
    font-size: 18px;
  }

  .editmenu {
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 20px;
    border: 10px solid black;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: white;
    font-size: 18px;
    z-index: 10;
    width: 600px;
  }
  
  .charts {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin: 20px;
    padding: 20px;
    border-radius: 5px;
    background-color: #4c9e9e;
    color: white;
    font-size: 18px;

  }

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

button {
  background: #2ecc71;
  width: 125px;
  padding-top: 5px;
  padding-bottom: 5px;
  color: white;
  border-radius: 4px;
  border: #27ae60 1px solid;

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
</style>