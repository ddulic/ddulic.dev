---
name: enrich-blog-post
description: Enrich a blog post's frontmatter (description, tags, category) and rename non-SEO image filenames, enforcing this repo's consistency rules. Use when adding or editing a post under src/content/posts/, when frontmatter is empty/placeholder, or when asked to "enrich", "fill in tags/description/category", or "fix image names" for a post.
---

# Enrich blog post

Runs the enrichment that used to live in the `Auto Enrich Blog Posts` GitHub
workflow, but locally against the working tree. It fills empty/placeholder
frontmatter and renames non-SEO image filenames for posts in
`src/content/posts/`, keeping tags/categories consistent across the whole blog.

## When to run

- A new or edited post under `src/content/posts/*.md`.
- The post's `description`, `tags`, or `category` is empty or a placeholder.
- The post references images with non-descriptive filenames.

## 1. Determine target post(s)

If the user named a file, use it. Otherwise detect changed posts vs `main`:

```bash
git diff --name-only main...HEAD -- 'src/content/posts/*.md'
git status --porcelain -- 'src/content/posts/*.md'   # include uncommitted/new
```

Only enrich a field that is **empty or clearly a placeholder** — never overwrite
content the author wrote deliberately.

## 2. Build the blog-wide tag map first

Read **all** files in `src/content/posts/` and build a frequency map of every
`tags:` value across posts. You need this before assigning tags, because tags are
only valid when shared. Also skim existing `description:` / `category:` values for
the house style.

## 3. Apply the rules

### Description
- Single sentence summarising the post.
- Length **110–160 characters inclusive**.
- Active, informative style — describe what the post covers or teaches.
- Never empty or a placeholder.
- Only (re)write it if currently empty (`""`) or clearly a placeholder.

### Tags
- A tag is valid only if it also appears on **at least one other** post in
  `src/content/posts/` (shared across ≥2 posts after your change).
- Max **5 tags** per post.
- Concise and Title-Cased (e.g. `Terraform`, `Kubernetes`, `DevOps`, `Linux`,
  `Productivity`).
- Never use generic/vague tags: `Personal`, `Setup`, `General`, `Misc`, `Other`,
  `Various`, `Tips`, `Guide`, `Tutorial`.
- If this change leaves a tag on only a single post elsewhere, remove that
  now-orphaned tag from those posts too, to keep tags shared.

### Category
- Single most significant topic of the post.
- One concise noun / proper noun (e.g. `Terraform`, `Kubernetes`, `Productivity`,
  `Linux`, `Gaming`, `Blogging`, `Career`, `CI/CD`, `AWS`).
- Never generic: `Personal`, `General`, `Misc`, `Other`, `Various`.

### Image filenames (SEO)
- Non-SEO filenames include: random hash (`hG4xpm85JuI6ZdjFi.png`), UUID
  (`DD591F5C-9F96-48C7-A580-E832B4465153.png`), screenshot timestamp
  (`Screenshot_2021-04-26_at_16.48.17.png`), generic (`Untitled.png`,
  `Untitled 1.png`), or camera-roll (`IMG_0945.png`).
- SEO-friendly names: lowercase, hyphen-separated, descriptive of the image
  content, keep the original extension (e.g. `kubernetes-node-architecture.png`).
- Derive the new name from nearby text (headings, captions, surrounding
  paragraphs). Ensure uniqueness within the folder.
- Do **not** rename images that already have SEO-friendly names.

## 4. Procedure

1. Read all posts in `src/content/posts/`; build the tag frequency map.
2. Read the full content of each target post.
3. If `description` is empty/placeholder, write a new one (110–160 chars) from the
   post content.
4. Pick candidate tags from the content; keep only those that exist on ≥1 other
   post (frequency ≥2 after adding); cap at 5.
5. Set `category` to the most significant topic.
6. Update `description:`, `tags:`, and `category:` on the target post(s) using
   Edit/Write.
7. Remove any tags elsewhere that this change orphaned (now on a single post).
8. List the post's local image references (paths starting with
   `../../assets/images/`).
9. For each non-SEO image, derive a descriptive name and rename it with
   `git mv <old> <new>`, then update **every** occurrence of the old path in the
   markdown.
10. Verify the build still passes: `pnpm astro check` (and `pnpm astro build` if
    images moved).

## 5. Commit (if the user wants it committed)

```bash
git add -A
git commit -m "auto-enrich: update tags, category, description, and image names for <filename>"
```

## Notes

- This replaces `.github/workflows/auto-enrich.yml`; there is no longer a CI step
  doing this, so run the skill before publishing a post.
- Operate on the working tree with native Edit/Write and `git mv` — there is no PR
  or `ANTHROPIC_API_KEY` involved locally.
