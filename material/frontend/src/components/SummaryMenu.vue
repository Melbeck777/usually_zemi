<template>
    <div class="summary_menu">
        <form>
            <div class="form-group year">
                <label>年度</label>
                <input
                    type="number"
                    :value="year"
                    v-model="year"/>
            </div>
            
        </form>
        <button v-on:click="go">Go</button>
    </div>
</template>

<script>
let date = new Date();
export default {
    data() {
        return  {
            year:date.getFullYear()
        }
    },
    methods:{
        go:function() {
            this.$router.push({path:`/summary/${this.year}`})
        }
    }
}
</script>


<style>
.form-group {
    color:black;
    font-size: 20px;
    text-align: center;
}
input  {
    max-width: 100px;
    text-align: center;
}
</style>