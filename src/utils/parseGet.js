//请求参数解析
export function parseString(obj){
    if (Object.keys(obj).every(v=>!obj[v])){
        return ''
    }else {
        let arr= Object.keys(obj).filter(v=>obj[v])
        return  arr.reduce((total,item,index)=>{
            if (arr.length===index+1){
                total+=item+'='+obj[item]
            }else{
                total+=item+'='+obj[item]+'&'
            }
            return total
        },'?')
    }
}

//时间解析
export function formatDate(date) {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}