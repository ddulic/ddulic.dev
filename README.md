# ddulic.dev

Personal blog of [Damir Dulic](https://github.com/ddulic) — `/dev/urandom/v4`.

Built with [Astro](https://astro.build), [Tailwind CSS](https://tailwindcss.com), and the [Fuwari](https://github.com/saicaca/fuwari) theme.

## Commands

All commands are run from the root of the project:

| Command                    | Action                                        |
|:---------------------------|:----------------------------------------------|
| `pnpm install`             | Install dependencies                          |
| `pnpm dev`                 | Start local dev server at `localhost:4321`    |
| `pnpm build`               | Build production site to `./dist/`            |
| `pnpm preview`             | Preview build locally before deploying        |
| `pnpm check`               | Run Astro checks for errors                   |
| `pnpm format`              | Format source code using Biome                |
| `pnpm lint`                | Lint and auto-fix source code using Biome     |
| `pnpm new-post <filename>` | Scaffold a new post in `src/content/posts/`   |

## New Post Frontmatter

```yaml
---
title: Post Title
published: 2026-01-01
description: A short description of the post.
image: ./cover.jpg
tags: [Tag1, Tag2]
category: Category
draft: false
---
```
