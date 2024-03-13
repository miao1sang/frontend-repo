<template>
    <el-upload  list-type="picture-card" :auto-upload="false" v-model:file-list="list" :disabled="list.length===1" @change="change">
        <el-icon><Plus /></el-icon>

        <template #file="{ file }">
            <div>
                <img class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
                <span class="el-upload-list__item-actions">

          <span
              v-if="!disabled"
              class="el-upload-list__item-delete"
              @click="handleRemove(file)"
          >
            <el-icon><Delete /></el-icon>
          </span>
        </span>
            </div>
        </template>
    </el-upload>


</template>
<script  setup>
import { ref,watch,nextTick } from 'vue'
import { Delete, Plus } from '@element-plus/icons-vue'
import { useFormItem } from "element-plus";
const { formItem } = useFormItem();
const props=defineProps({
    modelValue:{
        type:Array
    }
})
const emit=defineEmits(['update:modelValue'])
const list=ref([])

watch(()=>props.modelValue,newVal=>{
   list.value=[...newVal]
},{deep:true,immediate:true})

const change=()=>{
    nextTick(()=>{
        emit('update:modelValue', list.value);
        formItem?.validate("change");
    })
}
const handleRemove = (file) => {
    list.value=[]
    nextTick(()=>{
        emit('update:modelValue', list.value);
        formItem?.validate("change");
    })

}



const disabled = ref(false)





</script>