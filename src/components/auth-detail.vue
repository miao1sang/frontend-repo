<template>
    <div style="width: 350px;height: 150px;">
        <img-upload  v-model="lastImg" v-if="!id"></img-upload>
        <el-avatar
            v-else
            :src="imgSrc+info.img"
            shape="square" :size="150" fit="fill"
        />

    </div>
   <el-form>
       <el-row>
           <el-col :span="12">
               <el-form-item label="Username：">
                  <span>{{info.username}}</span>
               </el-form-item>
           </el-col>
           <el-col :span="12">
               <el-form-item label="account number：">
                   <span>{{info.accountNumber}}</span>
               </el-form-item>
           </el-col>
       </el-row>
       <el-row>
           <el-col :span="12">
               <el-form-item label="IP address：">
                   <span>United Kingdom</span>
               </el-form-item>
           </el-col>
           <el-col :span="12"  v-if="!id">
               <el-form-item label="Password：">
                   <el-input v-model="info.password"></el-input>
               </el-form-item>
           </el-col>

       </el-row>
       <el-row>
           <el-col :span="12">
               <el-form-item label="Email：">
                   <span>{{info.email}}</span>
               </el-form-item>
           </el-col>
           <el-col :span="12">
               <el-form-item label="SignTime：">
                   <span>{{info.signDate}}</span>
               </el-form-item>
           </el-col>
       </el-row>
       <el-row>
           <el-col :span="12">
               <el-form-item label="Total likes received：">
                   <span>{{info.likes}}</span>
               </el-form-item>
           </el-col>
           <el-col :span="12">
               <el-form-item label="Total number of comments received：">
                   <span>{{info.comments}}</span>
               </el-form-item>
           </el-col>
       </el-row>
   </el-form>
    <div style="margin-left: 100px" v-if="!id">
        <el-button  :loading="loading" @click="toUpdate">Update</el-button>
    </div>
</template>

<script setup>
import {reactive, ref, toRefs,watch} from "vue";
import {userDetail,userUpdate} from "@/api/index.js";
import {useRoute} from 'vue-router'
import ImgUpload from '@/components/list/upload.vue'
import {formatDate} from '@/utils/parseGet.js'
const imgSrc=ref('http://47.99.78.237:8001')
import { ElMessage } from 'element-plus'
const route=useRoute()
const props=defineProps({
    id:[String,Number],
})
const {id}=toRefs(props)
const info=reactive({
    username:'',
    accountNumber:'',
    password:'',
    email:'',
    likes:'',
    comments:'',
    img:'',
    signDate:''
})
const loading=ref(false)
const lastImg=ref([])
watch(()=>route,newVal=>{
    const lastParams=id.value || localStorage.getItem('uid')
    userDetail(`/?u_id=${lastParams}`).then(res=>{
        let obj=res[0]
        info.username=obj.u_name
        info.accountNumber=obj.u_id
        info.password=obj.u_password
        info.email=obj.u_mail
        info.signDate=formatDate(new Date(obj.registration_date))
        info.likes=obj.total_likes
        info.comments=obj.total_comments
        info.img=obj.avatar

        lastImg.value=[{
            name:'file.png',
            url:imgSrc.value+info.img
        }]
    })

},{deep:true,immediate:true})

const toUpdate=()=>{
    if (!info.password){
        ElMessage.error({
            message: 'password is required',
            type: 'error',
        })
        return
    }
    if (lastImg.value.length===0){
        ElMessage.error({
            message: 'img is required',
            type: 'error',
        })
        return
    }
    loading.value=true
    const lastParams=id.value || localStorage.getItem('uid')
    let formData = new FormData()
    if (lastImg.value[0].raw){
        formData.append('avatar', lastImg.value[0].raw)// 传文件
    }
    formData.append('u_password', info.password)

    userUpdate(`${lastParams}/`,formData).then(res=>{
        ElMessage.success({
            message: 'update success',
            type: 'success',
        })
    }).finally(()=>{
        loading.value=false
    })

}




</script>

<style scoped lang="less"></style>