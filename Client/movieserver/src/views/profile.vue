<template>
    <div class="user" v-if="this.user">
        <h1>Profile</h1>
        <label>Name :<input type="text" v-model="user.name" :placeholder="user.name"></label><br>
        <label>Username:<input type="text" v-model="user.email" :placeholder="user.email"></label><br>
        <label>Password:<input type="password" v-model="user.password1"></label><br>
        <label>Reenter password:<input type="password" v-model="user.repassword"></label><br>
        <button class="btn2" @click="updateuser">Update</button>
        <button class="btn2" @click="deleteuser">Delete</button>
    </div>
    <div class="admin" v-else-if="this.admin">
        <h1>Profile</h1>
        <label>Name :<input type="text" v-model="user.name" :placeholder="admin.name"></label><br>
        <label>Username:<input type="text" v-model="user.email" :placeholder="admin.email"></label><br>
        <label>Password:<input type="password" v-model="admin.password"></label><br>
        <label>Reenter password:<input type="password" v-model="admin.repassword"></label><br>
        <button class="btn" @click="updateadmin">Update</button>
        <button class="btn" @click="deleteadmin">Delete</button>
    </div>
</template>

<script>

export default {

    data() {
        return {
            user: {
                username: '',
                password: '',
                role: '',
            },
            admin: {
                username: '',
                password: '',
                role: '',
            },
        }
    },
    mounted() {
        if (this.$store.getters.isAuthenticated) {
            this.getuser()
            // console.log(this.user)
        }
        else if (this.$store.getters.isadminAuthenticated) {
            this.getadmin()
        }
        else {
            this.$router.push('/login')
        }
    },


    methods: {

        async getuser() {
            const response = await this.$store.dispatch('getuser')
            this.user = response[0]
            // console.log(this.user)
        },

        async getadmin() {
            const response = await this.$store.dispatch('getadmin')
            this.admin = response.data
        },

        async updateuser() {
            for (const [key, value] of Object.entries(this.user)) {
                if (value == "") {
                    alert("Please fill all the fields")
                    return
                }

            }
            if (this.user.repassword) {
                if (this.user.password != this.user.repassword) {
                    alert("Password doesn't match")
                    return
                }
            }

            const response = await this.$store.dispatch('updateuser', this.user)
            console.log(response)
        },

        async updateadmin() {
            for (const [key, value] of Object.entries(this.admin)) {
                if (value == "") {
                    alert("Please fill all the fields")
                    return
                }

            }
            if (this.admin.repassword) {
                if (this.admin.password != this.admin.repassword) {
                    alert("Password doesn't match")
                    return
                }
            }

            const response = await this.$store.dispatch('updateadmin', this.admin)
            console.log(response)
        },

        async deleteuser() {
            const response = await this.$store.dispatch('deleteuser')
            console.log(response)
            this.$store.dispatch('logout')
            this.$router.push('/login')
        },

        async deleteadmin() {
            const response = await this.$store.dispatch('deleteadmin')
            console.log(response)
            this.$store.dispatch('logout')
            this.$router.push('/login')
        }

    }

}

</script>

<style>
input[type=text], input[type=password] {
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;

    background: #ecf0f1;
    border: #ccc 1px solid;
    border-bottom: #ccc 2px solid;
    width: 100%;
    color: black;
    font-size: 1em;
    border-radius: 4px;
}

label{
    font-size: 20px;
    font-weight: 600;
}

.btn{

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
    background:#2ecc71;
}
.btn:hover{
    background: #27ae60;
    cursor: pointer;
}

.btn2{
    width: 125px;
    padding-top: 5px;
    padding-bottom: 5px;
    color: white;
    border-radius: 4px;
    border: #3498ed 1px solid;

    margin-top: 20px;
    margin-bottom: 20px;
    float: left;
    margin-left: 1px;
    font-weight: 800;
    font-size: 0.8em;
    position: relative;
    top: 10px;
    background:#3498ed;
}

.user{
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


</style>






