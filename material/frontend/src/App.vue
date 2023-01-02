<template>
  <div v-for="(group_data, key) in group_data_list" v-bind:key="key">
    <SummaryShow :group="group_data"/>
  </div>
  
</template>

<script>
import SummaryShow from './components/SummaryShow.vue'

export default {
  name: 'App',
  components: {
    SummaryShow
  },
  data() {
    return {
      group_data_list:[
        {
          name:"group 1",
          member:["河野", "金田", "青井", "大友"],
          meeting:[
            {
              day:"2022/12/7",
              content:"河野\n\t今日は実験をした"
            },
            {
              day:"2022/12/9",
              content:"河野\n\t実験系の再構築をした"
            },
            {
              day:"2022/12/12",
              content:"河野\n\t実験結果をまとめた"
            },
          ]
        },
      ]
    }
  }
}
</script>
