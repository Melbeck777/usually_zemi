<template>
  <div id="drop-down">
    <dl>
      <dt class="meeting_list" v-bind:class="{group_flag}" 
        @click="select_group">
        {{ group.name }}
      </dt>
      <dd v-show="group_flag">
        <h1>メンバー</h1>
        <div class="member">
          <div class="get-person" v-for="(person, key) in group.member" v-bind:key="key">
              <p v-on:click="select(key)" :class="select_person(key)">{{ person }}</p>
          </div>
        </div>
        <div class="meeting" v-for="(meeting, key) in group.meeting" v-bind:key="key">
          <dl>
            <dt class="summary_content" v-bind:class="{summary_open_list}"
              @click="summary_select_group(key)">
              {{ meeting.day }}
            </dt>
            <div v-show="summary_open_list[key]">
                <textarea class="content" v-show="edit_flag[key]" cols="50">{{ meeting.content }}</textarea>
                <p class="content read-only" v-show="edit_flag[key] == false">{{ meeting.content }}</p>
                <button v-on:click="get_summary(key)">読み込み</button>
                <button v-on:click="save_summary(key)">保存</button>
                <button v-on:click="edit_summary(key)">編集</button>
            </div>
          </dl>
        </div>
      </dd>
    </dl>
  </div>
</template>

<script>
export default {
  props:['group'],
  data() {
      return {
        group_flag:false,
        summary_open_list:[],
        edit_flag:[],
        member_select:[]
      };
  },
  mounted:function() {
    for(let index = 0; index < this.group.meeting.length; index++) {
      this.summary_open_list.push(false)
      this.edit_flag.push(false)
    }
    for(let index = 0; index < this.group.member.length; index++) {
      this.member_select.push(false)
    }
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
      summary_select_group: function(key) {
          this.summary_open_list.splice(key, 1, !this.summary_open_list[key])
          console.log(this.summary_open_list)
      },
      get_summary: function(key) {
          console.log("get ",key)
      },
      save_summary: function(key) {
          console.log("save ",key)
      },
      edit_summary: function(key) {
        this.edit_flag.splice(key, 1, !this.edit_flag[key])
      }
  }
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