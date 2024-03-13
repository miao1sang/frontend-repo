<template>
    <el-dialog  :before-close="close"  v-model="centerDialogVisible" title="Help" width="500" :align-center="true" center>
        <el-form :label-width="50" :rules="rules" ref="ruleFormRef" :model="info">
            <el-form-item label="Title" prop="title">
                <el-input v-model="info.title" ></el-input>
            </el-form-item>
            <el-form-item label="Detail" prop="detail">
                <el-input v-model="info.detail" type="textarea" rows="5"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="close">Cancel</el-button>
                <el-button type="primary" @click="submit(ruleFormRef)">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script setup>
//帮助
import {reactive, ref} from "vue";
const centerDialogVisible=ref(true)
const emit=defineEmits(['close'])
//提交
const info=reactive({
    title:'',
    detail:''
})
//校验
const rules=reactive({
    title:[{required:true,trigger: 'change',}],
    detail:[{required:true,trigger: 'change',}]
})
const ruleFormRef=ref(null)
const submit=(ruleFormRef)=>{
    ruleFormRef.validate().then(()=>{
        centerDialogVisible.value=false
    })
}
//关闭
const close=()=>{
    emit('close')
}

</script>
