<template>
    <header>
        <div class="wrapper">
            <h1 class="index" @click="select_index">
                Index
            </h1>
            <h1 class="summary" @click="select_summary">
                Summary
            </h1>
        </div>
    </header>
</template>

<script>
export default {
    methods: {
        select_index() {
            console.log("index")
        },
        select_summary() {
            this.$router.push({ name: 'summary_menu' })
        }
    }
}
</script>

<style>
header {
    position: fixed;
    top: 0;
    left: 0;
    background-color:rgb(25, 215, 41);
    color: #fff;
    height: 90px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap:10px;
    grid-template-rows: 1fr;
    margin-bottom: 80px;
    margin-left: 0;
    margin-right: 0;
    width: 100%;
    z-index: 1;
}
.wrapper {
    overflow: hidden;
}
header>* {
    grid-row: 1;
    grid-column: 2;
}
h1 {
    align-self: center;
    font-size: 20px;
    font-weight: normal;
    border: #fff solid 0.1em;
    padding:10px;
    margin: 20px;
    display: inline-block;
    width: 110px;
}
@media (min-width: 768px) {
    header {
        grid-template-columns: 1fr 700px 1fr;
    }
}

@media (min-width: 1024px) {
    header {
        grid-template-columns: 1fr 980px 1fr;
    }
}
</style>