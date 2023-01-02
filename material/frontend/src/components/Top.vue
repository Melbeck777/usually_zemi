<template>
    <div id="menu">
        <button v-on:click="summary">Summary</button>
        <button v-on:click="index">Index</button>
    </div>
    <router-view/>
</template>

<script>
export default {
    methods:{
        summary:function() {
            console.log(this.$router)
            this.$router.push('/summary/menu')
        },
        index:function() {
            console.log('Next development function...')
        }
    }
}
</script>