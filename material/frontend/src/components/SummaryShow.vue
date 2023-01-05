<template>
  <div id="summary_show">
    <h1>{{ group_info.lab_name }}</h1>
    <dl>
      <dt  class="summary_show" v-bind:class="{group_flag}" @click="select_group">
        {{ group_info.group_name }}
      </dt>
      <dd v-show="group_flag">
        <div class="member_show">
          <div class="get-person" v-for="(person, person_key) in group_info.member" v-bind:key="person_key">
            <p v-on:click="select(person_key)" :class="select_person(person_key)">{{ person }}</p>
          </div>
        </div>

        <div class="meeting_show">
          <div v-for="(current_meeting, meeting_key) in meeting" v-bind:key="meeting_key">
            <dt class="summary_content" v-bind:class="{summary_open_list}" @click="summary_select(meeting_key)">
              {{ current_meeting.day }}
            </dt>
            <div v-show="summary_open_list[meeting_key]">
              <div>
                <div v-for="(person, person_key) in group_info.member" v-bind:key="person_key" >
                  <p class="person" v-on:click="select_person_content(meeting_key,person_key)">{{ person }}</p>
                  <div v-show="personal_summary[meeting_key][person_key]">
                    <p class="content read-only" v-show="edit_flag[meeting_key][person_key] === false">
                      {{ current_meeting.content[person_key] }}
                    </p>
                    <textarea v-show="edit_flag[meeting_key][person_key]" cols="50">
                      {{ current_meeting.content[person_key] }}
                    </textarea>
                    <button v-on:click="get_summary(meeting_key, person_key)">Load</button>
                    <button v-on:click="save_summary(meeting_key, person_key)">Save</button>
                    <button v-on:click="edit_summary(meeting_key, person_key)">Edit</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </dd>
    </dl>
    <p>{{ summary_open_list }}</p>
    <p>{{ member_select }}</p>
    <p>{{ personal_summary }}</p>
    <p>{{ edit_flag }}</p>
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
          // if(this.member_select.length != this.group_info.member.length) {
          //   this.create_flag()
          // }
      },
      create_flag:function() {
        console.log(this.group_info.member)
        console.log(this.meeting)
        for(let index = 0; index < this.group_info.member.length; index++) {
          this.member_select.push(false)
        }
        for(let index = 0; index < this.meeting.length; index++) {
          this.summary_open_list.push(false)
          this.edit_flag.push(this.member_select.slice(0, this.member_select.length))
          this.personal_summary.push(this.member_select.slice(0, this.member_select.length))
        }
      },
      select: function(key) {
          this.member_select.splice(key, 1, !this.member_select[key])
          console.log(this.member_select)
      },
      select_person: function(key) {
        return{
          selected_person:this.member_select[key],
          person:!this.member_select[key]
        }
      },
      summary_select: function(key) {
          this.summary_open_list.splice(key, 1, !this.summary_open_list[key])
          console.log(this.summary_open_list)
      },
      select_person_content: function(meeting_key, person_key){
        this.personal_summary[meeting_key].splice(person_key,1,!this.personal_summary[meeting_key][person_key])
      },
      get_summary: function(meeting_key, content_key) {
        console.log(`get ${meeting_key} ${content_key}`)
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
  max-height: fit-content ;
  text-align: left;
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
.get-person {
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