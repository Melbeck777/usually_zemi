<template>
  <div id="drop-down">
    <dl>
      <dt class="summary_show" :class="{group_flag}" @click="select_group">
        {{ group_info.group_name }}
      </dt>
      <dd v-show="group_flag">
        <p class="count_meeting">ゼミ {{ meeting.length }}回</p>
        <p :class="select_person(all_member_flag)" class="all_member" @click="select_all_member">all</p>
        <div class="member_show">
          <div class="load_person" v-for="(person, person_key) in group_info.member" :key="person_key">
            <p :class="select_person(member_select[person_key])" @click="select(person_key)">{{ person }}</p>
          </div>
        </div>
        <div class="meeting_show">
          <div v-for="(current_meeting, meeting_key) in meeting" :key="meeting_key">
            <SummaryContentShow :member="this.group_info.member" :meeting="current_meeting" :member_select="this.member_select" :titles="this.titles" :day_index="meeting_key" @load_summary="fetch_data"  @save_summary="fetch_data"/>
          </div>
        </div>
      </dd>
    </dl>
  </div>
</template>

<script>
import axios from 'axios';
import SummaryContentShow from './SummaryContentShow.vue';

export default {
  data() {
      return {
        group_info:{
          lab_name:"",
          group_name:"",
          member:[]
        },
        meeting:[],
        titles:[],
        group_flag:false,
        all_member_flag:false,
        summary_open_list:[],
        personal_summary:[],
        edit_flag:[],
        member_select:[]
      };
  },
  components:{
    SummaryContentShow
  },
  created() {
    this.fetch_data()
  },
  methods:{
      hoge:function() {
        console.log("hoge")
      },
      select_group: function() {
        this.group_flag = !this.group_flag
      },
      select: function(key) {
        this.member_select.splice(key, 1, !this.member_select[key])
        console.log(this.member_select)
      },
      select_all_member:function() {
        console.log(this.all_member_flag)
        this.all_member_flag = !this.all_member_flag
        for(let index = 0; index < this.member_select.length; index++) {
          this.member_select.splice(index, 1, this.all_member_flag)
        }
      },
      select_person: function(flag) {
        return {
            selected_person:flag,
            person:!flag
        }
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
          this.titles  = obj.titles
          for(let index = 0; index < obj.member.length; index++) {
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
.meeting_show {
  margin-left: 60px;
}
.count_meeting {
  font-size: 25px;
  color: white;
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
button {
  background: linear-gradient(320deg, #da913f, #fcdcb7);
  color:black;
  font: 20px bold;
  padding: 5px 10px;
  margin: 5px 10px;
  border: whitesmoke;
  border-radius: 10px;
}
button:hover, .person:hover, .selected_person, .content_person:hover, .selected_content_person{
  opacity: 0.5;
}
.member_show {
  overflow: hidden;
}
.load_person {
  display: inline-block;
}

.all_member {
  display: inline-block;
}
.person, .selected_person, .content_person, .selected_content_person {
  font-size: 20px;
  color: #fff;
  text-align: center;
  line-height: 60px;
  width: 80px;
  height: 60px;
  background: linear-gradient(320deg, #3fc3da, #b7c9fc);
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
</style>