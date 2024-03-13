<template>
     <div style="width: 200px">
         <div class="title">
             <img style="width: 100%;height: 100%" src="../assets/logo.webp">
         </div>
         <el-menu
             active-text-color="#ffd04b"
             background-color="gray"
             class="el-menu-vertical-demo"
             :default-active="activePath"
             text-color="#fff"
             :router="true"
         >
             <el-menu-item index="/home/list">
                 <el-icon><icon-menu /></el-icon>
                 <span>Community</span>
             </el-menu-item>
             <el-menu-item index="/home/add">
                 <el-icon><document /></el-icon>
                 <span>Publish</span>
             </el-menu-item>
             <el-menu-item index="4">
                 <el-icon><setting /></el-icon>
                 <span>Notification</span>
             </el-menu-item>
             <el-menu-item index="/home/authList">
                 <el-icon><icon-menu /></el-icon>
                 <span>Your</span>
             </el-menu-item>
             <div class="footer">
                 <div>
                     <div class="iconfont icon-wenhao" style="font-size: 25px"></div>
                     <el-button @click="toHelp">Help</el-button>
                 </div>
                 <div style="margin-top: 10px">
                     <div class="iconfont icon-gengduo" style="font-size: 25px"></div>
                     <el-button style="margin-left: 13px">More</el-button>
                 </div>
             </div>
         </el-menu>
     </div>
     <help v-if="isShow" @close="isShow=false"></help>
</template>

<script setup>
import Help from '@/components/help.vue'
import {ref,watch} from 'vue'
import {
    Document,
    Menu as IconMenu,
    Setting,
} from '@element-plus/icons-vue'
import {useRoute} from 'vue-router'
const activePath=ref('/')
const route=useRoute()

watch(()=>route,newVal=>{
    activePath.value= newVal.fullPath
},{deep:true,immediate:true})


const isShow=ref(false)
const toHelp=()=>{
    isShow.value=true
}


</script>

<style lang="less" scoped>
@import url("@/assets/font/iconfont.css");
.title{
    height: 80px;
}
.el-menu-vertical-demo{
    height: calc(100% - 80px);
    position: relative;

    .footer{
        position: absolute;
        bottom: 10px;
        left: 10px;

        &>div{
            width: 100px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
    }
}
</style>
