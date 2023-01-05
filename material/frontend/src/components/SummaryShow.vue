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
            <p class="summary_content" :class="{summary_open_list}" @click="select_summary(meeting_key)">{{ current_meeting.day }}</p>
            <div v-show="summary_open_list[meeting_key]">
              <div v-for="(person, person_key) in group_info.member" :key="person_key"> 
                <p class="person" @click="select_personal_summary(meeting_key, person_key)">
                  {{ person }}
                </p>
                <div v-show="personal_summary[meeting_key][person_key]">
                  <p v-show="edit_flag[meeting_key][person_key] === false" class="content read-only">
                    {{ current_meeting.content[person_key] }}
                  </p>
                  <textarea class="content" v-show="edit_flag[meeting_key][person_key]" cols="50" rows="10">
                    {{ current_meeting.content[person_key] }}
                  </textarea>
                  <button @click="load_summary(meeting_key, person_key)">Load</button>
                  <button @click="save_summary(meeting_key, person_key)">Save</button>
                  <button @click="edit_summary(meeting_key, person_key)">Edit</button>
                </div>
              </div>
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
      load_summary: function(meeting_key, content_key) {
        console.log(`load ${meeting_key} ${content_key}`)
      },
      save_summary: function(meeting_key, content_key) {
          console.log(`save ${meeting_key} ${content_key}`)
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
          console.log("group_info")
          console.log(this.group_info)
          console.log("group_info.lab_name")
          console.log(this.group_info.lab_name)
          console.log("group_info.group_name")
          console.log(this.group_info.group_name)
          console.log("group_info.member")
          console.log(this.group_info.member)
          console.log("meeting")
          console.log(this.meeting)
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
  background-color: #eee;
  max-width: 200px;
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
.summary_content {
  position: relative;
  background-color: lightblue;
  border: black solid 0.1em;
  max-width: 150px;
  margin: 10px;
  padding: 10px;
  cursor: pointer;
  white-space: pre-wrap;
  text-align: center;
}
textarea {
  font-size: 15pt;
  padding: 10px;
  margin: 5px;
}
button {
  background-color: orange;
  color:white;
  font: 20px bold;
  padding: 5px 10px;
  margin: 5px 10px;
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
.person, .selected_person {
  font-size: 15px;
  color: #fff;
  text-align: center;
  line-height: 50px;
  width: 50px;
  height: 50px;
  background-color: #777;
  margin: 10px;
  cursor: pointer;
}
.content {
  white-space: pre-wrap;
  text-align: left;
}
.read-only {
  font-size:20px;
  color:black;
  width:auto;
  height:auto;
  background-color: white;
  max-width: 600px;
  border: black solid 0.1em;
  margin:auto;
  padding: 10px;
}
</style>