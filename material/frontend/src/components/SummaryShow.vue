<template>
  <div id="drop-down">
    <dl>
      <dt class="summary_show" :class="{group_flag}" @click="select_group">
        {{ group_info.group_name }}
      </dt>
      <dd v-show="group_flag">
        <div class="member_show">
          <div class="load_person" v-for="(person, person_key) in group_info.member" :key="person_key">
            <p :class="select_person(person_key)" @click="select(person_key)">{{ person }}</p>
          </div>
        </div>

        <div class="meeting_show">
          <div v-for="(current_meeting, meeting_key) in meeting" :key="meeting_key">
            <p class="summary_day" :class="{summary_open_list}" @click="select_summary(meeting_key)">{{ current_meeting.day }}</p>
            <div v-show="summary_open_list[meeting_key]">
              <div v-for="(person, person_key) in group_info.member" :key="person_key"> 
                <p class="person content_person" @click="select_personal_summary(meeting_key, person_key)">
                  {{ person }}
                </p>
                <div v-show="personal_summary[meeting_key][person_key]">
                  <p v-show="edit_flag[meeting_key][person_key] === false" class="content read-only">
                    {{ current_meeting.content[person_key] }}
                  </p>
                  <textarea class="content" v-show="edit_flag[meeting_key][person_key]" cols="50" rows="10" v-model="meeting[meeting_key].content[person_key]">
                    {{ current_meeting.content[person_key] }}
                  </textarea>
                  <br/>
                  <button v-show="!edit_flag[meeting_key][person_key]" @click="edit_summary(meeting_key, person_key)">Edit</button>
                  <button v-show="edit_flag[meeting_key][person_key]" @click="edit_summary(meeting_key, person_key)">Read</button>
                </div>
              </div>
              <button @click="save_summary(meeting_key, current_meeting.day)">Save</button>
              <button @click="load_summary(meeting_key, current_meeting.day)">Load</button>
            </div>
          </div>
        </div>
      </dd>
    </dl>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
      return {
        group_info:{
          lab_name:"",
          group_name:"",
          member:[]
        },
        meeting:[],
        group_flag:false,
        summary_open_list:[],
        personal_summary:[],
        edit_flag:[],
        member_select:[]
      };
  },
  created() {
    this.fetch_data()
  },
  methods:{
      select_group: function() {
        this.group_flag = !this.group_flag
      },
      select: function(key) {
        this.member_select.splice(key, 1, !this.member_select[key])
        console.log(this.member_select)
      },
      select_person: function(key) {
        return {
            selected_person:this.member_select[key],
            person:!this.member_select[key]
        }
      },
      select_summary: function(key) {
        this.summary_open_list.splice(key, 1, !this.summary_open_list[key])
        console.log(this.summary_open_list)
      },
      select_personal_summary: function(meeting_key, person_key) {
        this.personal_summary[meeting_key].splice(person_key, 1, !this.personal_summary[meeting_key][person_key])
      },
      load_summary: function(meeting_key, day) {
        console.log(`load ${meeting_key} ${day}`)
      },
      save_summary: function(meeting_key, day) {
          console.log(`save ${meeting_key} ${day}`)
      },
      edit_summary: function(meeting_key, content_key) {
        this.edit_flag[meeting_key].splice(content_key, 1, !this.edit_flag[meeting_key][content_key])
      },
      fetch_data: function() {
        console.log("fetch_data")
        let url = this.$route.path
        axios.get(url).then((result) => {
          var obj = JSON.parse(JSON.stringify(result.data))
          this.group_info.lab_name = obj.lab_name
          this.group_info.group_name = obj.group_name
          this.group_info.member = obj.member
          this.meeting = obj.meeting
          for(let index = 0; index < obj.member.length; index++) {
            this.member_select.push(false)
          }
          for(let index = 0; index < obj.meeting.length; index++) {
            this.summary_open_list.push(false)
            this.edit_flag.push(this.member_select.slice(0, this.member_select.length))
            this.personal_summary.push(this.member_select.slice(0, this.member_select.length))
          }
        })
        console.log("this.group_info")
        console.log(this.group_info)
        console.log("this.meeting")
        console.log(this.meeting)
        console.log("this.member_select")
        console.log(this.member_select)
        console.log("this.summary_open_list")
        console.log(this.summary_open_list)
        console.log("this.edit_flag")
        console.log(this.edit_flag)
        console.log("this.personal_summary")
        console.log(this.personal_summary)
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
.meeting_show {
  margin-left: 60px;
}
dt {
  border-radius: 10px;
}
dt::before{
  content: "+";
  display: block;
  position: absolute;
  right: 10px;
}
dt.group_flag::before {
  content: "-";
}
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
button {
  background: linear-gradient(320deg, #da913f, #fcdcb7);
  color:black;
  font: 20px bold;
  padding: 5px 10px;
  margin: 5px 10px;
  border: whitesmoke;
  border-radius: 10px;
}
button:hover, .person:hover, .selected_person{
  opacity: 0.5;
}
.member_show {
  overflow: hidden;
}
.load_person {
  display: inline-block;
}
.content_person {
  margin-left: 90px;
}
.person, .selected_person, .content_person {
  font-size: 20px;
  color: #fff;
  text-align: center;
  line-height: 60px;
  width: 80px;
  height: 60px;
  background-color: #777;
  cursor: pointer;
}
.person, .selected_person {
  margin:10px;
}
textarea {
  padding: 10px;
  max-height: fit-content ;
  text-align: left;
}
.content {
  font-size:20px;
  max-width: 600px;
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