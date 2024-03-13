import {get,post,put,del} from '@/utils/request.js'


//注册
export const sign=(body)=>{
    return post('/dev/users/',body)
}
//登录
export const login=(body)=>{
    return post('/dev/users/login/',body)
}

//个人信息查询
export const userDetail=(params)=>{
    return get(`/dev/users/${params}`)
}
//个人信息修改
export const userUpdate=(params,body)=>{
    return put(`/dev/users/${params}`,body)
}

//新增博客
export const addBlog=(body)=>{
    return post('/dev/blogs/',body)
}
//删除博客
export const delBlog=(params)=>{
    return del(`/dev/blogs/${params}/`)
}

//博客列表
export const blogList=(params)=>{
    return get(`/dev/blogs/${params}`)
}

//根据博客查询评论
export const getCommentById=(params)=>{
    return get(`/dev/comments/${params}`)
}
//新增评论
export const addComment=(body)=>{
    return post(`/dev/comments/`,body)
}
//删除评论
export const delComment=(params)=>{
    return del(`dev/comments/${params}`)
}

//点赞收藏博客
export const updateBlog=(params,body)=>{
    return put(`dev/blogs/${params}/`,body)
}