<template>
    <div id="drop-down" class="container">
        <div class="basic_info">
            <h1 class="basic_content">{{ group_info.group_name }}</h1>
            <p class="count_meeting basic_content">ゼミ {{ meeting.length }}回</p>
        </div>
        <p :class="select_person(all_member_flag)" class="all_member" @click="select_all_member">all</p>
        <div class="member_show">
            <div class="load_person" v-for="(person, person_key) in group_info.member" :key="person_key">
                <p :class="select_person(member_select[person_key])" @click="select(person_key)">{{ person }}</p>
            </div>
        </div>
        <div class="weekly_show">
            <div v-for="(current_meeting, meeting_key) in meeting" :key="meeting_key">
                <SummaryContentShow ref="content_show" :member="this.group_info.member" :meeting="current_meeting"
                    :member_select="this.member_select" :titles="this.titles" :day_index="meeting_key"
                    @load_summary="fetch_data" @save_summary="fetch_data" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import SummaryContentShow from './SummaryContentShow.vue';

export default {
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
        SummaryContentShow
    },
    created() {
        this.fetch_data()
    },
    methods: {
        select: function (key) {
            this.member_select.splice(key, 1, !this.member_select[key])
            if (!this.member_select[key]) {
                for (let index = 0; index < this.meeting.length; index++) {
                    this.$refs.content_show[index].close_personal_summary(key)
                }
            }
        },
        select_all_member: function () {
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
        select_person: function (flag) {
            return {
                selected_person: flag,
                person: !flag
            }
        },
        month_show: function (month) {
            this.$router.push({ path: `${this.$route.path}/${month}` })
        },
        fetch_data: function () {
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