<template>
    <!-- 页面的所有内容 -->
    <div class="container">
        <div class="deleteBlog" v-if="isMyBlog">
            <el-button size="large" style="width: 100px" type="danger" @click="deleteBlog">DeleteBlog</el-button>
        </div>
        <div class="close" @click="back">
            <div style="margin-right: 5px;font-size: 20px">close</div>
            <div class="iconfont icon-close"></div>

        </div>
        <div class="post-image">
            <!-- 使用相对路径引用帖子图片 -->
            <img :src="imgSrc+obj.image" style="height: 100%;width: 100%;border-radius: 8px" alt="帖子图片">
        </div>
        <div class="post-details">
            <div class="user-info">
                <!-- 使用相对路径引用默认头像 -->
                <img :src="imgSrc+obj.avatar" alt="用户头像" class="avatar">
                <span class="id">{{obj.u_name}}</span>
            </div>
            <h1 class="title">{{obj.title}}</h1>
            <p class="text">{{obj.content}}</p>
            <span class="published-date">发布日期:{{formatDate(new Date(obj.created_time))}}</span>
            <hr > <!-- 在这里添加横线 -->
            <span class="comment-count">评论数：{{commentList.length}}</span>

            <div class="comments-section">
                <!-- 第一条评论 -->
                <div class="comment" v-for="(item,index) in commentList" :key="index">
                    <!-- 使用默认头像 -->
                    <img  :src="imgSrc+item.avatar" alt="评论者头像" class="avatar comment-avatar">
                    <div class="comment-content">
                        <span class="comment-id">
                            <span>评论者ID：{{item.u_name}}</span>
                          <span >
                              <el-button @click="deleteComments(item.c_id)" type="danger" v-if="isMyComments(item.u_id)">Delete</el-button>
                          </span>
                        </span>

                        <p class="comment-text">评论内容：{{item.content}}</p>
                        <span class="comment-date">评论日期:{{formatDate(new Date(item.created_time))}}</span>
                    </div>
                </div>
                <!-- 更多评论 -->
            </div>


            <div class="interaction-bar">
                <el-button  type="danger" class="comment-button" @click="isShow=true">click to commit</el-button>
                <!-- 互动按钮 -->
                <div class="actions" >
                    <div >
                        <div class="iconfont icon-xihuan" :style="{color:isLike?'red':'black'}" style="display: flex;align-items: center;cursor: pointer" @click="likes">
                            <span style="margin-left: 5px;color: black">{{obj.likes}}</span>
                        </div>
                        <div>Like</div>
                    </div>
                    <div >
                        <div class="iconfont icon-shoucang" :style="{color:isSave?'yellow':'black'}" style="display: flex;align-items: center;cursor: pointer" @click="save">
                            <span style="margin-left: 5px;color: black">{{obj.views}}</span>
                        </div>
                        <div>save</div>
                    </div>
                    <div >
                        <div class="iconfont icon-pinglun" style="display: flex;align-items: center">
                            <span style="margin-left: 5px;cursor: pointer">{{obj.comments}}</span></div>
                        <div>comments</div>
                    </div>
                </div>
            </div>

            <commit v-if="isShow" @close="isShow=false"  :blogId="obj.blog_id" @flush="getComment(true)"></commit>
        </div>
    </div>
</template>

<script setup>
import {ref,onMounted} from 'vue'
import Commit from '@/components/commit.vue'
import {useRouter,useRoute} from 'vue-router'
import {getCommentById,delBlog,delComment,updateBlog} from '@/api/index.js'
import {formatDate} from '@/utils/parseGet.js'
const isShow=ref(false)
const router=useRouter()
const route=useRoute()
import { ElMessage } from 'element-plus'
const imgSrc=ref('http://47.99.78.237:8001')
const obj=ref(JSON.parse(route.query.item))
const commentList=ref([])
function getComment(isAdd){
    let blogId=obj.value.blog_id

    getCommentById(`?blog_id=${blogId}`).then(res=>{
        commentList.value=res
    })

    if (isAdd){
        obj.value.comments=obj.value.comments+1
    }
}
getComment()


const isMyBlog=ref(false)

onMounted(()=>{
    isMyBlog.value= localStorage.getItem('isSuper')==='true' || localStorage.getItem('uid')===String(obj.value.u_id)
})
function isMyComments(id){
    return localStorage.getItem('isSuper')==='true' || localStorage.getItem('uid')===String(id)
}

//删除博客
function deleteBlog(){
    delBlog(`${obj.value.blog_id}`).then(()=>{
        ElMessage.success({
            message: 'delete blog success',
            type: 'success',
        })
        router.back()
    })
}

//删除评论
function deleteComments(id){
    let blogId=obj.value.blog_id
    delComment(`${id}/?blog_id=${blogId}`).then(()=>{
        ElMessage.success({
            message: 'delete comments success',
            type: 'success',
        })
        obj.value.comments=obj.value.comments-1
        getComment()
    })
}


const isLike=ref(false)
const isSave=ref(false)
let likesArr=obj.value.likes_user
let saveArr=obj.value.favorite_user
function  init(){
    let uid=localStorage.getItem('uid')
    if (likesArr){
        likesArr=likesArr.split(',')
        isLike.value=likesArr.some(v=>v===uid)
    }
    if (saveArr){
        saveArr=saveArr.split(',')
        isSave.value=saveArr.some(v=>v===uid)
    }
}
init()

//喜欢
const likeLock=ref(false)
function likes(){
    if (likeLock.value){
        return
    }
    likeLock.value=true
    let data={
        u_id:obj.value.u_id,
        likes:'',
        likes_user:''
    }
    let like=obj.value.likes_user
    if (!like){
        like=[]
    }else {
        like=String(like).split(',')
    }
   if (isLike.value){
       obj.value.likes=obj.value.likes-1
       data.likes_user= like.filter(v=>v!==String(localStorage.getItem('uid'))).join(',') || null
   }else {
       obj.value.likes=obj.value.likes-1+2
       like.push(localStorage.getItem('uid'))
       data.likes_user=like.join(',')
   }
   data.likes= obj.value.likes

    updateBlog(obj.value.blog_id,data).then(()=>{
        isLike.value=!isLike.value
        likeLock.value=false
    })
}
//收藏
const saveLock=ref(false)
function save(){
    if (saveLock.value){
        return
    }
    saveLock.value=true
    let data={
        u_id:obj.value.u_id,
        views:'',
        favorite_user:''
    }
    let save=obj.value.favorite_user
    if (!save){
        save=[]
    }else {
        save=String(save).split(',')
    }

    if (isSave.value){
        obj.value.views=obj.value.views-1
        data.favorite_user=save.filter(v=>v!==String(localStorage.getItem('uid'))).join(',') || null
    }else {
        obj.value.views=obj.value.views-1+2
        save.push(localStorage.getItem('uid'))
        data.favorite_user=save.join(',')
    }
    data.views= obj.value.views
    updateBlog(obj.value.blog_id,data).then(()=>{
        isSave.value=!isSave.value
        saveLock.value=false
    })
}


//返回
const back=()=>{
    router.back()
}

</script>


<style scoped lang="less">
@import url("@/assets/font/iconfont.css");
/* styles.css */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}



.container {
    display: flex;
    width: 950px; /* 或者根据设计需求调整 */
    height: 600px;
    border: 2px solid black; /* 添加黑色边框 */
    border-radius: 8px; /* 圆角边框 */
    margin: 50px auto; /* 上下边距20px，左右自动居中 */
    background: white; /* 设置背景颜色，以防您的<body>有不同的背景颜色 */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 可选：添加一些阴影效果 */
    box-sizing: border-box; /* 确保边框不会增加元素的宽度 */
    position: relative;
}
.post-image {
    flex: 0 0 55%; /* 设置图片部分宽度 */
    display: flex;
    align-items: flex-start; /* 对齐到顶部，确保图片在顶部开始 */
}

.post-image img {
    width: 100%;
    height: auto;
    object-fit: cover; /* 如果需要，确保图片覆盖整个区域 */
}

.post-details {
    display: flex;
    flex-direction: column;
    justify-content: space-between; /* 这将分散对齐子元素，推动交互栏到底部 */
    flex: 1;
    padding: 20px;
}

/* 确保交互栏被推到底部 */
.interaction-bar {
    margin-top: auto; /* 自动将所有额外空间留在上方，将元素推到底部 */

}

.user-info {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.user-info .avatar {
    width: 50px; /* 调整头像的尺寸 */
    height: 50px;
    margin-right: 10px;
    border-radius: 50%; /* 圆形头像 */
}

.title {
    font-size: 25px;
    margin-bottom: 10px;
}

.text {
    overflow: auto;
    height: 300px;
    margin-bottom: 20px;
}

.published-date, .comment-count {
    display: block;
    margin-bottom: 10px;
}


.comments-section {
    width: 100%;
    display: flex;
    flex-direction: column; /* 使评论竖直排列 */
    margin-top: 20px; /* 在评论数和第一条评论之间添加一些空间 */
    height: 300px;
    overflow: auto;
}

.comment {
    display: flex;
    align-items: flex-start; /* 保证内容顶部对齐 */
    margin-bottom: 20px; /* 每条评论间的间距 */
}

.avatar.comment-avatar {
    width: 50px; /* 头像大小 */
    height: 50px;
    border-radius: 50%;
    margin-right: 15px; /* 头像与内容之间的间距 */
}

.iconfont{
    font-size: 30px;
}

.comment-content {
    display: flex;
    flex-direction: column; /* 评论详情内部竖直排列 */
}

.comment-id, .comment-text, .comment-date {
    margin-bottom: 5px; /* 细节之间的间距 */
}


.interaction-bar {
    display: flex;
    margin-top: 20px; /* 在评论区和互动栏之间添加一些空间 */
}

.comment-id {
    width: 100%;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
}

.comment-date {
    margin-left: 50px; /* 让评论日期靠右显示 */
}

.comment-button {
    padding: 10px;
}

body, html {
    height: 100%;
    overflow-y: scroll; /* 总是显示垂直滚动条 */
}

.actions {
    display: flex;
    flex: 1;

    &>div{
       margin-left: 30px;

     }
    & span{
        font-size: 16px;
    }
}

.actions span {
    cursor: pointer;
    margin-right: 10px; /* 缩短span元素之间的距离 */
}

.actions span:last-child {
    margin-right: 0; /* 最后一个span元素不需要右边距 */
}
.close{
    position: absolute;
    cursor: pointer;
    right: -100px;
    top: 0;
    display: flex;
    align-items: center;
}
.deleteBlog{
    position: absolute;
    top: -50px;
    left: 50%;
    transform: translateX(-50%);

}

</style>