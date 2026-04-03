—
title: “Back to Blogging: How AI Simplified My Migration”
published: 2026-04-03
description: “How AI tools like Claude Code made migrating a blog from Notion to GitHub Pages fast, enabling a return to blogging with minimal technical friction.”
tags: [Blogging, Migration, Notion]
category: Blogging
draft: false
—

Hello all, it has been a long time since I last published a post. I’ve had quite a few life events that forced me to reflect on what I was doing, and I didn’t feel like posting anything—partially because I wasn’t doing anything interesting.

Another thing that discouraged me from posting was the fact that I had moved away from using Notion, and my blog was still stuck there (see [Why I Migrated My Blog to Notion (Using Super)](https://ddulic.dev/posts/why-i-migrated-my-blog-to-notion-using-super)).

I had it on my backlog to migrate my blog to [GitHub Pages](https://docs.github.com/en/pages). It is currently free, and if that ever changes, I can always migrate to a similar solution. I was too locked into Notion, and the ease of publishing wasn’t worth the vendor lock-in. I was dreading the change, though...

Until the latest generation of AI came along. I downloaded the blog content zip from Notion, passed it to what I was using at the time—Claude Code (experimenting with Mistral Vibe now)—and told it to migrate my blog. The prompt was much larger, but you get the idea. I was shocked at how effective it was. Don’t get me wrong, it made quite a few mistakes, but after less than an hour, my blog was up and running locally with all the posts migrated. This would have taken me a few hours just to migrate the posts, let alone set everything up.

One of the reasons I switched from Hexo and Hugo back in the day was that I didn’t want to mess around with HTML, CSS, JS, or any framework. I don’t care about those technologies, and I don’t want to spend an hour figuring out how to center a div. Making these types of small tweaks with AI is easy, and it does them quickly. I’ve gone full circle.

Another thing I disliked was all the SEO and categorization. I just want to write and not think about those things. Well, that is also straightforward now with a custom workflow—[auto-enrich.yaml](https://github.com/ddulic/ddulic.dev/blob/main/.github/workflows/auto-enrich.yml).

The test was successful. AI can be a force for good, allowing us to spend time doing things we want instead of wasting hours trying to figure something out that will likely be replaced in a few years. If that happens, migrating is easy now. We just have to adapt our workflows and learn its ways.

Expect more posts on AI. I have quite a few thoughts. I will use AI for inspiration and suggestions, but all text is 100% mine (well maybe not the title depending on my mood, naming stuff is hard). I’m not looking to add more unoriginal AI slop to this world.