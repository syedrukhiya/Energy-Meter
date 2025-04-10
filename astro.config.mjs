import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import react from '@astrojs/react';
import node from '@astrojs/node';
// Import your global CSS file
import './src/styles/global.css';  // Adjust the path if necessary
import reactI18next from "astro-react-i18next";

export default defineConfig({
  integrations: [tailwind(), react(), reactI18next({
    defaultLocale: "it",
    locales: ["en", "it",],
  }),],
  base: '/',
  output: 'server',
  
  adapter: node({
    mode: 'standalone'
  }),
  build: {
    target: 'esnext', // Use a modern target that supports top-level await
  },
  // Add styles option for global stylesheets
  styles: [
    './global.css'  // Ensure the path is correct relative to your config file
  ],
});