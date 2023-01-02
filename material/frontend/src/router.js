import {createRouter, createWebHistory} from 'vue-router'
import SummaryMenu from './components/SummaryMenu.vue'
import SummaryShow from './components/SummaryShow.vue'
import Top from './components/Top.vue'

const routes = [
    {
        path:'/',
        name:'top',
        component:Top
    },
    {
        path:'/summary/menu',
        name:'summary',
        component:SummaryMenu
    },
    {
        path:'/summary/:year',
        name:'summary_show',
        component:SummaryShow
    }
]

const router = createRouter({
    history:createWebHistory(),
    routes:routes
})

export default router