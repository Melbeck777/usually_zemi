<template>
    <div class="all_group_info">
        <div class="basic_info">
            <p class="basic_content">{{ group_info.group_name }}</p>
            <p class="basic_content">合計{{ meeting.length }}回</p>
        </div>
        <div class="member_show">
            <div class="circle_wrapper">
                <p :class="person_status(all_member_flag)"       class="all_member" @click="select_all_member">all</p>
            </div>
            <div class="circle_wrapper">
                <p :class="person_status(all_announcement_flag)" class="all_member" @click="select_all_announcement">全体</p>
            </div>
            <div class="circle_wrapper" v-for="(person, person_key) in group_info.member" :key="person_key">
                <p  :class="person_status(member_select[person_key])" @click="select_member(person_key)">{{ person }}</p>
            </div>
            <input placeholder="検索" class="search" type="text" v-model="keyword">
        </div>
        <div class="title_show">
            <div class="load_title" v-for="(title, title_key) in titles" :key="title_key">
                <p :class="title_status(title_select[title_key])" @click="select_title(title_key)">{{ title }}</p>
            </div>
        </div>
    </div>
    <div class="blank_show">
        <p>未提出</p>
        <div v-for="(person, person_key) in group_info.member" :key="person_key">
            <div v-show="member_select[person_key]">
                <p class="blank_person">{{ person }} ({{ blank[person_key].length }})</p>
                <div v-for="(blank_day, blank_key) in blank[person_key]" :key="blank_key">
                    <li class="blank_day">{{ blank_day }}</li>
                </div>
            </div>
        </div>
    </div>
    <br/>
    <div class="weekly_show">
        <div v-for="(current_meeting, meeting_key) in filteredMeeting" :key="meeting_key">
            <SummaryContentShow ref="content_show" :group_info="this.group_info" :meeting="current_meeting"
                :member_select="this.member_select" :title_select="this.title_select" :titles="this.titles" :day_index="meeting_key" :year="this.$route.params['year']" 
                @load_summary="update_meeting"/>
        </div>
        <button class="add_button">
            +
        </button>
    </div>
</template>

<script>
import axios from 'axios';
import SummaryContentShow from './SummaryContentShow.vue';
export default {
    props:["year"],
    data() {
        return {
            group_info: {
                lab_name: "",
                group_name: "",
                member: []
            },
            blank:[],
            meeting: [],
            titles: [],
            all_member_flag: false,
            all_announcement_flag: false,
            edit_flag: [],
            member_select: [],
            title_select: [],
            keyword:''
        };
    },
    components: {
        SummaryContentShow,
    },
    created() {
        this.fetch_data()
    },
    methods: {
        select_member(key) {
            this.member_select.splice(key, 1, !this.member_select[key])
            if (!this.member_select[key]) {
                for (let index = 0; index < this.meeting.length; index++) {
                    this.$refs.content_show[index].close_personal_summary(key)
                }
            }
        },
        select_title(key) {
            console.log("year",this.year)
            this.title_select.splice(key, 1, !this.title_select[key])
            if (!this.title_select[key]) {
                for (let index = 0; index < this.meeting.length; index++) {
                    this.$refs.content_show[index].close_title(key)
                }
            }
        },
        select_all_member() {
            console.log(this.all_member_flag)
            this.all_member_flag = !this.all_member_flag
            for (let index = 0; index < this.member_select.length; index++) {
                this.member_select.splice(index, 1, this.all_member_flag)
            }
            for(let index = 0; index < this.titles.length; index++) {
                this.title_select.splice(index, 1, this.all_member_flag)
            }
            if (!this.all_member_flag) {
                for (let index = 0; index < this.meeting.length; index++) {
                    this.$refs.content_show[index].close_summary()
                }
            }
        },
        select_all_announcement() {
            console.log(this.all_announcement_flag)
            this.all_announcement_flag = !this.all_announcement_flag
            for (let index = 0; index < this.meeting.length; index++) {
                this.$refs.content_show[index].change_announcement_button()
            }
        },
        person_status(flag) {
            return {
                selected_person: flag,
                person: !flag
            }
        },
        title_status(flag) {
            return {
                selected_title: flag,
                title: !flag
            }
        },
        to_monthly_show() {
            this.$router.push({ name:'monthly_show', params:{year:this.year, lab:this.group_info.lab_name, group:this.group_info.group} })
        },
        fetch_data() {
            console.log("start fetch data")
            let url = this.$route.path
            console.log('url, ',url)
            axios.get(url).then((result) => {
                var obj = JSON.parse(JSON.stringify(result.data))
                this.group_info.lab_name = obj.lab_name
                this.group_info.group_name = obj.group_name
                this.group_info.member = obj.member
                this.meeting = obj.meeting
                this.titles = obj.titles
                this.blank = obj.blank
                console.log("obj, ",obj)
                console.log("obj.member.length, ",obj.member.length)
                console.log("obj.titles.length, ",obj.titles.length)
                for (let index = 0; index < obj.member.length; index++) {
                    this.member_select.push(false)
                }
                for (let index = 0; index < obj.titles.length; index++) {
                    this.title_select.push(false)
                }
                console.log("meeting, ",this.meeting)
                console.log("end fetch data")
            })
        },
        // 議事録の更新
        async update_meeting(meeting_key) {
            let url = `${this.$route.path}/${meeting_key}`
            console.log(url)
            await axios.get(url).then(result => {
                var obj = JSON.parse(JSON.stringify(result.data))
                this.meeting.splice(meeting_key, 1, obj.meeting)
                this.blank = obj.blank
            }).catch(error => console.log(error))
            console.log('update meeting,',this.meeting)
        },
        // 予定の追加
        async add_meeting(add_date) {
            let url = `${this.$route.path}/add_day`
            await axios.post(url, {
                day:add_date
            })
            this.fetch_data()
        }
    },
    computed:{
        filteredMeeting:function() {
            if(this.keyword == "")return this.meeting
            var meeting = []
            console.log("start filteredMeeting")
            console.log("this.meeting, ",this.meeting)
            for(let i = 0; i < this.meeting.length; i++){
                var current_meeting = this.meeting[i]
                console.log("current_meeting, ",current_meeting)
                var now_flag = false
                for(let j = 0; j < current_meeting.content.length; j++) {
                    if(!this.member_select[j])continue;
                    for(let k = 0; k < current_meeting.content[j].length; k++) {
                        if(now_flag || !this.title_select[k])continue
                        if(current_meeting.content[j][k].indexOf(this.keyword) !== -1) {
                            meeting.push(current_meeting)
                            now_flag = true;
                        }
                    }
                }
            }
            console.log("end filteredMeeting")
            return meeting
        }
    }
}
</script>

<style>
.blank_show {
    position: fixed;
    font-size: 25px;
    width: 200px;
    margin-top: 250px;
    right:20px;
    border: solid beige;
}
.blank_person {
    text-align: center;
}
.blank_day {
    font-size: 20px;
    text-align: left;
    padding-left: 20px;
}

.content_show {
    z-index: 0;
}
.summary_show {
    cursor: pointer;
    position: relative;
    padding: 10px;
    margin-left: 30px;
    background-color: #eee;
    max-width: 200px;
}
.weekly_show {
    margin-top: 250px;
    margin-left: 60px;
    margin-bottom: 200px;
}
.circle_wrapper {
    border-radius: 50%;
    background: linear-gradient(320deg, #3fc3da, #b7c9fc);
    line-height: 80px;
    width: 80px;
    height: 80px;
    padding:5px;
    margin:10px;
}
.basic_content {
    font-size: 30px;
    color: black;
    display: inline;
    margin: 10px;
}

dt {
    border-radius: 10px;
}

dt::before {
    content: "+";
    display: block;
    position: absolute;
    right: 10px;
}

dt.group_flag::before {
    content: "-";
}

button {
    /* background: linear-gradient(320deg, #da913f, #fcdcb7); */
    background-color: #3fdada;
    color: white;
    font: 20px bold;
    padding: 5px 10px;
    margin: 5px 10px;
    border: whitesmoke;
    border-radius: 10px;
}
.person:hover,
.selected_person:hover,
.title:hover,
.selected_title:hover {
    transform: scale(0.7, 0.7);
}

button:hover,
.selected_person,
.selected_title {
    opacity: 0.5;
}
.all_group_info {
    position: fixed;
    top: 90px;
    left: 0;
    border: #b7c9fc solid 5px;
    background-color: white;
    width: 100%;
    z-index: 1;
}
.title_show,
.member_show,
.basic_info {
    overflow: hidden;
}
.load_title,
.load_person,
.circle_wrapper {
    display: inline-block;
}

.person {
    cursor: pointer;
}

.person,
.selected_person {
    font-size: 20px;
    color: black;
    background-color: white;
    text-align: center;
    line-height: 70px;
    width: 70px;
    height: 70px;
    border-radius: 50px;
    z-index: 0;
}
.title_show {
    max-width: auto;
}

.load_title {
    background:linear-gradient(320deg, #b5ca85, #85ca87);
    margin:5px 10px;
}
.title, .selected_title {
    width: 120px;
    margin: 10px;
    padding: 5px;
    cursor: pointer;
    white-space: pre-wrap;
    text-align: center;
    font-size: 20px;
    background-color: white;
    /* border-color: linear-gradient(320deg, #3fc3da, #b7c9fc); */
}
textarea {
    padding: 10px;
    max-height: fit-content;
    text-align: left;
}
.search {
    font-size: 20px;
    width: 200px;
    margin: 10px;
}
.add_button {
    margin: 10px;
    border-radius: 50%;
    background: #d1d3bcd9;
    width: 50px;
    height: 50px;
    padding:5px;
    font-size: 20px;
}
</style>