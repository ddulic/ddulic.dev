#!/usr/bin/env python3
"""
Migration script: Notion export (dev urandom v3) → Fuwari/Astro (ddulic.dev)
"""

import csv
import re
import shutil
import os
from pathlib import Path
from datetime import datetime
from urllib.parse import unquote

# ── Paths ────────────────────────────────────────────────────────────────────
NOTION_POSTS_DIR = Path("/home/deck/Documents/dev urandom v3/Blog Posts/Blog Posts")
NOTION_CSV       = Path("/home/deck/Documents/dev urandom v3/Blog Posts/Blog Posts 1f463f368cbb438f85304931cd7ced4d.csv")
NOTION_ABOUT     = Path("/home/deck/Documents/dev urandom v3/Damir Dulic, Systems Engineering Lead 21acf7fb0e1c4738b4cfe0bdbaafe2f9.md")

ASTRO_POSTS_DIR  = Path("/home/deck/Documents/ddulic.dev/src/content/posts")
ASTRO_IMAGES_DIR = Path("/home/deck/Documents/ddulic.dev/src/assets/images")
ASTRO_ABOUT      = Path("/home/deck/Documents/ddulic.dev/src/content/spec/about.md")

# ── Helpers ──────────────────────────────────────────────────────────────────

def slugify(title: str) -> str:
    """Convert a post title to a URL-friendly slug."""
    slug = title.lower()
    slug = re.sub(r"[''']", "", slug)          # drop apostrophes
    slug = re.sub(r"[^a-z0-9]+", "-", slug)   # non-alnum → hyphen
    slug = slug.strip("-")
    return slug


def parse_date(date_str: str) -> str | None:
    """Parse a date string like 'August 22, 2023' → '2023-08-22'."""
    if not date_str:
        return None
    for fmt in ("%B %d, %Y", "%B %d %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None


def infer_category(title: str) -> str:
    """Very simple keyword-based category inference."""
    t = title.lower()
    if any(k in t for k in ["kubernetes", "cka", "k8s", "helm", "eks", "aks"]):
        return "Kubernetes"
    if any(k in t for k in ["terraform", "cloudformation", "iac"]):
        return "Terraform"
    if any(k in t for k in ["aws", "cloudfront", "route53", "s3", "acm"]):
        return "AWS"
    if any(k in t for k in ["linux", "ubuntu", "elementary"]):
        return "Linux"
    if any(k in t for k in ["devops", "ci/cd", "circleci", "pipeline", "deploy"]):
        return "DevOps"
    if any(k in t for k in ["book", "notes", "review"]):
        return "Reading"
    if any(k in t for k in ["notion", "setup", "workflow", "productivity"]):
        return "Productivity"
    if any(k in t for k in ["cloudflare"]):
        return "DevOps"
    if any(k in t for k in ["plex", "hackintosh", "wow", "steam", "ipad"]):
        return "Personal"
    if any(k in t for k in ["blog", "hugo", "hexo", "markdown", "wordpress", "migrate"]):
        return "Blogging"
    return "DevOps"


def infer_tags(title: str) -> list[str]:
    """Pull obvious technology tags from the title."""
    tags = []
    pairs = [
        ("kubernetes", "Kubernetes"), ("helm", "Helm"), ("eks", "EKS"),
        ("terraform", "Terraform"), ("cloudformation", "CloudFormation"),
        ("aws", "AWS"), ("cloudfront", "CloudFront"), ("cloudflare", "Cloudflare"),
        ("linux", "Linux"), ("devops", "DevOps"), ("docker", "Docker"),
        ("ci/cd", "CI/CD"), ("circleci", "CircleCI"), ("plex", "Plex"),
        ("notion", "Notion"), ("github", "GitHub"), ("hugo", "Hugo"),
        ("wordpress", "WordPress"), ("ansible", "Ansible"), ("python", "Python"),
        ("kong", "Kong"), ("opa", "OPA"), ("istio", "Istio"),
        ("hackintosh", "Hackintosh"), ("ipad", "iPad"), ("siri", "Siri"),
        ("book notes", "Book Notes"), ("cka", "CKA"),
    ]
    t = title.lower()
    for keyword, tag in pairs:
        if keyword in t:
            tags.append(tag)
    return tags


# ── Notion-markup cleaner ─────────────────────────────────────────────────────

# Matches the inline date like "Jun 08, 2021" or "Oct 12, 2015" on its own line
INLINE_DATE_RE = re.compile(
    r"^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\s*$",
    re.MULTILINE,
)

def clean_notion_markdown(raw: str, title: str) -> str:
    """
    Strip Notion-export artefacts and return clean body markdown.
    """
    lines = raw.splitlines()
    output = []
    i = 0
    skip_until_close_aside = False

    while i < len(lines):
        line = lines[i]

        # Skip the first H1 (it becomes the frontmatter title)
        if i == 0 and line.strip() == f"# {title}":
            i += 1
            continue

        # Remove "Status: ..." and "Date: ..." metadata lines
        if re.match(r"^Status:\s|^Date:\s", line.strip()):
            i += 1
            continue

        # Remove <aside> … </aside> blocks entirely
        if "<aside>" in line:
            skip_until_close_aside = True
            i += 1
            continue
        if skip_until_close_aside:
            if "</aside>" in line:
                skip_until_close_aside = False
            i += 1
            continue

        # Remove lone inline-date lines
        if INLINE_DATE_RE.match(line.strip()):
            i += 1
            continue

        # Remove cover photo credit lines  "Cover Photo by ... on Unsplash"
        if re.match(r"^Cover Photo by\s", line.strip()):
            i += 1
            continue

        output.append(line)
        i += 1

    # Strip leading/trailing blank lines
    text = "\n".join(output).strip()
    return text


def fix_image_paths(content: str, notion_folder: str, slug: str) -> str:
    """
    Rewrite Notion image refs  ![](FolderName/image.png)
    to Astro-relative paths   ![](../../assets/images/slug/image.png)

    Uses a non-greedy match anchored at end-of-token so that paths
    containing literal parentheses (e.g. (CKA)) are captured in full.
    """
    # Non-greedy: captures up to the ) that is followed by whitespace or EOL,
    # preventing a premature stop at ) inside (CKA)-style names.
    IMG_RE = re.compile(r'!\[([^\]]*)\]\((.+?)\)(?=\s|$)', re.MULTILINE)

    def replacer(m):
        alt  = m.group(1)
        path = m.group(2)
        # Skip external URLs
        if path.startswith("http://") or path.startswith("https://"):
            return m.group(0)
        # URL-decode then take only the filename, discarding any leading folders
        filename = Path(unquote(path)).name
        return f"![{alt}](../../assets/images/{slug}/{filename})"

    return IMG_RE.sub(replacer, content)


# ── Image copier ─────────────────────────────────────────────────────────────

def copy_post_images(notion_post_folder: Path, slug: str):
    """Copy all image files from a Notion post subfolder to ASTRO_IMAGES_DIR/slug/."""
    if not notion_post_folder.exists():
        return
    dest = ASTRO_IMAGES_DIR / slug
    dest.mkdir(parents=True, exist_ok=True)
    image_exts = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
    for f in notion_post_folder.iterdir():
        if f.suffix.lower() in image_exts:
            shutil.copy2(f, dest / f.name)
            print(f"  📷  {f.name} → assets/images/{slug}/{f.name}")


# ── Find Notion .md file ──────────────────────────────────────────────────────

def normalize_for_match(s: str) -> str:
    """Strip/replace punctuation that Notion drops or replaces in filenames."""
    s = re.sub(r"[/]", " ", s)          # slash → space (Notion treats / as separator)
    s = re.sub(r"[:.?!']", "", s)       # other special chars just removed
    s = re.sub(r"\s+", " ", s)          # collapse multiple spaces
    return s.strip()


def find_notion_md(title: str) -> Path | None:
    """
    Notion exports files as  "Title uuid.md".
    Notion strips special characters (colons, slashes, question marks …)
    from the filename, so we normalise both sides before comparing.
    """
    title_norm = normalize_for_match(title)

    for f in NOTION_POSTS_DIR.glob("*.md"):
        # Strip the trailing uuid (last space + 32 hex chars)
        stem       = re.sub(r"\s+[0-9a-f]{32}$", "", f.stem)
        stem_norm  = normalize_for_match(stem)
        if stem_norm == title_norm:
            return f

    # Fallback: normalised startswith (first 20 chars)
    for f in NOTION_POSTS_DIR.glob("*.md"):
        stem      = re.sub(r"\s+[0-9a-f]{32}$", "", f.stem)
        stem_norm = normalize_for_match(stem)
        if stem_norm.lower().startswith(title_norm.lower()[:20]):
            return f
    return None


# ── Find Notion image folder ──────────────────────────────────────────────────

def find_notion_image_folder(title: str) -> Path | None:
    """
    Notion creates a sibling folder whose name is the title with special chars
    stripped (same normalisation as the .md file).
    """
    # Exact match (no special chars in title)
    exact = NOTION_POSTS_DIR / title
    if exact.is_dir():
        return exact

    title_norm = normalize_for_match(title)

    for d in NOTION_POSTS_DIR.iterdir():
        if d.is_dir():
            d_norm = normalize_for_match(d.name)
            if d_norm == title_norm:
                return d

    # Fallback: normalised prefix (50 chars)
    for d in NOTION_POSTS_DIR.iterdir():
        if d.is_dir():
            d_norm = normalize_for_match(d.name)
            if d_norm.lower().startswith(title_norm.lower()[:50]):
                return d
    return None


# ── Build frontmatter ─────────────────────────────────────────────────────────

def build_frontmatter(title: str, date_str: str | None, is_draft: bool, slug: str) -> str:
    category = infer_category(title)
    tags     = infer_tags(title)
    tags_yaml = "[" + ", ".join(tags) + "]" if tags else "[]"

    published = date_str if date_str else "2015-01-01"
    draft_val = "true" if is_draft else "false"

    return f"""---
title: "{title}"
published: {published}
description: ""
tags: {tags_yaml}
category: {category}
draft: {draft_val}
---"""


# ── Main migration ────────────────────────────────────────────────────────────

def migrate_posts():
    print("\n─── Migrating blog posts ───────────────────────────────────────────")

    with open(NOTION_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    skipped = []
    migrated = []

    for row in rows:
        title  = row["Name"].strip()
        date   = row.get("Date", "").strip()
        status = row.get("Status", "").strip()

        # Skip template/placeholder rows
        if title in ("New Blog Post", "New Book Note"):
            print(f"  ⏭  Skipping template: {title}")
            continue

        is_draft = status in ("Drafts", "Archive")
        slug     = slugify(title)
        date_iso = parse_date(date)

        # Locate source .md
        md_file = find_notion_md(title)
        if md_file is None:
            print(f"  ❌  Cannot find .md for: {title}")
            skipped.append(title)
            continue

        raw = md_file.read_text(encoding="utf-8")

        # Clean content
        body = clean_notion_markdown(raw, title)

        # Copy images and fix paths
        img_folder = find_notion_image_folder(title)
        if img_folder:
            copy_post_images(img_folder, slug)
        body = fix_image_paths(body, title, slug)

        # Build output
        fm      = build_frontmatter(title, date_iso, is_draft, slug)
        output  = fm + "\n\n" + body + "\n"

        dest = ASTRO_POSTS_DIR / f"{slug}.md"
        dest.write_text(output, encoding="utf-8")
        print(f"  ✅  {title} → posts/{slug}.md")
        migrated.append(title)

    print(f"\n  Done: {len(migrated)} migrated, {len(skipped)} skipped")
    if skipped:
        print(f"  Skipped: {skipped}")


# ── About page ────────────────────────────────────────────────────────────────

def migrate_about():
    print("\n─── Migrating about page ───────────────────────────────────────────")

    raw = NOTION_ABOUT.read_text(encoding="utf-8")
    lines = raw.splitlines()

    # Remove the duplicate H1 at very top (first two identical lines)
    # The file starts with "# Damir Dulic, …\n\n# Damir Dulic, …"
    cleaned_lines = []
    skip_first_h1 = True
    for line in lines:
        if skip_first_h1 and line.startswith("# "):
            skip_first_h1 = False
            continue     # skip the very first H1 duplicate
        # Drop <aside> blocks (just the wrapper tags, keep content? here they are simple links, drop entirely)
        cleaned_lines.append(line)

    content = "\n".join(cleaned_lines).strip()

    # Remove <aside> … </aside> blocks
    content = re.sub(r"<aside>.*?</aside>", "", content, flags=re.DOTALL)

    # Collapse multiple blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    about_md = content.strip() + "\n"
    ASTRO_ABOUT.write_text(about_md, encoding="utf-8")
    print(f"  ✅  about.md written")


# ── Remove demo content ───────────────────────────────────────────────────────

DEMO_FILES = [
    "draft.md",
    "expressive-code.md",
    "markdown-extended.md",
    "markdown.md",
    "video.md",
]

def remove_demo_content():
    print("\n─── Removing demo content ──────────────────────────────────────────")

    # Remove demo posts
    for name in DEMO_FILES:
        p = ASTRO_POSTS_DIR / name
        if p.exists():
            p.unlink()
            print(f"  🗑  Removed posts/{name}")

    # Remove demo guide folder
    guide = ASTRO_POSTS_DIR / "guide"
    if guide.is_dir():
        shutil.rmtree(guide)
        print(f"  🗑  Removed posts/guide/")

    # Remove demo banner/avatar images (keep directory)
    for img in ["demo-banner.png", "demo-avatar.png"]:
        p = ASTRO_IMAGES_DIR / img
        if p.exists():
            p.unlink()
            print(f"  🗑  Removed assets/images/{img}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Ensure output dirs exist
    ASTRO_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    ASTRO_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    remove_demo_content()
    migrate_posts()
    migrate_about()

    print("\n✨  Migration complete!\n")
