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
                    <select v-show="!labFlag" class="user_select" v-model="labName">
                        <option v-for="(lab, lab_key) in labInfo" :key="lab_key">{{ lab }}</option>
                    </select>
                    <button v-show="!labFlag" @click="checkLab">新規</button>
                    <input type="text" v-model="labName">
                    <button v-show="labFlag" @click="addLab">追加</button>
                    <button v-show="labFlag" @click="checkLab">選択</button>
                </td>
                <td class="user_info">
                    <select class="user_select" v-model="groupName">
                        <option v-for="(group, group_key) in selectedTeams" :key="group_key">{{ group }}</option>
                    </select>
                    <button v-show="!labFlag" @click="checkTeam">新規</button>
                    <input type="text" v-model="labName">
                    <button v-show="labFlag" @click="addTeam">追加</button>
                    <button v-show="labFlag" @click="checkTeam">選択</button>
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
        <button class="move_button" @click="register">Register</button>
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
            labId:-1,
            labName:"",
            groupId:-1,
            groupName:"",
            grade:"",
            studentNumber:"",
            emailAddress:"",
            password:"",
            grades:[],
            selectedTeams:[],
            labInfo:[],
            labFlag:false,
            teamFlag:false
        }
    },
    created() {

    },
    methods:{
        async register() {
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
        },
        checkLab() {
            this.labFlag = !this.labFlag;
        },
        addLab() {
            axios.post(`${this.$route.path}/lab`)
        },
        checkTeam() {
            this.labFlag = !this.labFlag;
        },
        addTeam() {
            axios.post(`${this.$route.path}/team`)
        },
        fetch_data() {
            axios.get(this.$route.path).then((result) => {
                var obj = JSON.parse(JSON.stringify(result.data));
                this.labInfo = obj.labInfo;
                this.groups = this.groups;
            })
        }
    },
    watch: {
        'labName':async function() {
            this.labId = this.labInfo[this.labName].id;
            this.selectedTeams = this.labInfo[this.labName].team;
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
    text-align: center;
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