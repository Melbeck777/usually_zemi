<template>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css" integrity="sha512-KfkfwYDsLkIlwQp6LFnl8zNdLGxu9YAA1QvwINks4PhcElQSvqcyVLLD9aMhXd13uQjoXtEKNosOWaZqXgel0g==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <div>
        <Header/>
        <div class="container">
            <router-view @loginSuccess="loginSuccess"></router-view>
        </div>
        <Footer/>
    </div>

</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
export default {
    name: 'App',
    data() {
        return {
            userLogin:false,
        }
    },
    components: {
        Header,
        Footer
    },
    methods:{
        loginSuccess() {
            this.userLogin = true;
        },
        logout() {
            this.userLogin = false;
        }
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
    /* height: 100vh; */
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
        margin-bottom: 50px;
    }
}

@media (min-width: 1024px) {
    .container {
        width: 1100px;
        margin-bottom: 80px;
    }
}
</style>