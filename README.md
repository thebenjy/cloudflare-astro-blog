# Cloudflare Astro Blog

A fully automated, $10/year blogging platform built with Astro, Hono, Cloudflare Pages, and D1.

## Features

- 🚀 **Static Site Generation** with Astro
- 💬 **Dynamic Comments** via Hono API + D1 database
- 🤖 **Automated Content Generation** with Python scripts
- 📦 **Automated Deployment** via GitHub Actions
- 💰 **Ultra Low Cost** - Just $10/year for domain!
- 🎨 **Classic Boomer CSS** - Simple, readable, nostalgic design
- 📱 **Responsive** - Works on all devices
- 🔍 **SEO Optimized** - Proper meta tags, sitemaps, structured data

## Architecture

```
┌─────────────────┐
│  GitHub Repo    │  ← Content stored as JSON
└────────┬────────┘
         │
         │ git push
         ▼
┌─────────────────┐
│ GitHub Actions  │  ← Builds & deploys automatically
└────────┬────────┘
         │
         ├─────────────────┐
         ▼                 ▼
┌──────────────┐   ┌──────────────┐
│ Cloudflare   │   │   Hono API   │
│   Pages      │   │   (Worker)   │
│  (Static)    │   │              │
└──────────────┘   └──────┬───────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ D1 Database │
                   │  (SQLite)   │
                   └─────────────┘
```

## Setup Instructions

### 1. Prerequisites

- GitHub account
- Cloudflare account (free tier works!)
- Node.js 20+ installed locally
- Python 3.8+ installed locally

### 2. Clone and Install

```bash
git clone https://github.com/thebenjy/cloudflare-astro-blog.git
cd cloudflare-astro-blog
npm install
```

### 3. Create D1 Database

```bash
# Login to Cloudflare
npx wrangler login

# Create D1 database
npx wrangler d1 create blog_comments

# Note the database_id from output, update wrangler.toml

# Run schema
npx wrangler d1 execute blog_comments --file=schema.sql
```

### 4. Update Configuration

Edit `wrangler.toml`:
```toml
database_id = "your-actual-d1-database-id"
```

Edit `astro.config.mjs`:
```js
site: 'https://your-actual-domain.pages.dev'
```

### 5. Deploy API Worker

```bash
npx wrangler deploy functions/api.ts
```

Note the Worker URL (e.g., `https://cloudflare-astro-blog-api.your-subdomain.workers.dev`)

### 6. Configure GitHub Secrets

Go to your repo Settings → Secrets and variables → Actions, add:

- `CLOUDFLARE_API_TOKEN` - Get from Cloudflare dashboard
- `CLOUDFLARE_ACCOUNT_ID` - Get from Cloudflare dashboard

### 7. Create Your First Post

Create `input.json`:
```json
{
  "title": "My First Blog Post",
  "content": "<h2>Hello World</h2><p>This is my first post!</p>",
  "excerpt": "Welcome to my new blog",
  "author": "Your Name",
  "tags": ["introduction", "meta"]
}
```

Generate the post:
```bash
python scripts/generate_post.py input.json
```

### 8. Deploy

```bash
git add .
git commit -m "Add first blog post"
git push
```

GitHub Actions will automatically build and deploy!

## Usage

### Generate a Blog Post

**From JSON file:**
```bash
python scripts/generate_post.py my-post.json
```

**From stdin:**
```bash
echo '{"title": "Quick Post", "content": "<p>Hello!</p>"}' | python scripts/generate_post.py
```

**JSON format:**
```json
{
  "title": "Post Title",
  "content": "Full HTML content",
  "excerpt": "Short description (optional, auto-generated if missing)",
  "author": "Author Name (optional)",
  "tags": ["tag1", "tag2"]
}
```

### Download Comments Daily

Set up environment variables:
```bash
export API_URL="https://your-api.workers.dev"
```

Run backup:
```bash
python scripts/download_comments.py
```

Comments saved to `backups/comments/` with timestamp.

### Local Development

```bash
npm run dev
```

Visit `http://localhost:4321`

### Manual Build

```bash
npm run build
npm run preview
```

## Project Structure

```
cloudflare-astro-blog/
├── src/
│   ├── layouts/
│   │   └── Layout.astro          # Main layout with SEO
│   ├── pages/
│   │   ├── index.astro           # Home page (latest posts)
│   │   ├── archive.astro         # All posts by year
│   │   ├── about.astro           # About page
│   │   └── posts/
│   │       └── [slug].astro      # Dynamic post pages
│   └── content/
│       └── posts/                # Generated JSON posts
│           └── *.json
├── functions/
│   └── api.ts                    # Hono API worker for comments
├── scripts/
│   ├── generate_post.py          # Generate blog posts from JSON
│   └── download_comments.py      # Backup D1 comments to JSON
├── public/
│   └── styles/
│       └── main.css              # Boomer CSS styling
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions CI/CD
├── schema.sql                    # D1 database schema
├── wrangler.toml                 # Cloudflare configuration
├── astro.config.mjs              # Astro configuration
└── package.json
```

## Automated Workflows

### Content Generation → Deployment

1. Create post JSON
2. Run `python scripts/generate_post.py input.json`
3. Commit and push
4. GitHub Actions automatically:
   - Builds static site
   - Deploys to Cloudflare Pages
   - Deploys Hono API worker

### Daily Comment Backups

Set up a cron job:
```bash
# Add to crontab (runs daily at 2am)
0 2 * * * cd /path/to/blog && python scripts/download_comments.py
```

Or use GitHub Actions:
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2am UTC
```

## Cost Breakdown

- **Domain**: $10/year (only required cost)
- **Cloudflare Pages**: FREE (500 builds/month)
- **Cloudflare Workers**: FREE (100k requests/day)
- **D1 Database**: FREE (5GB storage, 5M reads/day)

Total: **$10/year** 🎉

## SEO Features

- Semantic HTML5 structure
- Open Graph meta tags
- Twitter Card support
- Canonical URLs
- Sitemap generation (coming soon)
- robots.txt (coming soon)
- Structured data (coming soon)

## Customization

### Change CSS Theme

Edit `public/styles/main.css` - it's plain CSS, no build step needed!

### Add New Pages

Create `.astro` files in `src/pages/`

### Modify Layout

Edit `src/layouts/Layout.astro`

## Troubleshooting

### Build fails in GitHub Actions

- Check that secrets are set correctly
- Verify `wrangler.toml` has correct database_id
- Ensure D1 database is created

### Comments not loading

- Check API Worker is deployed
- Verify D1 binding in `wrangler.toml`
- Check browser console for CORS errors

### Python scripts fail

- Ensure Python 3.8+
- Check you're in project root directory
- Verify `src/content/posts/` directory exists

## Contributing

Pull requests welcome! Please open an issue first to discuss changes.

## License

MIT License - feel free to use for your own blog!

## Credits

Built with:
- [Astro](https://astro.build)
- [Hono](https://hono.dev)
- [Cloudflare Pages](https://pages.cloudflare.com)
- [Cloudflare D1](https://developers.cloudflare.com/d1)

---

**Questions?** Open an issue on GitHub!
