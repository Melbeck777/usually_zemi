import {createRouter, createWebHistory} from 'vue-router'
import SummaryMenu from './components/SummaryMenu.vue'
import WeeklyShow from './components/WeeklyShow.vue'
import SummaryShow from './components/SummaryShow.vue'
import SelectGroup from './components/SelectGroup.vue'
import Top from './components/Top.vue'
import MonthlyShow from './components/MonthlyShow.vue'

const routes = [
    {
        path:'/',
        name:'top',
        component:Top
    },
    {
        path:'/summary',
        name:'summary_menu',
        component:SelectGroup
    },
    {
        path:'/summary/:year/:lab/:group',
        name:'summary_show',
        component:SummaryShow,
        props:true,
    },
    {
        path:'/summary/:year/:lab/:group/weekly',
        name:'weekly_summary_show',
        component:WeeklyShow
    },
    {
        path:'/summary/:year/:lab/:group/monthly',
        name:'monthly_summary_show',
        component:MonthlyShow,
        props:true
    }
]

const router = createRouter({
    history:createWebHistory(),
    routes:routes
})

export default router