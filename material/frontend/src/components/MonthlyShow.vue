<template>
    <div class="meeting_list">
        <div v-for="(meeting, meeting_key) in meeting_list" :key="meeting_key">
            <p @click="summary_select(meeting_key)" class="date_show">
                {{ meeting_days[meeting_key].month }}月{{ meeting_days[meeting_key].day }}日
            </p>
            <div class="summary_show" v-show="summary_open[meeting_key]">
                <div v-for="(person, person_key) in member" :key="person_key">
                    <p class="person">{{ person }}</p>
                    <p class="content read-only">
                        {{ meeting[person_key] }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props:["meeting_list", "member", "member_select"],
    data() {
        return {
            summary_open:[],
            meeting_days:[]
        }
    },
    mounted() {
        console.log(this.meeting_list)
        for(let index = 0; index < this.meeting_list.length; index++) {
            let num_list = this.meeting_list[index].day.split("/")
            this.meeting_days.push({month:num_list[1]-0, day:num_list[2]-0})
            this.summary_open.push(false)
        }
        console.log(this.meeting_list)
    }
}
</script>