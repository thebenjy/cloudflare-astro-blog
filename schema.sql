-- Blog comments table
CREATE TABLE IF NOT EXISTS comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_slug TEXT NOT NULL,
  author_name TEXT NOT NULL,
  author_email TEXT,
  comment_text TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  approved BOOLEAN DEFAULT 1
);

CREATE INDEX idx_post_slug ON comments(post_slug);
CREATE INDEX idx_created_at ON comments(created_at DESC);

-- Blog posts metadata (optional, for tracking)
CREATE TABLE IF NOT EXISTS posts (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  published_at DATETIME NOT NULL,
  updated_at DATETIME,
  view_count INTEGER DEFAULT 0
);
