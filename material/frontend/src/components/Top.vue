<template>
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