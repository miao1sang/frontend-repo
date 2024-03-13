<template>
    <ul class="list"  v-infinite-scroll="load" infinite-scroll-distance="1" :infinite-scroll-immediate="false">
            <li  style="padding:  40px 30px;box-sizing: border-box;" v-for="(item,index) in list" :key="index">
                <div class="card"  >
                    <div class="img" @click="toDetail(item)">
                        <img style="width: 100%;height: 100%" :src="imgSrc+item.image">
                    </div>
                    <div>
                        <div class="title">{{item.title}}</div>
                        <div class="footer">
                            <div style="cursor: pointer;" @click="toAuth(item.u_id)">{{item.u_name}}</div>
                            <div >{{item.likes}}</div>
                        </div>
                    </div>
                </div>
            </li>
        <div  class="loading">
            <p v-if="next">Loading...</p>
            <p v-else>No more</p>
        </div>
    </ul>
</template>


<script setup>
import {toRefs,onMounted,reactive,ref,watch} from 'vue'
import {useRouter,useRoute} from 'vue-router'
const router=useRouter()
const route=useRoute()
import {blogList} from '@/api/index.js'
const imgSrc=ref('http://47.99.78.237:8001')
import {parseString} from '@/utils/parseGet.js'
//高度自适应
const props=defineProps({
    boxHeight:[String,Number],
    id:[String,Number]
})
const {boxHeight,id}=toRefs(props)
onMounted(()=>{
    document.documentElement.style.setProperty('--height', `${boxHeight.value}px`)
})
const list=ref([])
const filter=reactive({
    page:1,//当前页
    size:10,//每页大小
    u_id:id.value,//作者id
})
//是否有下一页
const next=ref(true)
const fetch=()=>{
    blogList(parseString(filter)).then(res=>{
        next.value=Boolean(res.next)
        list.value.push(...res.data)
    })
}
watch(()=>route,newVal=>{
    filter.u_id=id.value
    list.value=[]
    fetch()
},{deep:true})


fetch()
//外部搜索调用，重置page为1
const search=(callback)=>{
    callback(filter,list,fetch)
}


//加载更多
const load = () => {
    if (!next.value){
        return
    }
    filter.page++
    fetch()
}

//作者详情页
const toAuth=(id)=>{
    router.push({
        name:'authList',
        query:{
            id
        }
    })
}
//帖子详情
const toDetail=((item)=>{
    router.push({
        name:'cardDetail',
        query:{
           item:JSON.stringify(item)
        }
    })
})


defineExpose({
    search
})
</script>


<style  lang="less" scoped>
.text() {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.list{
    width: 85%;
    height: calc(95% - var(--height));
    overflow: auto;
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    padding: 0;
    margin: 0 30px 0 30px;



    .card{
        width: 200px;
        height: auto;
        .img{
            background: blue;
            width: 100%;
            height: 200px;
            cursor: pointer;
        }
        .title{
            border:1px solid gray;
            border-bottom: none;
            text-align: center;
            height: 50px;
            line-height: 50px;
            .text()
        }
        .footer{
            display: flex;
            align-items: center;

            &>div{
                width: 50%;
                height: 50px;
                line-height: 50px;
                text-align: center;
                border:1px solid gray;
                .text()
            }
            &>div:nth-child(1){
                border-right:none;
            }
        }
    }

    .loading{
       width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
}


.list::-webkit-scrollbar {
    width: 0 !important;

}



</style>