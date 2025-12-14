import { defineConfig } from 'vite'

// Make React plugin optional so dev can start even if npm install hasn't been run yet.
export default defineConfig(async () => {
  const plugins: any[] = []
  try {
    const mod = await import('@vitejs/plugin-react')
    const react = (mod as any).default
    if (react) plugins.push(react())
  } catch (e) {
    // plugin not installed yet; skip to allow basic dev server to run
    console.warn('[vite] @vitejs/plugin-react not found; running without React fast-refresh')
  }
  return {
    plugins,
    server: {
      port: 5173,
      strictPort: true,
    }
  }
})
