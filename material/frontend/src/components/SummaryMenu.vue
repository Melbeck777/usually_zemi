<template>
    <div class="summary_menu">
        <form>
            <div class="form-group year">
                <p>年度</p>
                <input type="number" v-model="year"/>
                <button v-on:click="go">Go</button>
            </div>
        </form>
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
    created() {
        if (date.getMonth() < 4) {
            this.year = date.getFullYear()-1;
        }
    },
    methods:{
        go:function() {
            this.$router.push({path:`/summary/${this.year}`})
            // this.$router.push({path:`/summary/${this.year}`})
        }
    }
}
</script>


<style>
.form-group {
    color:black;
    font-size: 30px;
    text-align: center;
    margin:10px;
}
input  {
    max-width: 100px;
    text-align: center;
}
</style>