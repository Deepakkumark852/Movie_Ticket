<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { EventBus } from '../utils/index.js'
</script>
<template>
  <div class="about">
    <div class="box">
      <h1>Login</h1>
      <input class="email" type="text" v-model="username" placeholder="Username">
      <input class="password" type="password" v-model="password" placeholder="Password">
      <div class="radio">
        <label for="user"><input type="radio" id="user" value="user" v-model="role" />USER</label>

        <label for="admin"><input type="radio" id="admin" name="contact" value="admin" v-model="role" />ADMIN</label>
      </div>

      <button class="btn" @click="Authenticate">Login</button>
      <button class="btn2"><RouterLink to="/register">Register</RouterLink></button>
    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 25vh;
    display: flex;
    align-items: center;
    padding-top: 50px;
  }

  .box {
    background: teal;
    width: 300px;
    border-radius: 6px;
    margin: 0 auto 0 auto;
    padding: 10px 10px 70px 10px;
    border: #2980b9 4px solid;
  }

  .email {
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

  .password {
    border-radius: 4px;
    background: #ecf0f1;
    border: #ccc 1px solid;
    padding: 8px;
    width: 250px;
    font-size: 1em;
  }

  input[type="radio"] {
    position: relative;
    top: 10px;
    bottom: 10px;
    margin-top: 0px;
    margin-bottom: 10px;
    padding: 0px;
  }

  .btn {
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
    margin-left: 1px;
    font-weight: 800;
    font-size: 0.8em;
    position: relative;
    top: 10px;

  }

  .btn:hover {
    background: #2CC06B;
  }


.btn2{
    width: 125px;
    padding-top: 5px;
    padding-bottom: 5px;
    color: white;
    border-radius: 4px;
    border: #27ae60 1px solid;

    margin-top: 20px;
    margin-bottom: 20px;
    float: left;
    margin-left: 5px;
    font-weight: 800;
    font-size: 0.8em;
    position: relative;
    top: 10px;
    background:#3498db;
}

.btn2:hover{ 
background:#3594D2; 
}

}
</style>
<script>
import axios from 'axios'
import config from '../config'
export default {
  data() {
    return {
      base_url: config.base_url,
      username: '',
      password: '',
      role: '',
    }
  },
  methods:
  {
    async Authenticate() {
      //  const response = await this.auth_api();
      // console.log(response.data)
      if (this.role == 'user') {
        this.$store.dispatch('login', { username: this.username, password: this.password })
          .then(() => {
            if (this.$store.getters.isAuthenticated) {
              this.$router.push('/user')
            }
            else {
              console.log('failed', this.$store.state.getjwt)
              this.$router.push('/login')
            }
          })
      }

      if (this.role == 'admin') {

        this.$store.dispatch('adminlogin', { username: this.username, password: this.password })
          .then(() => {
            if (this.$store.getters.isadminAuthenticated) {
              // console.log('success', this.$store.getters.getjwt)
              this.$router.push('/admin')
            }
            else {
              console.log('failed', this.$store.state.getjwt)
              this.$router.push('/login')
            }
          })
      }





    },
  },
  mounted() {
    console.log('jwt', this.$store.state.getjwt)
    EventBus.on('failedAuthentication', (msg) => {
      console.log(msg)
      this.$router.push('/login')
    })
    EventBus.on('failedRegister', (msg) => {
      console.log(msg)
      this.$router.push('/login')
    })

  },

  beforeDestroy() {
    EventBus.off('failedAuthentication')
    console.log('off')
    EventBus.off('failedRegister')
  }

}



</script>

