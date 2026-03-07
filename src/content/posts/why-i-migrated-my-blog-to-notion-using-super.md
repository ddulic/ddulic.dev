---
title: "Why I migrated my Blog to Notion (using Super)"
published: 2021-01-31
description: ""
tags: [Notion, Blogging, Productivity]
category: Productivity
draft: false
---

"Everything is a balance of time, money, and units of joy."

It should be easy to add content to a website, it shouldn't be a struggle. My previous workflow had issues that I had to solve.

---

Many of you will have noticed that my website looks and performs quite different. Many of you will also notice that it looks like [notion.so](http://notion.so), and the reason is that my website is now using Notion as the [CMS](https://en.wikipedia.org/wiki/Content_management_system).

How did I do this?

I am using [super.so](https://super.so?via=ddulic) to host my website statically and improve upon the Notion pages.

"Super turns your Notion pages into fast, functional websites with custom domains, fonts, analytics, and more."

As the above quote states, it just adds the missing layers on top of Notion that would allow you to properly host a website.


![](../../assets/images/why-i-migrated-my-blog-to-notion-using-super/86E4AB63-F866-4E53-BF99-CAA40D8724E6.png)

There are a couple of reasons why I decided to do this.

1. I use Notion for everything already, so why not as a CMS for my website, given that it is plausible.
2. Easier updates!

    ![](https://media.giphy.com/media/NaboQwhxK3gMU/source.gif)

    - A few years ago it made sense for me to show off my DevOps skills and create a website that showcased my understanding of git, AWS, CI/CD and other DevOps related skills, I think I am now at the point in my career where my experience shows for itself.
    - I want to write more and have caught my self refraining from doing so because updating and adding a new post has become a hassle. I would like to break down barriers and make it easier to add new posts and update old ones.
    - Furthermore, I commit multiple times a day at work, and I got sick of having to make commits to publish/update posts. I managed to make it more efficient by using GitHub Actions, but it just wasn’t quick enough to publish/update a post.
    - Updates to my website in Notion take less than 10 seconds to in order for the change to be visible on the [super.so](https://super.so?via=ddulic) static website.
    - All of the above results to almost 0 upkeep.
3. I kind of like the Notion design anyway, plus it gives me much more flexibility over the design of posts when using it as a CMS.
4. Lower costs!

    “But I took a look at [super.so](https://super.so/?via=ddulic) it costs more than your previous setup”

    True, but I save a lot of time (see other reasons). My time to me is worth more than the price difference. I also managed to lock in a lower price as an “early adopter”, let’s see how long that lasts...


Those are all the pros, let’s take a look at some cons.

Using Notion for my blog isn’t perfect, I like to write on my iPad and there are some issues with this, and my main gripe with Notion is that their iPad app isn’t the best... it works, and it works OK, but it can be better.

How can something so fundamental as copy-paste [not work](https://twitter.com/_ddulic/status/1328272880711430144)? And why can’t I view the full Notion website when I visit it in a browser? They basically just show the same UI as the iPad app... I guess this has something to do with how the web-native app is built...

[super.so](https://super.so/?via=ddulic) is still new, although they keep adding new features almost every week, some of the issues I have experienced so far are:

- The dashboard experience can be better, especially when adding custom code is extremely clunky
- Doesn't support database views and thus custom filters, as it strips the anything after a `?` in the URL when adding a "Pretty URL", making it impossible to have everything in one database and use filters to control different views (this is why I have "Latest Posts" and "Older Posts" databases).
- No easy dark theme support at the time of writing (they have [guides](https://super.so/guides/colors) on how you can change the colours, but for some reason, this doesn't work for me and I would prefer if the users could have a toggle to choose the theme, just like [fruition](https://fruitionsite.com)).
- As every change is almost immediately picked up by Super, there is a chance users can view your website while you are in the process of making a change to it and think your website is a mess or incomplete.

:::note
Update: I made a [post](https://community.super.so/c/showcase/why-i-migrated-my-blog-to-notion-using-super) on the Super Community and the co-founder replied the same that stating that they will fix most of the drawbacks in the next release!
:::

[super.so](https://super.so/?via=ddulic) can’t compare to a fully customizable website, but this is a compromise I am OK with.

If you want, you can copy most of the layout I have by just taking a look at how it looks directly in Notion, bypassing [super.so](https://super.so/?via=ddulic) - [https://www.notion.so/ddulic/dev-urandom-a87599b01bef4817a96ec9d95806839d](https://www.notion.so/a87599b01bef4817a96ec9d95806839d?pvs=21) (the page has to be public for Super to pick it up).

![](https://media.giphy.com/media/3o7TKS0OxsooHm8Wm4/giphy.gif)

---

Super also just published the below video, which gives you a good overview of how it works.
<iframe width="100%" height="468" src="https://www.youtube.com/watch?v=1zWiz7xL3q0" title="YouTube video player" frameborder="0" allowfullscreen></iframe>

---

Liked the post? Interested in more? Follow me on [LinkedIn](https://www.linkedin.com/in/ddulic/)

Until next time, take care and stay safe!
