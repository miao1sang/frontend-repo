<template>
    <div class="login">
        <div class="title">Login</div>
        <div class="box" >
            <div>
                <div style="width: 200px;height: 230px">
                    <img  style="width: 100%;height: 100%" src="../assets/myqrcode.jpg">
                </div>
            </div>
            <div>
                <div>
                   <el-form ref="box" :rules="rules" :label-width="100" :model="info">
                       <el-form-item label="Username" prop="username">
                           <el-input v-model="info.username"></el-input>
                       </el-form-item>
                       <el-form-item label="Password" prop="password">
                           <el-input :type="passwordType" v-model="info.password"></el-input>
                       </el-form-item>
                   </el-form>
                    <div class="isShow" @click="changeInput">{{passWordTitle?'show':'hide'}}</div>
                    <hr style="margin-left: 10px">
                    <el-checkbox @change="radioChange" style="margin-left: 10px;" v-model="radio" label="Remeber my username on this computer" size="large" />
                    <div class="commit">
                        <el-button :loading="loading" style="width: 200px; height: 50px" @click="commit(box)">Continue</el-button>
                    </div>
                    <div class="sign">
                        don’t have an account?
                        <span @click="toSign" style="color: #0086b3;cursor: pointer">Sign up</span>
                    </div>
                </div>
            </div>


        </div>
    </div>
</template>


<script setup>
import {useRouter} from 'vue-router'
const router=useRouter()
import { ElMessage } from 'element-plus'
import {login} from '@/api/index.js'

//校验
import {reactive,ref,computed,onMounted} from "vue";
const rules=reactive({
    username:[{required:true,trigger: 'change',}],
    password:[{required:true,trigger: 'change',}],
})
const info=reactive({
    username:'',
    password:''
})

onMounted(()=>{
   let username= localStorage.getItem('username')
    if (username){
        info.username=username
        radio.value=true
    }
})
const box=ref(null)
const loading=ref(false)
//登录
const commit=(box)=>{
    box.validate().then(()=>{
        loading.value=true
        let obj={
            name:info.username,
            password:info.password
        }
        return login(obj)
    }).then((res)=>{
        localStorage.setItem('name',res.u_name)
        localStorage.setItem('uid',res.u_id)
        localStorage.setItem('isSuper',res.is_super)
        ElMessage.success({
            message: 'login success',
            type: 'success',
        })
        setTimeout(()=>{
            router.push({
                name:'home'
            })
        },1000)
    }).catch(()=>{
        ElMessage.error({
            message: 'the username or password is incorrect',
            type: 'error',
        })
    }).finally(()=>{
        loading.value=false
    })
}

//切换
const passwordType=computed(()=>{
   return passWordTitle.value?'password':'text'
})
const passWordTitle=ref(true)
const changeInput=()=>{
   passWordTitle.value=!passWordTitle.value
}

//记住我
const radio=ref(false)
const radioChange=()=>{
   if (radio.value){
       localStorage.setItem('username',info.username)
   }else {
       localStorage.removeItem('username')
   }
}

//跳转到注册页面
const toSign=()=>{
    router.push({
        name:'sign'
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
            .sign{
                width: 100%;
                position: absolute;
                bottom: -100px;
                left: 180px;
                color: gray;
            }

        }
    }
}
</style>