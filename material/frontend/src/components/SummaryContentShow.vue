<template>
    <div class="container">
        <p class="summary_day" @click="select_summary">
            {{ meeting.day }}
        </p>
    
        <div v-show="summary_open">
            <p :class="!this.announcement_open ? 'announcement':'selected_announcement'" @click="select_announcement">
                全体
            </p>
            <div v-show="announcement_open">
                <p class="content read-only">
                    {{ meeting.announcement }}
                </p>
            </div>
            <div v-for="(person, person_key) in member" :key="person_key">
                <div v-show="member_select[person_key]">
                    <p :class="personal_status(person_key)" @click="select_personal_summary(person_key)">
                        {{ person }}
                    </p>
                    <div v-show="personal_summary[person_key]">
                        <p v-show="edit_flag[person_key] === false" class="content read-only">
                            {{ meeting.content[person_key] }}
                        </p>
                        <textarea class="content" v-show="edit_flag[person_key]" cols="100" rows="10" v-model="meeting.content[person_key]">
                            {{ meeting.content[person_key] }}
                        </textarea>
                        <br/>
                        <button v-show="!edit_flag[person_key]" @click="edit_summary(person_key)">Edit</button>
                        <button v-show="edit_flag[person_key]" @click="edit_summary(person_key)">Read</button>
                    </div>
                </div>
            </div>
            <button @click="load_summary(meeting.day)">Load</button>
            <button @click="load_summary(meeting.day)">Save</button>
        </div>

    </div>
</template>


<script>
import axios from 'axios'

export default {
    props:["meeting", "member", "member_select", "day_index", "titles"],
    data() {
        return {
            announcement_open:false,
            summary_open:false,
            personal_summary:[],
            edit_flag:[],
            date:{
                year:0,
                month:0,
                day:0,
            }
        }
    },
    created() {
        for(let index = 0; index < this.member.length; index++){
            this.edit_flag.push(false)
            this.personal_summary.push(false)
        }
    },
    mounted() {
        console.log(this.meeting.day.length)
        let num_list = this.meeting.day.split("/")
        this.date.year = num_list[0]-0
        this.date.month = num_list[1]-0
        this.date.day = num_list[2]-0
    },
    methods:{
        select_summary:function() {
            this.summary_open = !this.summary_open
            if(!this.summary_open) {
                this.announcement_open = false
                this.close_summary()
            }
        },
        select_announcement:function() {
            this.announcement_open = !this.announcement_open
        },
        close_summary:function() {
            for(let index = 0; index < this.member_select.length; index++) {
                this.personal_summary.splice(index, 1, false)
                this.member_select.splice(index, 1, false)
                this.edit_flag.splice(index, 1, false)
            }
        },
        select_personal_summary:function(key) {
            this.personal_summary.splice(key, 1, !this.personal_summary[key])
        },
        close_personal_summary:function(key) {
            this.personal_summary.splice(key, 1, false)
            this.edit_flag.splice(key, 1, false)
        },
        edit_summary:function(key) {
            this.edit_flag.splice(key, 1, !this.edit_flag[key])
        },
        load_summary:function() {
            console.log("meeting")
            console.log(this.meeting)
            console.log("day_index")
            console.log(this.day_index)
            let confirm_text = ""
            for(let index = 0; index < this.titles.length; index++) {
                if (index != 0){
                    confirm_text += ", "
                }
                confirm_text += this.titles[index]
            }
            confirm_text += "\n上記のタイトルを含む資料を作成していますか？"
            let sep_date_flag = false;
            if(confirm(confirm_text)) {
                sep_date_flag = true
            }
            console.log('meeting')
            console.log(this.meeting)
            axios.post(this.$route.path, {
                meeting:this.meeting,
                day_index:this.day_index,
                sep_date_flag:sep_date_flag
                
            }).then(function(response) {
                console.log(response.data)
            })
            this.$emit('load_summary')
        },
        personal_status:function(key) {
            return  {
                selected_content_person:this.personal_summary[key],
                content_person:!this.personal_summary[key]
            }
        }
    },
}
</script>

<style>
.summary_day {
    position: relative;
    background-color:rgb(235, 211, 211);
    border: rgb(245, 235, 235) solid 0.1em;
    max-width: 180px;
    margin: 10px;
    padding: 10px;
    cursor: pointer;
    white-space: pre-wrap;
    text-align: center;
    border-radius: 10px;
    font-size: 20px;
}
.announcement, .selected_announcement {
    font-size: 20px;
    color: #fff;
    text-align: center;
    line-height: 60px;
    height: 60px;
    background: linear-gradient(320deg, #3fc3da, #b7c9fc);
    cursor: pointer;
    width: 100px;
    margin-left:90px;
}
.announcement:hover, .selected_announcement {
    opacity: 0.5;
}
.content_person, .selected_content_person {
    margin-left: 110px;
}
.content {
    font-size:20px;
    max-width: 1000px;
    white-space: pre-wrap;
    text-align: left;
    width: auto;
    border: black solid 0.1em;
}
.read-only {
    color:black;
    height:auto;
    background-color: white;
    padding: 10px;
    margin:auto;
}
</style>