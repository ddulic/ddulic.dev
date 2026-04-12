---
title: “The Good, the Buggy, and the Unfinished: Testing Mistral Vibe”
published: 2026-04-12
description: “First impressions of Mistral Vibe after dozens of coding hours, highlighting bugs, memory gaps, stability issues, and how it compares to Claude Code.”
tags: [Productivity, DevOps]
category: AI
draft: false
---

After using Mistral Vibe for a few dozen hours, I can say it’s not yet as polished as Claude Code, the last coding tool I used.

I’m using devstral-2, their highest-tier coding model, and there are several quirks I haven’t seen elsewhere. For example, it failed a precommit hook and got stuck in a loop. Instead of resolving the issue, it just removed the test entirely—something it absolutely shouldn’t do. If it’s not doing that, it’s failing to pull PR checks properly, even after I mentioned how to do it multiple times, it just doesn’t want to use the GitHub API or CLI effectively. Instead, it fetches entire web pages—up to 10,000 characters—by passing an auth header and analyzing the raw output. While it’s technically impressive to parse that much data, it’s a complete waste of tokens. Mistral’s limits seem higher or possibly unlimited, but I haven’t hit a cap yet, even after quite long sessions.

Its memory isn’t as strong as Claude Code’s or even Copilot’s, which at least asks if you want to store something to memory. Mistral Vibe doesn’t seem to retain or use context as reliably. Another weird thing it does is ignore command exit codes. I ran a test that returned exit code 128, and it treated it as fine because there was output. It should check whether a command actually succeeded before proceeding.

There are also stability issues. Sometimes it hangs on a command for five minutes with no output. Other times, it just stops mid-execution without warning. My terminal (Konsole on KDE) slows down noticeably with Mistral Vibe, which doesn’t happen with other models.

Many of these issues will likely be fixed in future updates, and they might already be working on patches. I could check the repository for existing issues, but given how quickly things move, it’s probably not worth the effort—what’s broken today might be fixed in a week. If I see the issues persist, I’ll raise issues in their GitHub repository.

For the price, it’s not quite worth it yet, even with no throttling. The weekly token allocation assumes 20-25 hours of coding, but nobody codes full-time at that pace. It’s a shame because the potential is there—it just needs more refinement.

That said, I’ll give it another month. It’s a capable model, and I can see the reasoning behind its actions. It just needs that extra layer of guidance that Claude Code has, whether through better skill triggers or more refined error handling. Right now, it handles about 80% of tasks correctly but lacks that final polish.