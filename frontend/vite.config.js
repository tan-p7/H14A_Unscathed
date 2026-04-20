import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
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
