---
title: "Free Gmail Custom Domain"
published: 2016-05-27
description: ""
tags: [Email, Gmail, DNS, Custom Domain]
category: DevOps
draft: false
---

Setting up a mail server can be tricky and there are far too many places where you can make a stupid mistake that will end up in you not receiving email, no one wants that. Here is a quote from [@Kernellinux](https://twitter.com/Kernellinux) from [The Linux Action Show‘s](https://itunes.apple.com/us/podcast/the-linux-action-show!-hd/id505494738?mt=2) latest episode:

> If you’ve ever run your own email server, that is enough experience for you to know that you’ll never want to run your own email server, and if you think you want to run your own email server it's because you’ve never run your own email server.
>

So, an alternative is to use something like [protonmail](https://protonmail.com/) or [gmail](https://mail.google.com/) and add a custom domain, but in both of the services I listed that requires paying, it’s not much (minimum \$5), and even then, it isn’t perfect. I wanted to use [protonmail](https://protonmail.com/) at first, and even bought a month to test it out, but the lack of some features – like importing mail and custom folders drew me away – maybe I will check it out in the future because they are becoming better and better by each passing day. - **Update 2017: Now using it :)**

Moving on to gmail. If you want a custom domain you will have to buy Google Apps For Work, which costs $5 a month, but in doing so, I would have to re-import everything and start over and slowly change all of my emails on various services and websites to my new email. I know I can use forwarding, but that just wasn’t clean enough for me, I wanted a better solution. Why couldn’t I just use both, that was what I wanted to do on protonmail. So, after a bit of searching, I found how to do it in gmail.

![](../../assets/images/free-gmail-custom-domain/gmail_custom.jpg)

Thanks to [this](https://www.reddit.com/r/Entrepreneur/comments/3y7nve/use_gmail_to_send_email_from_custom_domains_for) reddit post for the idea and guide. I will be iterating and adding something of my own in this how-to.

![](../../assets/images/free-gmail-custom-domain/gmail_custom_domain.jpg)

What we will need:

- Access to your DNS Control Panel for the custom domain you wish to use
- Mailgun free account
- Gmail account? (❍ᴥ❍ʋ)

So, the way this works is we will be adding our custom domain via the alias feature inside gmail. The alias will be done via [SMTP](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol).

I will be using [Mailgun](https://www.mailgun.com/), but you can use other similar services. It gives us 10k emails a month, which is more than enough, I think. When signing up be sure to use the @gmail email address you are using at the moment!

Adding a domain to Mailgun is simple, follow the DNS instructions and add the records within the service that manages your DNS.

Once that is done, move on to gmail. Find alias under Settings/Accounts and Import, click on the Add another email address you own. In the popup window, fill in the info and make sure that “Treat as an alias” is checked. In the next part, use:

- Server: `smtp.mailgun.org`
- Port: `587`
- Username: the full email address, e.g. `me@example.com`
- Password: the password you set in mailgun SMTP Credentials (the password is a long string containing 32 characters, not to be mistaken with your mailgun password)

And there you go, your alias is set up 😸

To enable some additional gmail and google+ features add your new email address to google+and after a short delay your google+ picture will be connected to your new custom domain, something that is not possible if you use your own email server, also all the gmail features such as anti-spam also work, not to mention that you can reply to all your emails sent to your old address with your new custom domain email, how cool is that ＼（＾ ＾）／
