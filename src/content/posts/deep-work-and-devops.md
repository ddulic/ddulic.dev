---
title: "Deep Work and DevOps"
published: 2021-06-08
description: ""
tags: [DevOps, Productivity]
category: Productivity
draft: false
---

:::warning
Rant Alert
:::

There has been something that has been on my mind for the past few months, it is hard to maintain "[the flow](https://www.youtube.com/watch?v=kj1hLFSORTQ)" in DevOps.

It seems to be easier for Developers (at least the friends and colleagues I talked to) as they usually work in one language, and they use fewer tools, not saying that it is easy, but it is easier to get and stay in "the zone".

Might be just me, but as I am getting older, I am finding it harder and harder to just sit down and focus on a task for a couple of hours.

---

I don’t know if I should blame Slack and the constant expectation that we should always be online, answering everyone's questions the instant we hear the ding.

Or is it just the plethora of tools I am exposed to as a “DevOps Engineer”:

- we have the Clouds: AWS, Azure, GCP. Depending on which company you work at it is mostly expected that you default to just knowing as much as possible about that cloud, you always have to keep learning, and they are constantly changing, not to mention the services unique to that provider...
- we then have the compute in the cloud, be in VMs, which usually require Linux experience, Kubernetes (I can go into a whole subset of tools on k8s that you need to keep up to date on such as Istio, external-dns, etc)
- you have the LBs such as Nginx, Kong, Apache (is this even still used? I still remember LAMP), AWS API GW, all of which are beasts on their own
- depending on what you do you also most likely have to script and code in bash, python, golang, node, Java? If not code, you are expected to know at least the bare minimum for these languages
- all of these tools require a profound understanding of the whole network stack, knowing the ins and outs of the wonderfully complex world of the internet, including DNS (something I don’t think I will ever truly fully understand)

I don’t want this to sound like I am [qqing](https://www.urbandictionary.com/define.php?term=qqing) (although I kind of am), I just want to show that pretty much anything we do will require some combination of the above tools, requiring you to usually constantly context switch back and forth between them, losing focus in the process

I wanted to write down all of this, so hopefully, someone who is having the same issue will stumble on this post, why? Because I want to share what I have realized.

---

After a lot of thought, experimenting with different approaches, I have realized that the issue was with me, that I needed to get better at planning, prioritizing, allocating time, communicating and documenting.

The annoying part is, it will be different for everyone. There is no magical "one-size-fits-all" approach to solving these problems.

Here are some of my tips on how you can regain your focus:

- work on 3 or fewer projects at a time (aka try and stop multitasking)
- block out time for deep work
- know what you will work/do that day (doesn’t always work if you are on support)
- structure the project/tickets in advance, using a tool like [Notion](https://www.notion.so/) to document your work, so everything is in one place (consider using [The Second Brain](https://fortelabs.co/blog/basboverview/) methodology)
- use tools like [Alfred](https://www.alfredapp.com/) on macOS and [PowerToys](https://docs.microsoft.com/en-us/windows/powertoys/) on Windows to not lose as much time

It will take time, but you will build up a flow that works for you.

Don't work on improving just the work you do, the tools and systems you have in place to manage your work matter just as much.

And as always, have fun. Our role gives us exposure to numerous cool tools to play around with 😄

> Once you stop learning, you start dying - Albert Einstein
