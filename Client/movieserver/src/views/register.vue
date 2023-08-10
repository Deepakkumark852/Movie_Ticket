<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
    <div class="about">
    <div class="box">
      <h1>Register</h1>
      <input class="email" type="text" v-model="user['name']" placeholder="Name" required>
      <input class="email" type="text" v-model="user['username']" placeholder="Username">
      <input class="password" type="password" v-model="user['password']" placeholder="Password">
      <div class="radio">
        <label for="user" style="position: relative; left:20px; top:5px"><input type="checkbox" id="user" value="user" v-model="user['role1']" />  USER</label>

        <label for="admin" style="position: relative; left:40px; top:5px;"><input type="checkbox" id="admin" name="contact" value="admin" v-model="user['role2']" /> ADMIN</label>
      </div>

      <button class="btn2" style="left: 50px !important;" @click="register()">Register</button>
    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 50vh;
    display: flex;
    align-items: center;
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

  input[type="checkbox"] {
    position: relative;
    top: 1px;
    bottom: 10px;
    margin-top: 0px;
    margin-bottom: 10px;
    padding: 0px;
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

export default {
  name: 'Register',
  data() {
    return {
      user:{
      name: '',
      username: '',
      password: '',
      role1: '',
      role2: ''
      }
    }
  },
  methods: {
    async register() {
      console.log("register",this.user)
      if (this.user['role1'] == true && this.user['role2'] == true) {
        await this.$store.dispatch('register', this.user)
        await this.$store.dispatch('adminregister', this.user)
      } else if (this.user['role1'] == true) {
        this.$store.dispatch('register', this.user)
      } else if (this.user['role2'] == true) {
        this.$store.dispatch('adminregister', this.user)
      } else {
        console.log("no role")
      }
      this.$router.push('/login')
    }
  }
}

</script>
