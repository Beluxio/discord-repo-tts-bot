import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/tts': 'http://localhost:8000',
      '/status': 'http://localhost:8000',
    },
  },
})
