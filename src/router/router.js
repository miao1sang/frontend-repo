// 从 vue-router 中引入 createRouter, createWebHashHistory 方法
import { createRouter, createWebHashHistory } from 'vue-router'


// 定义一个路由数组，统一管理路由
const routes = [
    {
        path: '/',
        redirect:'/login'
    },
    //登录
    {
        path: '/login',
        name: 'login',
        component:() => import("../components/login.vue"),
    },
    //注册
    {
        path: '/sign',
        name: 'sign',
        component:() => import("../components/sign.vue"),
    },
    {
        path: '/home', // 路由地址：首页
        name: 'home', // 命名路由
        redirect:'/home/list',
        component:() => import("../components/index.vue"),
        children:[

            //首页
            {
                path: '/home/list',
                name: 'list',
                component:() => import("../components/list.vue"),
            },
            //作者详情
            {
                path: '/home/authList',
                name: 'authList',
                component:() => import("../components/auth-list.vue"),
            },
            //新增博客
            {
                path: '/home/add',
                name: 'add',
                component:() => import("../components/add-blog.vue"),
            },
        ]
    },
    //详情
    {
        path: '/cardDetail',
        name: 'cardDetail',
        component:() => import("../components/card-detail.vue"),
    },
]

// 使用 createRouter 方法创建路由实例
const router = createRouter({
    history: createWebHashHistory(), // 指定 history 模式，这里采用的是 hash 模式
    routes // 定义路由数组，相当于 routes: routes 的简写模式
})

// ES6 模块导出语句，它用于将 router 对象导出，以便其他文件可以导入和使用这个对象
export default router