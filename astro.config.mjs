import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',
  site: 'https://cloudflare-astro-blog.pages.dev',
  build: {
    format: 'directory'
  }
});
