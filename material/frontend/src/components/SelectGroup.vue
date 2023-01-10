<template>
    <div class="select container">
        <table>
            <tr>
                <td>
                    <select v-model="selects.lab" class="select-lab">
                        <option disabled value="">研究室</option>
                        <option v-for="(data, key) in lab_group" v-bind:value="data.lab" v-bind:key="key">
                            {{ data.lab }}
                        </option>
                    </select>
                </td>
            </tr>
            <tr>
                <td>
                    <select v-model="selects.group">
                        <option disabled value="">研究班</option>
                        <option v-for="(group, key) in group_list" v-bind:value="group" v-bind:key="key">
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
            lab_group: [],
            res_data: {},
            reference_folder: ".",
        }
    },
    created() {
        axios.get(this.$route.path).then((result) => {
            this.lab_group = JSON.parse(JSON.stringify(result.data))
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

input {
    width: 100px;
}
</style>