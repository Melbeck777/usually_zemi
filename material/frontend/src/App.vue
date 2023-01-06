<template>
  <div class="background">
    <router-view></router-view>
  </div>
  
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
body {
  height: 100vh;
  background: linear-gradient(320deg, #ca8585, #9785ca);
  color: white;
}
</style>