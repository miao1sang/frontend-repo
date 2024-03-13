import axios from 'axios';

// 创建axios实例
const  instance = axios.create({
    baseURL: 'http://127.0.0.1:5173', // api的base_url
    timeout: 5000 // 请求超时时间
});

// request拦截器
instance.interceptors.request.use(
    config => {
        // 在发送请求之前做些什么
        // 例如添加请求头、身份验证等
        // config.headers['Authorization'] = 'Bearer ' + token; // 让每个请求携带自定义token
        return config;
    },
    error => {
        // 处理请求错误
        console.log(error); // for debug
        Promise.reject(error);
    }
);

// respone拦截器
instance.interceptors.response.use(
    response => {
        // 如果返回的状态码为200，说明接口请求成功，可以正常拿到数据
        // 否则的话抛出错误
        const res = response.data;
        if (res.code !== 200) {
            return Promise.reject(new Error(res.message || 'Error'));
        } else {
            return response.data;
        }
    },
    // 服务器状态码不是2xx的情况
    error => {
        console.log('err' + error); // for debug
        if (error.response.status) {
            switch (error.response.status) {
                case 401:
                    // 未授权，登录过期等
                    // 可以选择重新登录，或者跳转到登录页
                    break;
                case 404:
                    // 请求不存在
                    break;
                case 500:
                    // 服务器错误
                    break;
                default:
                    break;
            }
            return Promise.reject(error.response);
        }
    }
);

// 添加get请求方法
export const get =  (url, config)=> {
    return new Promise((resolve, reject) => {
        instance.get(url, config)
            .then(response => {
                resolve(response.data);
            })
            .catch(error => {
                reject(error);
            });
    });
};

export const post=(url,params={})=>{
    return new Promise((resolve, reject) => {
        instance.post(url,params)
         .then(r=>{
            resolve(r.data)
        })
         .catch(error => {
            reject(error);
        });
    })
}

export const put=(url,params={})=>{
    return new Promise((resolve, reject) => {
        instance.put(url,params)
            .then(r=>{
                resolve(r.data)
            })
            .catch(error => {
                reject(error);
            });
    })
}

export const del=(url,params={})=>{
    return new Promise((resolve, reject) => {
        instance.delete(url)
            .then(r=>{
                resolve(r.data)
            })
            .catch(error => {
                reject(error);
            });
    })
}
