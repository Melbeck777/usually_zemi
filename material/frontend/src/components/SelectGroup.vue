<template>
    <div class="select container">
        <div v-for="(data, data_key) in lab_group_list" :key="data_key">
            <p class="year" @click="select_year(data_key)">{{ data.year }}</p>
            <div v-show="year_select[data_key]">
                <div class="lab_wrapper" v-for="(lab, lab_key) in data.lab_group">
                    <p class="lab" @click="select_lab(data_key,lab_key)">{{ lab.lab.substring(0,2) }}</p>
                    <div v-show="lab_select[data_key][lab_key]" v-for="(group, group_key) in lab.group" :key="group_key">
                        <p class="group"  @click="select_group(data.year,lab.lab,group)">
                            {{ group }}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { watch } from 'vue'

export default {
    props: ["year"],
    data() {
        return {
            selects: {
                lab: "",
                group: ""
            },
            group_list: [],
            lab_group_list: [],
            year_select:[],
            lab_select:[]
        }
    },
    created() {
        axios.get(this.$route.path).then((result) => {
            var obj = JSON.parse(JSON.stringify(result.data))
            console.log("obj, ",obj)
            this.lab_group_list = obj
            console.log("obj.length, ",obj.length)
            for(let i = 0; i < obj.length; i++) {
                this.year_select.push(false)
                this.lab_select.push([])
                console.log("obj[].lab_group.length, ",obj[i].lab_group.length)
                for(let j = 0; j < obj[i].lab_group.length; j++) {
                    this.lab_select[i].push(false)
                }
            }
        })
    },
    methods: {
        get_group_list() {
            for (let index = 0; index < this.lab_group.length; index++) {
                if (this.lab_group[index].lab === this.selects.lab) {
                    this.group_list = this.lab_group[index].group
                    break
                }
            }
        },
        select_year(year_key){
            this.year_select.splice(year_key, 1, !this.year_select[year_key])
        },
        select_lab(year_key, lab_key){
            this.lab_select[year_key].splice(lab_key, 1, !this.lab_select[year_key][lab_key])
        },
        select_group(year, lab, group){
            this.$router.push({name:"weekly_summary_show", params: { year: year, lab: lab, group: group }})
        },
        decide() {
            console.log(this.year)
            this.$router.push({ name: 'weekly_summary_show', params: { year: this.year, lab: this.selects.lab, group: this.selects.group } })
        }
    },
    watch: {
        'selects.lab': function(new_val, old_val) {
            console.log(old_val, new_val)
            for (let index = 0; index < this.lab_group.length; index++) {
                if (this.lab_group[index].lab === this.selects.lab) {
                    this.group_list = this.lab_group[index].group
                    break
                }
            }
        }
    }
}
</script>


<style>
table {
    margin: auto;
}

td {
    margin: 10px;
    padding: 5px;
    font-size: 25px;
    height: 40px;
    max-width: 400px;
}
.year {
    font-size: 30px;
    text-align: center;
    width: 200px;
    height: 60px;
    background:rgba(233,200,233, 0.4);
}
.lab {
    font-size: 30px;
    text-align: center;
    width: 200px;
    height: 50px;
    background:rgba(0,230,230, 0.4);
    border-radius: 10px;
    margin-left: 30px;
    margin-top: 10px;
    margin-bottom: 10px;
}
.lab_wrapper{
    margin: 10px;
}
.group {
    font-size: 25px;
    text-align: center;
    width: 250px;
    height: 40px;
    background:rgba(0,220,0, 0.4);
    border-radius: 10px;
    margin-left: 60px;
    margin-top: 10px;
}
</style>