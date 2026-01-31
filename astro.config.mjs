import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'static',
  site: 'https://your-blog.pages.dev',
  adapter: cloudflare(),
  build: {
    format: 'directory'
  }
});
