<template>
    <div class="select">
        <table>
            <tr>
                <td><label>研究室</label></td>
                
                <td>
                    <select v-model="selects.lab" class="select-lab">
                        <option disabled value="">研究室</option>
                        <option v-for="(data, key) in lab_group"
                            v-bind:value="data.lab"
                            v-bind:key="key">
                            {{ data.lab }}
                        </option>
                    </select>
                </td>
                <td><button v-on:click="get_group_list">Reload</button></td>
            </tr>
            <tr>
                <td><label>研究班</label></td>
                <td>
                    <select v-model="selects.group">
                        <option disabled value="">研究班</option>
                        <option v-for="(group, key) in group_list" 
                            v-bind:value="group"
                            v-bind:key="key">
                            {{ group }}
                        </option>
                    </select>
                </td>
                <td><button v-on:click="decide">Decide</button></td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            selects:{
                lab:"",
                group:""
            },
            group_list:[],
            lab_group:[],
            res_data:{},
        }
    },
    created() {
        axios.get(this.$route.path).then((result) => {
            this.lab_group = JSON.parse(JSON.stringify(result.data))
        })
    },
    methods:{
        get_group_list:function() {
            for(let index = 0; index < this.lab_group.length; index++) {
                if (this.lab_group[index].lab === this.selects.lab) {
                    this.group_list = this.lab_group[index].group
                    break
                }
            }
        },
        decide:function() {
            let url = `/summary/${this.$route.params.year}/${this.selects.lab}/${this.selects.group}`
            this.$router.push({path:url})
        }
    }
}
</script>


<style>
table {
    margin:auto;
}
td {
    margin:10px;
    padding:5px;
    font-size: 20px;
}
html {
    background-color: #24eff2;
}
</style>