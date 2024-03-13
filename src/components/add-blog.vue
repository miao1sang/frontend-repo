<template>
    <div class="box">
      <el-form :model="info" :label-width="100" :rules="rules" ref="box">
          <el-form-item label="blog title" prop="title">
             <el-input v-model="info.title"></el-input>
          </el-form-item>
          <el-form-item label="blog image" prop="img">
              <upload-list v-model="info.img"></upload-list>
          </el-form-item>
          <el-form-item label="blog text" prop="text">
              <el-input type="textarea" rows="10" v-model="info.text"></el-input>
          </el-form-item>
      </el-form>
        <el-button :loading="loading" style="width: 100%;height: 50px;" @click="commit(box)">Commit</el-button>
    </div>
</template>

<script  setup>
import { ref,reactive,watch } from 'vue'
import UploadList from '@/components/list/upload.vue'
import {addBlog} from '@/api/index.js'
import { ElMessage } from 'element-plus'
import {useRouter} from 'vue-router'
const router=useRouter()
const box=ref(null)
const loading=ref(false)
const info=reactive({
    img:[],
    title:'',
    text:''
})


//校验
const validateEmail=(rules,value,callback)=>{
    if (!value.length){
        callback(new Error('image is required'))
    }else{
        callback()
    }
}
const rules=reactive({
    title:[{required:true,trigger: 'change',}],
    text:[{required:true,trigger: 'change',}],
    img:[{validator:validateEmail,required:true,trigger: 'change',}],
})

//提交
const commit=(ruleForm)=>{
    ruleForm.validate().then(()=>{
        let id=localStorage.getItem('uid')
        loading.value=true
        let formData = new FormData()
        let file=info.img[0].raw
        formData.append('image', file)// 传文件
        formData.append('title', info.title)
        formData.append('content', info.text)
        formData.append('u_id', id)
        return addBlog(formData)
    }).then(()=>{
        ElMessage.success({
            message: 'add success',
            type: 'success',
        })
        setTimeout(()=>{
            router.push({
                name:'list'
            })
        },2000)
    }).finally(()=>{
       loading.value=false
    })
}

</script>

<style scoped lang="less">
.box{
    width: 50%;
    height: auto;
    margin: 100px auto;
    border: 3px solid gray;
    padding: 50px;
    box-sizing: border-box;
    border-radius: 10px;
}



</style>