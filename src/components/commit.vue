<template>
    <el-dialog  :before-close="close"  v-model="centerDialogVisible" title="Comment" width="500" :align-center="true" center>
        <el-form :label-width="80" :rules="rules" ref="ruleFormRef" :model="info">
            <el-form-item label="comment" prop="comment">
                <el-input v-model="info.comment" type="textarea" rows="5" placeholder="Please enter your comment"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="close">Cancel</el-button>
                <el-button :loading="loading" type="primary" @click="submit(ruleFormRef)">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script setup>
//评论
import {reactive, ref,toRefs} from "vue";
const centerDialogVisible=ref(true)
const emit=defineEmits(['close','flush'])
import {addComment} from "@/api/index.js";
import { ElMessage } from 'element-plus'
const props=defineProps({
    blogId:{
        type:[String,Number]
    }
})
const {blogId}=toRefs(props)


//提交
const info=reactive({
    comment:''
})
const loading=ref(false)
//校验
const rules=reactive({
    comment:[{required:true,trigger: 'change',}],
})
const ruleFormRef=ref(null)
const submit=(ruleFormRef)=>{
    ruleFormRef.validate().then(()=>{
        loading.value=true
        let obj={
            content:info.comment,
            u_id:localStorage.getItem('uid'),
            blog_id:blogId.value
        }
        addComment(obj).then(res=>{
            emit('close')
            ElMessage.success({
                message: 'add success',
                type: 'success',
            })
            emit('flush')
        }).finally(()=>{
            loading.value=false
        })
    })
}
//关闭
const close=()=>{
    emit('close')
}

</script>
