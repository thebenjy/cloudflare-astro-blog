#!/usr/bin/env python3
"""
Download all comments from D1 database to local JSON file.

Usage:
    python scripts/download_comments.py

Requires:
    - CLOUDFLARE_API_TOKEN environment variable
    - CLOUDFLARE_ACCOUNT_ID environment variable
    - D1_DATABASE_ID environment variable (or in wrangler.toml)

Or configure API URL directly:
    python scripts/download_comments.py --api-url https://your-api.workers.dev
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

def download_comments(api_url):
    """Download comments from the API"""

    endpoint = f"{api_url}/api/comments/all"

    try:
        print(f"Fetching comments from {endpoint}...")

        with urllib.request.urlopen(endpoint) as response:
            data = json.loads(response.read())
            comments = data.get('comments', [])

        print(f"✓ Downloaded {len(comments)} comments")
        return comments

    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def save_comments(comments, output_dir='backups/comments'):
    """Save comments to JSON file with timestamp"""

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{output_dir}/comments_{timestamp}.json"

    # Save to file
    with open(filename, 'w') as f:
        json.dump({
            'exported_at': datetime.utcnow().isoformat() + 'Z',
            'total_comments': len(comments),
            'comments': comments
        }, f, indent=2)

    print(f"✓ Saved to {filename}")

    # Also save as latest.json for easy access
    latest_file = f"{output_dir}/latest.json"
    with open(latest_file, 'w') as f:
        json.dump({
            'exported_at': datetime.utcnow().isoformat() + 'Z',
            'total_comments': len(comments),
            'comments': comments
        }, f, indent=2)

    print(f"✓ Updated {latest_file}")

    return filename

def main():
    # Get API URL from command line or environment
    if len(sys.argv) > 2 and sys.argv[1] == '--api-url':
        api_url = sys.argv[2]
    else:
        api_url = os.getenv('API_URL', 'https://your-blog-api.workers.dev')
        print(f"Using API URL: {api_url}")
        print("(Set API_URL environment variable or use --api-url flag to change)")

    # Download comments
    comments = download_comments(api_url)

    # Save to file
    filename = save_comments(comments)

    # Print summary
    print(f"\n--- Summary ---")
    print(f"Total comments: {len(comments)}")

    # Group by post
    by_post = {}
    for comment in comments:
        slug = comment['post_slug']
        by_post[slug] = by_post.get(slug, 0) + 1

    print(f"Posts with comments: {len(by_post)}")
    print("\nComments per post:")
    for slug, count in sorted(by_post.items(), key=lambda x: x[1], reverse=True):
        print(f"  {slug}: {count}")

    print(f"\n✓ Backup complete!")

if __name__ == '__main__':
    main()
