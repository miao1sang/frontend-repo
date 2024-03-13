<template>
    <div :style="{height:clientHeight}" class="index">
        <left-menu ></left-menu>
        <router-view ></router-view>
    </div>
</template>

<script setup>
import {ref,onMounted} from 'vue'
import LeftMenu from '../components/menu.vue'


const clientHeight=ref()
onMounted(()=>{
    clientHeight.value=window.innerHeight+'px'
})


</script>


<style lang="less" scoped>
.index{
    display: flex;
}
</style>
