<template>
    <div class="form-group">
        <input class="user_info" type="text" required v-model="emailAddress">
        <input class="user_info" type="text" required v-model="password">
    </div>
    <button class="move" @click="user_check()">Login</button>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return  {
            emailAddress:"",
            password:""
        }
    },
    methods:{
        user_check() {
            let post_url = this.$route.path;
            this.axios.post(post_url, {
                emailAddress:this.emailAddress,
                password:this.password
            }).then(res=>{
                console.log(res.data);
                this.$router.push({path:this.$router.path});
                this.$emit("loginSuccess");
            },(error)  => {
                console.log(error)
            }) 
        }
    }
}

</script>

