// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

// Utilities
import { defineConfig, loadEnv } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
// eslint-disable-next-line no-unused-vars
export default defineConfig(({command, mode}) => {
  const env = loadEnv(mode, process.cwd())
  return {
    plugins: [
      vue({ 
        template: { transformAssetUrls }
      }),
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
      vuetify({
        autoImport: true,
      }),
    ],
    define: { 
      'process.env': {},
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
      extensions: [
        '.js',
        '.json',
        '.jsx',
        '.mjs',
        '.ts',
        '.tsx',
        '.vue',
      ],
    },
    server: {
      port: parseInt(env.VITE_UI_PORT),
    },
    test: {
      passWithNoTests: true,
      exclude: [
        "**/node_modules/**",
      ],
      environment: "jsdom",
      globals: true,
      reporter: ["verbose"],
      mockReset: true,
      coverage: {
        provider: "c8",
        all: true,
        reporter: ["text", "text-summary", "html"],
        include: ["**/*.{js,ts,vue}"],
        exclude: [
          "*.{config,options,spec,eslintrc}.*",
          "coverage/**",
          "dist/**",
          "public/**",
          "test/**",
          "src/assets/**",
          "src/plugins/**",
        ],
        reportsDirectory: "coverage",
      },
      deps: {
        external: ["**/node_modules/**", "**/dist/**"],
      },
      include: ["**/*.spec.{js,ts,vue}"],
    },
  }
})
