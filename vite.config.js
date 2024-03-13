import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),
    AutoImport({
    resolvers: [ElementPlusResolver()],
     }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),],
  resolve: {
    // 配置路径别名
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  css: {
    preprocessorOptions: {
      less: {
        // javascriptEnabled: true,
        charset: false,
      },
    },
  },
  server: {
    host:'127.0.0.1',
    port: 5173,
    proxy: {
      '/dev': {
        target: 'http://47.99.78.237:8001',//目标服务器地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/dev/, '')
      },
    }
  }
})
