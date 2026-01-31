#!/usr/bin/env python3
"""
Generate a new blog post from JSON input.

Usage:
    python scripts/generate_post.py input.json

Or pipe JSON:
    echo '{"title": "My Post", "content": "Hello world"}' | python scripts/generate_post.py

Input JSON format:
{
  "title": "Post Title",
  "content": "Full HTML or Markdown content",
  "excerpt": "Short description (optional, auto-generated if missing)",
  "author": "Author Name (optional)",
  "tags": ["tag1", "tag2"] (optional)
}
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
import re

def slugify(text):
    """Convert title to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def generate_excerpt(content, max_length=200):
    """Auto-generate excerpt from content"""
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', content)
    # Take first paragraph or max_length characters
    text = text.strip()[:max_length]
    # End at last complete word
    if len(text) == max_length:
        text = text[:text.rfind(' ')] + '...'
    return text

def create_post(data):
    """Create a new blog post file"""

    # Validate required fields
    if 'title' not in data or 'content' not in data:
        raise ValueError("JSON must include 'title' and 'content' fields")

    # Generate metadata
    slug = slugify(data['title'])
    now = datetime.utcnow().isoformat() + 'Z'

    # Auto-generate excerpt if not provided
    if 'excerpt' not in data or not data['excerpt']:
        data['excerpt'] = generate_excerpt(data['content'])

    # Create post object
    post = {
        'slug': slug,
        'title': data['title'],
        'content': data['content'],
        'excerpt': data['excerpt'],
        'author': data.get('author', 'Anonymous'),
        'publishedAt': now,
        'updatedAt': now,
        'tags': data.get('tags', [])
    }

    # Ensure content directory exists
    content_dir = Path('src/content/posts')
    content_dir.mkdir(parents=True, exist_ok=True)

    # Check if post already exists
    post_file = content_dir / f'{slug}.json'
    if post_file.exists():
        print(f"Warning: Post '{slug}' already exists. Updating with new content.")
        # Keep original publishedAt date
        with open(post_file, 'r') as f:
            existing = json.load(f)
            post['publishedAt'] = existing.get('publishedAt', now)

    # Write post file
    with open(post_file, 'w') as f:
        json.dump(post, f, indent=2)

    print(f"✓ Created post: {post_file}")
    print(f"  Title: {post['title']}")
    print(f"  Slug: {slug}")
    print(f"  Published: {post['publishedAt']}")

    return post

def main():
    try:
        # Read JSON from file or stdin
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r') as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)

        # Support batch creation
        if isinstance(data, list):
            posts = [create_post(item) for item in data]
            print(f"\n✓ Created {len(posts)} posts")
        else:
            create_post(data)
            print("\n✓ Post created successfully!")

        print("\nNext steps:")
        print("  1. Review the generated file in src/content/posts/")
        print("  2. Commit and push to trigger GitHub Actions deployment")
        print("  3. Or run 'npm run build' to build locally")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
