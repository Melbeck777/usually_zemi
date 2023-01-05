<template>
  <div id="drop-down">
    <h1 v-on:click="select_group">{{ group_info.lab_name }}</h1>
    <h2>{{ group_info.group_name }}</h2>
    <h2>{{ group_info.member }}</h2>
    <p>{{ meeting[0].day }}</p>
    <p>{{ meeting[0].content }}</p>
    <p>{{ meeting[1].day }}</p>
    <p>{{ meeting[1].content }}</p>
    <p>{{ meeting[2].day }}</p>
    <p>{{ meeting[2].content }}</p>
    <p>{{ summary_open_list }}</p>
    <p>{{ member_select }}</p>
    <p>{{ edit_flag }}</p>
    <!-- <dl>
      <dt class="meeting_list" v-bind:class="{group_flag}" @click="select_group">
        {{ group_info.group_name }}
      </dt>
      <dd v-show="group_flag">
        <h2>メンバー</h2>
        <div class="member">
          <div class="get-person" v-for="(person, key) in group_info.member" v-bind:key="key">
              <p v-on:click="select(key)" :class="select_person(key)">{{ person }}</p>
          </div>
        </div>
        <div class="meeting" v-for="(current_meeting, meeting_key) in meeting" v-bind:key="meeting_key">
          <dl>
            <dt class="summary_content" v-bind:class="{summary_open_list}" @click="summary_select_group(meeting_key)">
              {{ current_meeting.day }}
            </dt>
            <div v-show="summary_open_list[meeting_key]">
              <div v-for="(personal_content, content_key) in current_meeting.content" v-bind:key="content_key">
                <p class="member">{{ group_info.member[content_key] }}</p>
                <textarea class="content edit" v-show="edit_flag[meeting_key][content_key]" cols="50">{{ personal_content }}</textarea>
                <p class="content read-only" v-show="edit_flag[meeting_key][content_key] == false">{{ personal_content }}</p>
                <button v-on:click="get_summary( meeting_key, content_key)">読み込み</button>
                <button v-on:click="save_summary(meeting_key, content_key)">保存</button>
                <button v-on:click="edit_summary(meeting_key, content_key)">編集</button>
              </div>
            </div>
          </dl>
        </div>
      </dd>
    </dl> -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props:["group_info", "meeting"],
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
        edit_flag:[],
        member_select:[]
      };
  },
  mounted:function() {
    this.fetch_data()
  },
  methods:{
      select_group: function() {
          this.group_flag = !this.group_flag
          if(this.member_select.length != this.group_info.member.length) {
            for(let index = 0; index < this.group_info.member.length; index++) {
              this.member_select.push(false)
            }
          }
          if(this.summary_open_list.length != this.meeting.length) {
            for(let index = 0; index < this.meeting.length; index++) {
              this.summary_open_list.push(false)
              this.edit_flag.push(this.member_select)
            }
          }
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
      summary_select_group: function(key) {
          this.summary_open_list.splice(key, 1, !this.summary_open_list[key])
          console.log(this.summary_open_list)
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
.meeting_list {
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
.member {
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