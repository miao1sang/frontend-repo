<template>
    <div style="width: 80%;height: 100%;margin: 0 auto">
        <div class="box" ref="box">
            <div class="search">
                <el-input
                    v-model="input1"
                    style="width: 900px"
                    size="large"
                    placeholder="search"
                    :prefix-icon="Search"
                />
                <el-button @click="searchTitle" style="margin-left: 50px;height: 40px">Business cooperation</el-button>
            </div>
            <div class="auth">
               <auth-detail   :id="route.query.id"></auth-detail>
            </div>

        </div>

      <public-list ref="boxList"  v-if="boxHeight" :boxHeight="boxHeight"  :id="authId"></public-list>
    </div>
</template>


<script setup>
import {onMounted, ref,watch} from 'vue'
import { Search } from '@element-plus/icons-vue'
import PublicList from '@/components/list/public-list.vue'
import AuthDetail from '@/components/auth-detail.vue'
import {useRoute} from 'vue-router'

const route=useRoute()
const input1 = ref('')


const boxList=ref(null)
function searchTitle(){
    let fetch=boxList.value.search
    fetch((filter,list,search)=>{
        list.value=[]
        filter.title=input1.value
        search()
    })
}


const authId=ref('')
watch(()=>route,newVal=>{
    authId.value=route.query.id || localStorage.getItem('uid')
},{deep:true,immediate:true})



//计算高度
const box=ref(null)
const boxHeight=ref()



onMounted(()=>{
    boxHeight.value=box.value.clientHeight
})


</script>


<style scoped lang="less">
.text() {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/deep/ .el-input__wrapper{
    border-radius: 50px !important;
}
.box{
    margin: 0 auto;
    padding-top: 50px;
    box-sizing: border-box;
    .search{
        display: flex;
        margin-left: 100px;
        align-items: center;
    }
    .auth{
        height: 250px;
        display: flex;
        align-items: center;
        margin-left: 200px;
    }


}
</style>