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
        </div>
        <div class="title_show">
            <div class="load_title" v-for="(title, title_key) in titles" :key="title_key">
                <p :class="title_status(title_select[title_key])" @click="select_title(title_key)">{{ title }}</p>
            </div>
        </div>
    </div>
    <br/>
    <div class="weekly_show">
        <div v-for="(current_meeting, meeting_key) in meeting" :key="meeting_key">
            <SummaryContentShow ref="content_show" :member="this.group_info.member" :meeting="current_meeting"
                :member_select="this.member_select" :title_select="this.title_select" :titles="this.titles" :day_index="meeting_key"
                @load_summary="update_meeting"/>
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
            all_announcement_flag: false,
            summary_open_list: [],
            personal_summary: [],
            edit_flag: [],
            member_select: [],
            title_select: []
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
                for (let index = 0; index < obj.titles.length; index++) {
                    this.title_select.push(false)
                }
                console.log("meeting, ",this.meeting)
                console.log("end fetch dta")
            })
        },
        async update_meeting(meeting_key) {
            let url = `${this.$route.path}/${meeting_key}`
            console.log(url)
            await axios.get(url).then(result => {
                var obj = JSON.parse(JSON.stringify(result.data))
                this.meeting.splice(meeting_key, 1, obj)
            }).catch(error => console.log(error))
        }
    },
}
</script>

<style>
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
    margin-top: 200px;
    margin-left: 60px;
    margin-bottom: 200px;
}
.circle_wrapper {
    border-radius: 50%;
    background: linear-gradient(320deg, #3fc3da, #b7c9fc);
    line-height: 90px;
    width: 90px;
    height: 90px;
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
    background: linear-gradient(320deg, #da913f, #fcdcb7);
    color: black;
    font: 20px bold;
    padding: 5px 10px;
    margin: 5px 10px;
    border: whitesmoke;
    border-radius: 10px;
}

/* .month_divide {
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
} */

button:hover,
.person:hover,
.selected_person,
.title:hover,
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
    font-size: 25px;
    color: black;
    background-color: white;
    text-align: center;
    line-height: 80px;
    width: 80px;
    height: 80px;
    border-radius: 50px;
    z-index: 0;
}
.title_show {
    max-width: auto;
}

.title, .selected_title {
    width: 150px;
    margin: 10px;
    padding: 10px;
    cursor: pointer;
    white-space: pre-wrap;
    text-align: center;
    font-size: 20px;
    background-color: white;
    /* border-color: linear-gradient(320deg, #3fc3da, #b7c9fc); */
    border: 10px solid;
    border-image-source: linear-gradient(320deg, #ca8585, #9785ca);
    border-image-slice: 1;
}
textarea {
    padding: 10px;
    max-height: fit-content;
    text-align: left;
}
</style>