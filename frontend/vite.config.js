import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  base: '/H14A_Unscathed/',
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/atlas': {
        target: 'https://y1j7xv2ua6.execute-api.us-east-1.amazonaws.com/v2',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/atlas/, '')
      }
    }
  }
})