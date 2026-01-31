import { Hono } from 'hono';
import { cors } from 'hono/cors';

type Bindings = {
  DB: D1Database;
};

const app = new Hono<{ Bindings: Bindings }>();

// Enable CORS for all routes
app.use('/*', cors());

// GET /api/comments?slug=post-slug - Fetch comments for a post
app.get('/api/comments', async (c) => {
  const slug = c.req.query('slug');

  if (!slug) {
    return c.json({ error: 'Missing slug parameter' }, 400);
  }

  try {
    const { results } = await c.env.DB.prepare(
      'SELECT id, post_slug, author_name, comment_text, created_at FROM comments WHERE post_slug = ? AND approved = 1 ORDER BY created_at DESC'
    ).bind(slug).all();

    return c.json({ comments: results });
  } catch (error) {
    return c.json({ error: 'Database error' }, 500);
  }
});

// POST /api/comments - Submit a new comment
app.post('/api/comments', async (c) => {
  try {
    const body = await c.req.json();
    const { slug, author, email, text } = body;

    if (!slug || !author || !text) {
      return c.json({ error: 'Missing required fields: slug, author, text' }, 400);
    }

    // Insert comment
    await c.env.DB.prepare(
      'INSERT INTO comments (post_slug, author_name, author_email, comment_text) VALUES (?, ?, ?, ?)'
    ).bind(slug, author, email || null, text).run();

    return c.json({ success: true, message: 'Comment submitted' }, 201);
  } catch (error) {
    return c.json({ error: 'Failed to submit comment' }, 500);
  }
});

// GET /api/comments/all - Export all comments (for backup script)
app.get('/api/comments/all', async (c) => {
  try {
    const { results } = await c.env.DB.prepare(
      'SELECT * FROM comments ORDER BY created_at DESC'
    ).all();

    return c.json({ comments: results });
  } catch (error) {
    return c.json({ error: 'Database error' }, 500);
  }
});

export default app;
