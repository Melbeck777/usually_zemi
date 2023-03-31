<template>
    <table  class="input_table">
        <tr>
            <td class="user_info_label"><span class="red">*</span>メールアドレス</td>
            <td>
                <input class="user_input_long" type="text" required v-model="emailAddress">
            </td>
        </tr>
        <tr>
            <td class="user_info_label"><span class="red">*</span>パスワード</td>
            <td>
                <input class="user_input_long" type="password" required v-model="password">
                <span :class="iconType" @click="onClick"></span>
            </td>
        </tr>
    </table>
    <button class="move" @click="user_check">Login</button>
    <button class="move" @click="sign_in">New</button>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return  {
            emailAddress:"",
            password:"",
            isChecked:false
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
        },
        onClick() {
            this.isChecked = !this.isChecked;
        },
        inputType() {
            return this.isChecked ? "text":"password";
        },
        iconType() {
            return this.isChecked ? "fa-solid fa-eye-slash":"fa-solid fa-eye";
        },
        sign_in() {
            console.log("New button")
            this.$router.push({name:'singIn'})
        },
    }
}

</script>