<template>
    <div class="login">
        <div class="title">Sign</div>
        <div class="box">
            <div>
                <div style="width: 200px;height: 230px">
                    <img  style="width: 100%;height: 100%" src="../assets/myqrcode.jpg">
                </div>
            </div>
            <div>
                <div>
                    <el-form :rules="rules" :label-width="130" :model="info" ref="box">
                        <el-form-item label="email" prop="email">
                            <el-input  v-model="info.email"></el-input>
                        </el-form-item>
                        <el-form-item label="Username" prop="username">
                            <el-input v-model="info.username"></el-input>
                        </el-form-item>
                        <el-form-item label="Password" prop="password">
                            <el-input type="password"  show-password v-model="info.password"></el-input>
                        </el-form-item>
                        <el-form-item label="password again" prop="passwordAgain">
                            <el-input type="password" show-password v-model="info.passwordAgain"></el-input>
                        </el-form-item>


                    </el-form>


                    <div class="commit">
                        <el-button :loading="loading" style="width: 200px; height: 50px" @click="toSign(box)">Continue</el-button>
                    </div>
                </div>
            </div>


        </div>
    </div>
</template>


<script setup>
import {sign} from '@/api/index.js'
import { ElMessage } from 'element-plus'
import {useRouter} from 'vue-router'
const router=useRouter()
//校验
import {reactive,ref} from "vue";

const loading=ref(false)
const info=reactive({
    username:'',
    password:'',
    passwordAgain:'',
    email:''
})

const validatePass=(rule,value,callback)=>{
    if (!value){
        callback(new Error('password is required'))
    }else if (info.password!==info.passwordAgain){
       callback(new Error('Two passwords do not match'))
    }else {
        callback()
    }
}

const validateEmail=(rule,value,callback)=>{
    if (!value){
        return callback(new Error('email is required'));
    }
    if ((value.length > 128) || (value.length < 6)) {
        return callback(new Error('length error'));
    }
    var format = /^[A-Za-z0-9+]+[A-Za-z0-9\.\_\-+]*@([A-Za-z0-9\-]+\.)+[A-Za-z0-9]+$/;
    if (!value.match(format)) {
        return callback(new Error('Incorrect format error'));
    }
    return callback();
}

const rules=reactive({
    username:[{required:true,trigger: 'change',}],
    password:[{required:true,trigger: 'change',}],
    passwordAgain:[{validator: validatePass,trigger: 'change',required:true}],
    email:[{validator:validateEmail,trigger: 'change',required:true}],
})

//提交
const box=ref(null)
const toSign=(box)=>{
    box.validate().then(()=>{
        loading.value=true
         let obj={
             u_name:info.username,
             u_password:info.password,
             u_mail:info.email,
             is_super:false
         }
        return  sign(obj)
    }).then(()=>{
        ElMessage.success({
            message: 'Congratulations, registration successful',
            type: 'success',
        })
        setTimeout(()=>{
            router.push({
                name:'login'
            })
        },2000)
    }).catch(()=>{
        ElMessage.error({
            message: 'Please do not register again',
            type: 'error',
        })
    }).finally(()=>{
        loading.value=false
    })
}






</script>


<style scoped lang="less">
.login{
    width: 900px;
    height: 600px;
    border: 3px solid gray;
    border-radius: 10px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    overflow: hidden;

    .title{
        height: 50px;
        line-height: 50px;
        text-align: center;
        font-size: 30px;
        background: #cbc3c3;
    }

    .box{
        display: flex;
        justify-content: center;
        align-items: center;
        &>div{
            width: 50%;
            height: calc(600px - 50px);
            display: flex;
            justify-content: center;
            align-items: center;
        }
        &>div:nth-child(2){

            &>div{
                padding: 30px 10px 0 0 ;
                box-sizing: border-box;
                width: 95%;
                height: 60%;
                border: 1px solid gray;
                position: relative;
            }
            .isShow{
                width: 100%;
                text-align: right;
                color: #0086b3;
                cursor: pointer;
            }

            .commit{
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
            }

        }
    }
}
</style>