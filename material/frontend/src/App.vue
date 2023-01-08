<template>
    <div>
        <Header />
        <div class="container">
            <router-view></router-view>
        </div>
        <Footer />
    </div>

</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
export default {
    name: 'App',
    components: {
        Header,
        Footer
    }
}
</script>

<style>
* {
    margin: 0;
    padding: 0;
}

body {
    /* background: linear-gradient(320deg, #ca8585, #9785ca); */
    line-height: 1.5;
    font-size: 14px;
    margin-top: 110px;
    height: 100vh;
}

.container {
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
}

@media (min-width: 768px) {
    .container {
        width: 700px;
        padding: 0;
        margin: 0 auto;
    }
}

@media (min-width: 1024px) {
    .container {
        width: 980px;
    }
}
</style>