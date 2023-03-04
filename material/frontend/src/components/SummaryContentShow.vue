<template>
    <div>
        <div class="summary_day_wrapper">
            <p :class="[ is_empty ? 'empty' : 'summaryDay', {after : dateFlag}]" @click="select_summary">
                {{ meeting.day }}
            </p>
        </div>
        
        <div v-show="summary_open">
            <div class="info_wrapper">
                <label class="record">議事録記録者</label>
                <select v-model="this.meeting.recorder" class="select_event">
                    <option disabled value="">議事録作成者</option>
                    <option v-for="(person, person_key) in this.group_info.member" :key="person_key" :value="person">
                        {{ person }}
                    </option>
                </select>
            </div>
            <div class="info_wrapper">
                <label class="record">欠席者</label>
                <div v-for="(name, num) in this.meeting.absences" class="same_col" :key="num">
                    <select class="select_event" v-model="this.meeting.absences[num]">
                        <option disabled value="">欠席者</option>
                        <option v-for="(person, person_key) in this.group_info.member" :key="person_key" :value="person">
                            {{ person }}
                        </option>
                    </select>
                </div>
                <button v-if="this.meeting.absences.length < member_select.length" class="same_col add_button" @click="add_absence">+</button>
                <button v-if="this.meeting.absences.length > 0" class="same_col add_button" @click="minus_absence">-</button>
            </div>
            <div class="circle_wrapper content_info" v-show="announcement_button_flag">
                <p v-show="announcement_button_flag" :class="!announcement_open ? 'person':'selected_person'" @click="select_announcement">
                    全体
                </p>
            </div>
            <div v-show="announcement_open">
                <p class="content read-only" v-show="!announcement_edit_flag">
                    {{ meeting.announcement }}
                </p>
                <textarea class="content" v-show="announcement_edit_flag" cols="30" rows="10" v-model="meeting.announcement">
                    {{ meeting.announcement }}
                </textarea>
                <button v-show="!announcement_edit_flag" @click="edit_announcement()">Edit</button>
                <button v-show="announcement_edit_flag"  @click="edit_announcement()">Read</button>
            </div>
            <div v-for="(person, person_key) in this.group_info.member" :key="person_key">
                <div v-show="member_select[person_key]">
                    <div class="circle_wrapper content_info">
                        <p :class="personal_status(person_key)" @click="select_personal_summary(person_key)">
                            {{ person }}
                        </p>
                    </div>
                    <br/>
                    <div v-show="personal_summary[person_key]" v-for="(title, title_key) in titles" :key="title_key" class="content_box">
                        <div v-show="title_select[title_key]">
                            <div class="1">
                                <p :class="title_status(title_key)" @click="select_personal_content(person_key, title_key)">
                                    {{ title }}
                                </p>
                            </div>
                            <div>
                                <p v-show="edit_flag[person_key][title_key] === false" class="content read-only">
                                    {{ meeting.content[person_key][title_key] }}
                                </p>
                                <textarea class="content" v-show="edit_flag[person_key][title_key]" cols="30" rows="10" v-model="meeting.content[person_key][title_key]">
                                    {{ meeting.content[person_key][title_key] }}
                                </textarea>
                                <br/>
                                <button v-show="!edit_flag[person_key][title_key]" @click="edit_summary(person_key, title_key)">Edit</button>
                                <button v-show="edit_flag[person_key][title_key]" @click="edit_summary(person_key, title_key)">Read</button>
                            </div>
                            <!-- <div>
                                <div v-show="personal_content[person_key][title_key]">
                                    <p v-show="edit_flag[person_key][title_key] === false" class="content read-only">
                                        {{ meeting.content[person_key][title_key] }}
                                    </p>
                                    <textarea class="content" v-show="edit_flag[person_key][title_key]" cols="30" rows="10" v-model="meeting.content[person_key][title_key]">
                                        {{ meeting.content[person_key][title_key] }}
                                    </textarea>
                                    <br/>
                                    <button v-show="!edit_flag[person_key][title_key]" @click="edit_summary(person_key, title_key)">Edit</button>
                                    <button v-show="edit_flag[person_key][title_key]" @click="edit_summary(person_key, title_key)">Read</button>
                                </div>
                            </div> -->
                        </div>
                    </div>

                </div>
            </div>
            <button class="load_button" @click="load_summary(meeting.day)">Load</button>
            <button class="load_button" @click="load_summary(meeting.day)">Save</button>
        </div>

    </div>
</template>


<script>
import axios from 'axios'
import moment from 'moment'

let today = new Date()
let tomorrow = new Date(today.getFullYear(),today.getMonth(),today.getDate()+1)
export default {
    props:["meeting", "group_info", "member_select", "title_select", "day_index", "titles", "year"],
    data() {
        return {
            announcement_open:false,
            announcement_button_flag:false,
            announcement_edit_flag:false,
            summary_open:false,
            personal_summary:[],
            personal_content:[],
            edit_flag:[],
            dateFlag:"",
        }
    },
    created() {
        // console.log('push member_select, ',this.day_index)
        this.absence_num = this.meeting.absences.length;
        let now = this.meeting.day.split('/')
        // console.log("meeting.day",now[0],now[1],now[2])
        let date = new Date(now[0], now[1]-1, now[2])
        this.dateFlag = date > tomorrow
        console.log(tomorrow, date, this.dateFlag)
        for(let index = 0; index < this.group_info.member.length; index++){
            this.edit_flag.push([])
            this.personal_content.push([])
            for(let sIndex = 0; sIndex < this.titles.length; sIndex++) {
                // console.log("push false edit_flag and personal_content ",index)
                this.edit_flag[index].push(false)
                this.personal_content[index].push(false)
            }
            this.personal_summary.push(false)
            // console.log("meeting ",this.day_index, this.meeting)
        }
    },
    // mounted() {
    //     console.log(this.meeting.day.length)
    //     let num_list = this.meeting.day.split("/")
    //     this.date.year = num_list[0]-0
    //     this.date.month = num_list[1]-0
    //     this.date.day = num_list[2]-0
    // },
    methods:{
        select_summary:function() {
            if(this.dateFlag) return this.summary_open = false;
            this.summary_open = !this.summary_open
            if(!this.summary_open) {
                this.recorder_edit_flag = false
                this.announcement_open = false
                this.announcement_button_flag = false
                this.close_summary()
            }
        },
        select_announcement:function() {
            this.announcement_open = !this.announcement_open
        },
        close_summary:function() {
            console.log("close_summary")
            for(let index = 0; index < this.member_select.length; index++) {
                console.log(index)
                this.personal_summary.splice(index, 1, false)
                for(let sIndex = 0; sIndex < this.titles.length; sIndex++) {
                    this.personal_content[index].splice(sIndex, 1, false)
                    this.edit_flag[index].splice(sIndex, 1, false)
                }
            }
        },
        close_summary_member:function() {
            for(let index = 0; index < this.member_select.length; index++) {
                this.personal_summary.splice(index, 1, false)
                for(let sIndex = 0; sIndex < this.titles.length; sIndex++) {
                    this.personal_content[index].splice(sIndex, 1, false)
                    this.edit_flag[index].splice(sIndex, 1, false)
                }
                this.member_select.splice(index, 1, false)
            }
        },
        change_announcement_button() {
            this.announcement_button_flag = !this.announcement_button_flag
            console.log(this.announcement_button_flag)
            if (!this.announcement_button_flag) {
                this.announcement_open = false
            }
        },
        edit_announcement() {
            this.announcement_edit_flag = !this.announcement_edit_flag
        },
        edit_recorder() {
            this.recorder_edit_flag = !this.recorder_edit_flag
        },
        add_absence() {
            this.meeting.absences.push("");
            console.log(this.meeting.absences,this.meeting.absences.length)
        },
        minus_absence() {
            this.meeting.absences.pop();
        },
        check_absence(person) {
            console.log("person",person)
            console.log("return",this.absences.indexOf(person) === -1)
            return this.absences.indexOf(person) === -1;
        },
        check_absence_before_post() {
            console.log("before check")
            let res_absence = [];
            for(var i = 0; i < this.meeting.absences.length; i++) {
                console.log(this.meeting.absences[i],typeof(this.meeting.absences[i]));
                if(typeof(this.meeting.absences[i]) === "undefined") {continue;}
                else if(res_absence.indexOf(this.meeting.absences[i]) != -1){continue;}
                console.log("input name,",this.meeting.absences[i])
                res_absence.push(this.meeting.absences[i]);
            }
            this.meeting.absences.splice(0, this.meeting.absences.length)
            this.meeting.absences.push(...res_absence)
            console.log("after check", this.meeting.absences)
        },
        select_title(key) {
            this.title_select[key] = !this.title_select[key]
        },
        title_status(key) {
            return {
                title:this.title_select[key],
                selected_title:!this.title_select[key]
            }
        },
        select_personal_summary:function(key) {
            this.personal_summary.splice(key, 1, !this.personal_summary[key])
            if (!this.personal_summary[key]) {
                for(let index = 0; index < this.titles.length; index++) {
                    this.personal_content[key].splice(index, 1, false)
                    this.edit_flag[key].splice(index, 1, false)
                }
            }
        },
        select_personal_content:function(person_key, title_key) {
            this.personal_content[person_key].splice(title_key, 1, !this.personal_content[person_key][title_key])
        },
        close_personal_summary:function(key) {
            for(let index = 0; index < this.titles.length; index++) {
                this.edit_flag[key].splice(index, 1, false)
                this.personal_content[key].splice(index, 1, false)
            }
            this.personal_summary.splice(key, 1, false)
        },
        close_title:function(key) {
            for(let index = 0; index < this.member_select.length; index++) {
                this.edit_flag[index].splice(key, 1, false)
                this.personal_content[index].splice(key, 1, false)
            }
            this.title_select.splice(key, 1, false)
        },
        edit_summary:function(person_key, title_key) {
            this.edit_flag[person_key].splice(title_key, 1, !this.edit_flag[person_key][title_key])
        },
        async load_summary() {
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
            try {
                let url = `${this.$route.path}/${this.day_index}`
                console.log("post url", url)
                await this.check_absence_before_post();
                console.log("post meeting",this.meeting)
                await axios.post(url, {
                    meeting:this.meeting,
                    sep_date_flag:sep_date_flag,
                })
            } catch (err) {
                return
            }

            console.log("end load_summary")
            this.$nextTick(function() {
                this.$emit('load_summary', this.day_index)
            })
        },
        personal_status:function(key) {
            return  {
                selected_person:this.personal_summary[key],
                person:!this.personal_summary[key]
            }
        }
    },
    computed:{
        is_empty() {
            if(this.dateFlag) return false
            // console.log("empty check, ",this.day_index,this.meeting.recorder)
            if(this.meeting.recorder === ""){
                // console.log("empty")
                return true;
            }
            // console.log("exist recorder")
            return false;
        }
    }
}
</script>

<style>
.summaryDay, .empty{
    /* border: rgb(245, 235, 235) solid 0.1em; */
    width: 200px;
    margin: 10px;
    padding: 10px;
    cursor: pointer;
    white-space: pre-wrap;
    text-align: center;
    border-radius: 10px;
    font-size: 30px;
    background-color: white;
    /* border-color: linear-gradient(320deg, #3fc3da, #b7c9fc); */
    border: 10px solid;
    border-image-slice: 1;
}
.summaryDay {
    border-image-source: linear-gradient(320deg, #ca8585, #9785ca);
}
.empty {
    border-image-source: linear-gradient(320deg, #f11616, #ede608);
}
.after {
    opacity: 0.5;
}
.content_box {
    width: 500px;
    max-height: 300px;
    margin: 10px;
    display: inline-block;
}
.info_wrapper {
    height: 60px;
    line-height: 40px;
}
.announcement, .selected_announcement {
    font-size: 30px;
    color: black;
    text-align: center;
    line-height: 60px;
    height: 60px;
    background: white;
    cursor: pointer;
    width: 100px;
    margin-left:90px;
}
.announcement:hover, .selected_announcement {
    opacity: 0.5;
}
/* .content_person, .selected_content_person {
    margin-left: 110px;
} */
.record,
.record-content {
    font-size: 20px;
    width: 200px;
    height: 40px;
    padding: auto;
    display: inline-block;
}
.record {
    text-align: center;
}
.record-content {
    text-align: left;
    border: black solid 0.1em;
    margin-bottom: 0px;
}
.edit_single_line {
    text-align: left;
    line-height: 20px;
    font-size: 20px;
    background-color: #fff;
    padding: 10px;
    margin: auto;
    height: 40px;
    width: 200px;
}
.content {
    font-size:20px;
    white-space: pre-wrap;
    text-align: left;
    width: 500px;
    height: 100px;
    margin: 10px;
    border: black solid 0.1em;
}
.read-only {
    color:black;
    background-color: white;
    padding: 10px;
    margin:auto;
    overflow: auto;
}
.load_button {
    margin-top:10px;
    margin-bottom: 10px;
}
.same_col {
    display: inline-block;
}
.select_event {
    width: 100px;
    height: 40px;
    margin:0px 10px;
}
</style>