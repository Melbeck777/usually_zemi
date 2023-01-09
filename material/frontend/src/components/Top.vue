<template>
    <h1 class="top_view">Enjoy<br/>Your<br/>Research<br/>Life...</h1>
</template>

<script>
export default {
    methods:{
        summary:function() {
            console.log(this.$router)
            this.$router.push({name:'summary_menu'})
        },
        index:function() {
            console.log('Next development function...')
        }
    }
}
</script>

<style>
.top_view {
    font-size: 100px;
    margin: auto;
    text-align: center;
    width: 100%;
    height: 600px;
    padding: 35px;
    background:linear-gradient(340deg, #3fc3da, #b7c9fc);
}
</style>