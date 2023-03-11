<template>
    <div class="sign_in">
        <table class="input_table">
            <tr>
                <td class="user_info_label"><span class="red">*</span>苗字</td>
                <td class="user_info_label"><span class="red">*</span>名前</td>
            </tr>
            <tr class="input_div">
                <td class="user_info">
                    <input class="user_input" type="text" required v-model="firstName">
                </td>
                <td class="user_info">
                    <input class="user_input" type="text" required v-model="secondName">
                </td>
            </tr>
            <tr>
                <td class="user_info_label"><span class="red">*</span>セイ</td>
                <td class="user_info_label"><span class="red">*</span>メイ</td>
            </tr>
            <tr class="input_div">
                <td class="user_info">
                    <input class="user_input" type="text" required v-model="firstKana">
                </td>
                <td class="user_info">
                    <input class="user_input" type="text" required v-model="secondKana">
                </td>
            </tr>
            <tr>
                <td class="user_info_label">所属研究室</td>
                <td class="user_info_label">所属班</td>
            </tr>
            <tr class="input_div">
                <td class="user_info">
                    <select class="user_select" v-model="labName">
                        <option v-for="(lab, lab_key) in labNames" :key="lab_key">{{ lab }}</option>
                    </select>
                </td>
                <td class="user_info">
                    <select class="user_select" v-model="groupName">
                        <option v-for="(group, group_key) in selectedGroups" :key="group_key">{{ group }}</option>
                    </select>
                </td>
            </tr>
            <tr>
                <td class="user_info_label"><span class="red">*</span>学年・教員</td>
                <td class="user_info_label"><span class="red">*</span>学籍番号・教員番号</td>
            </tr>
            <tr class="input_div">
                <td class="user_info">
                    <select class="user_select" v-model="grade">
                        <option v-for="(grade_op, grade_key) in grades" :key="grade_key">{{ grade_op }}</option>
                    </select>
                </td>
                <td class="user_info">
                    <input class="user_input" type="text" required v-model="studentNumber">
                </td>
            </tr>
            <tr>
                <td class="user_info_label"><span class="red">*</span>メールアドレス</td>
                <td class="user_info">
                    <input class="user_input_long" type="text" required v-model="emailAddress">
                </td>
            </tr>
            <tr>
                <td class="user_info_label"><span class="red">*</span>パスワード</td>
                <td class="user_info">
                    <input class="user_input_long" type="text" required v-model="password">
                </td>
            </tr>
        </table>
        <button class="move_button" @click="submit">Register</button>
    </div>
</template>

<script>
import axios from 'axios'
import { watch } from 'vue'
export default {
    data() {
        return  {
            firstName:"",
            secondName:"",
            firstKana:"",
            secondKana:"",
            labName:"",
            groupName:"",
            grade:"",
            studentNumber:"",
            emailAddress:"",
            password:"",
            grades:["B3","B4","M1","M2","D1","D2","D3","教員"],
            selectedGroups:[],
        }
    },
    methods:{
        async submit() {
            let url = `${this.$route.path}`
            let result = await axios.post(url,{
                firstName:this.firstName,
                secondName:this.secondName,
                firstKana:this.firstKana,
                secondKana:this.secondKana,
                emailAddress:this.emailAddress,
                password:this.password,
                labName:this.labName,
                groupName:this.groupName,
                grade:this.grade,
                studentNumber:this.studentNumber,
            })
            if(result) {
                window.alert('認証成功')
            } else {
                window.alert('認証失敗\nすでにメールアドレスが登録されている可能性があります')
                this.$router.push({name:'login'})
            }
        }
    },
    watch: {
        'labName':async function() {
            let result = await axios.get(`${this.$route.push}/${this.labName}`);
            if(result.length > 0){
                this.selectedGroups = result
            } else {
                return false;
            }
        }
    }
}

</script>

<style>
.user_form_group {
    line-height: normal;
    width: 100px;
}
.user_info {
    /* font-size: 20px; */
    /* width: 300px; */
    text-align: center;
    /* padding: 5px; */
}
.user_input_long {
    font-size: 15px;
    width: 250px;
}
.user_input {
    font-size: 15px;
    width: 150px;
}
.user_info_label {
    margin: auto;
    font-size: 15px;
}
.user_select {
    min-width: 100px;
    max-width: 350px;
    font-size: 15px;
}
.move_button {
    font: white;
}
.input_table {
    background-color: aliceblue;
}
.red {
    color:red;
}
.input_div {
    margin-bottom: 15px;
}
</style>