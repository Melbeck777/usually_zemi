<template>
    <div id="drop-down">
        <div class="basic_info">
            <p class="basic_content">{{ group_info.group_name }}</p>
            <p class="basic_content">合計{{ meeting.length }}回</p>
        </div>
        <div class="member_show">
            <p :class="select_person(all_member_flag)" class="all_member" @click="select_all_member">all</p>
            <div class="load_person" v-for="(person, person_key) in group_info.member" :key="person_key">
                <p :class="select_person(member_select[person_key])" @click="select(person_key)">{{ person }}</p>
            </div>
        </div>
        <div class="weekly_show">
            <div v-for="(current_meeting, meeting_key) in meeting" :key="meeting_key">
                <SummaryContentShow ref="content_show" :member="this.group_info.member" :meeting="current_meeting"
                    :member_select="this.member_select" :titles="this.titles" :day_index="meeting_key"
                    @load_summary="fetch_data"/>
            </div>
        </div>
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
            meeting: [],
            titles: [],
            month_divide: [],
            month_flag: [],
            all_member_flag: false,
            summary_open_list: [],
            personal_summary: [],
            edit_flag: [],
            member_select: []
        };
    },
    components: {
        SummaryContentShow,
    },
    created() {
        this.fetch_data()
    },
    methods: {
        select(key) {
            this.member_select.splice(key, 1, !this.member_select[key])
            if (!this.member_select[key]) {
                for (let index = 0; index < this.meeting.length; index++) {
                    this.$refs.content_show[index].close_personal_summary(key)
                }
            }
        },
        select_all_member() {
            console.log(this.all_member_flag)
            this.all_member_flag = !this.all_member_flag
            for (let index = 0; index < this.member_select.length; index++) {
                this.member_select.splice(index, 1, this.all_member_flag)
            }
            if (!this.all_member_flag) {
                for (let index = 0; index < this.meeting.length; index++) {
                    this.$refs.content_show[index].close_summary()
                }
            }
        },
        select_person(flag) {
            return {
                selected_person: flag,
                person: !flag
            }
        },
        to_monthly_show() {
            this.$router.push({ name:'monthly_show', params:{year:this.year, lab:this.group_info.lab_name, group:this.group_info.group} })
        },
        async fetch_data() {
            console.log("fetch_data")
            let url = this.$route.path
            axios.get(url).then((result) => {
                var obj = JSON.parse(JSON.stringify(result.data))
                this.group_info.lab_name = obj.lab_name
                this.group_info.group_name = obj.group_name
                this.group_info.member = obj.member
                this.meeting = obj.meeting
                this.titles = obj.titles
                for (let index = 0; index < obj.member.length; index++) {
                    this.member_select.push(false)
                }
            })
        }
    },
}
</script>

<style>
.summary_show {
    cursor: pointer;
    position: relative;
    padding: 10px;
    margin-left: 30px;
    background-color: #eee;
    max-width: 200px;
}

.weekly_show {
    margin-left: 60px;
}

.basic_content {
    font-size: 50px;
    color: white;
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
    background: linear-gradient(320deg, #da913f, #fcdcb7);
    color: black;
    font: 20px bold;
    padding: 5px 10px;
    margin: 5px 10px;
    border: whitesmoke;
    border-radius: 10px;
}

.month_divide {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-wrap: wrap;
    flex-wrap: wrap;
    -ms-flex-pack: distribute;
    justify-content: space-around;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
}

.month {
    background: linear-gradient(320deg, #3f7dda, #b7d7fc);
    color: white;
    font-size: 50px;
    text-align: center;
    border: whitesmoke;
    line-height: 140px;
    width: 140px;
    height: 140px;
    border-radius: 10px;
    margin: 20px;
    float: left;
}

button:hover,
.person:hover,
.selected_person,
.content_person:hover,
.selected_content_person {
    opacity: 0.5;
}

.member_show,
.basic_info {
    overflow: hidden;
}

.load_person,
.all_member {
    display: inline-block;
}

.person,
.selected_person,
.content_person,
.selected_content_person {
    font-size: 20px;
    color: #fff;
    text-align: center;
    line-height: 60px;
    width: 80px;
    height: 60px;
    background: linear-gradient(320deg, #3fc3da, #b7c9fc);
    cursor: pointer;
}

.person,
.selected_person {
    margin: 10px;
}

textarea {
    padding: 10px;
    max-height: fit-content;
    text-align: left;
}
</style>