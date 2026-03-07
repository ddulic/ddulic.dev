---
title: "Book Notes: Site Reliability Engineering"
published: 2022-07-12
description: ""
tags: [Book Notes, Reliability, DevOps]
category: SRE
draft: false
---

Reading through the reviews on Goodreads, I am seeing countless people complain how the book is lacking details? The fact that they even shared this much is remarkable. I have accumulated 104 highlights, most of which, I believe, are useful.

The downside is that the book can be a bit of a dry read. It doesn’t follow the DRY (don’t repeat yourself) principle, but at the same time I think that might be a good thing as this book is about learning, and when it comes to learning, repetition is king.

Everything is a people problem to an extent, and this book attempts to solve reliability issues through a systematic approach to organizing teams and work.

Not every company will have the same scale issues Google has, and this might be more applicable to companies that utilize data centres directly instead of using a Cloud Service.

# 🎨 What are my 3 Key Takeaways?

- Focus on simplicity from day one, a “a complex system that works necessarily evolved from a simple system that works”
- There has to be a balance between “ops work” (tickets, on-call, manual tasks, etc) and “feature work” (improving reliability, performance, utilization)
- Keep asking questions, about systems, about processes, about everything

# 🤔 3 Questions to Answer Before Reading

- Are you curious what SRE is all about?
- Does your organization have a reliability problem?
- Are you interested in building more reliable systems?

# ✍️ 3 Questions to Answer After Reading

- What are the actions you can take to help your organization implement/improve SRE?
- Are you successfully avoiding over-engineering?
- Are you doing postmortems correctly and efficiently?

# ✏️ Favourite Quotes

Apologies for the long list, but it was impossible to keep the number of favourite quotes low due to the large number of highlights 😕

---

> Monitoring should never require a human to interpret any part of the alerting domain. Instead, software should do the interpreting, and humans should be notified only when they need to take action.
>

> A key principle of any effective software engineering, not only reliability-oriented engineering, simplicity is a quality that, once lost, can be extraordinarily difficult to recapture. Nevertheless, as the old adage goes, a complex system that works necessarily evolved from a simple system that works.
>

> Understanding how well a system is meeting its expectations helps decide whether to invest in making the system faster, more available, and more resilient. Alternatively, if the service is doing fine, perhaps staff time should be spent on other priorities, such as paying off technical debt, adding new features, or introducing other products.
>

> The four golden signals of monitoring are latency, traffic, errors, and saturation. If you can only measure four metrics of your user-facing system, focus on these four.
>

> The global computer is — it must be self-repairing to operate once it grows past a certain size, due to the essentially statistically guaranteed large number of failures taking place every second. This implies that as we move systems up the hierarchy from manually triggered, to automatically triggered, to autonomous, some capacity for self-introspection is necessary to survive.
>

> Blameless culture originated in the healthcare and avionics industries where mistakes can be fatal. These industries nurture an environment where every “mistake” is seen as an opportunity to strengthen the system. When postmortems shift from allocating blame to investigating the systematic reasons why an individual or team had incomplete or incorrect information, effective prevention plans can be put in place. You can’t “fix” people, but you can fix systems and processes to better support people making the right choices when designing and maintaining complex systems.
>

> SREs are often generalists, as the desire to learn breadth-first instead of depth-first lends itself well to understanding the bigger picture (and there are few pictures bigger than the intricate inner workings of modern technical infrastructure).
>

> The forces of data freshness and restore completion compete against comprehensive protection. The further down the stack you push a snapshot of your data, the longer it takes to make a copy, which means that the frequency of copies decreases. At the database level, a transaction may take on the order of seconds to replicate. Exporting a database snapshot to the filesystem underneath may take 40 minutes. A full backup of the underlying filesystem may take hours.
>

> The aspects of your recovery plan you should confirm are myriad: Are your backups valid and complete, or are they empty? Do you have sufficient machine resources to run all of the setup, restore, and post-processing tasks that comprise your recovery? Does the recovery process complete in reasonable wall time? Are you able to monitor the state of your recovery process as it progresses? Are you free of critical dependencies on resources outside of your control, such as access to an offsite media storage vault that isn’t available 24/7?
>

> Polarizing time means that when a person comes into work each day, they should know if they’re doing just project work or just interrupts. Polarizing their time in this way means they get to concentrate for longer periods of time on the task at hand. They don’t get stressed out because they’re being roped into tasks that drag them away from the work they’re supposed to be doing.
>

> A production platform with a common service structure, conventions, and software infrastructure made it possible for an SRE team to provide support for the “platform” infrastructure, while the development teams provide on-call support for functional issues with the service — that is, for bugs in the application code. Under this model, SREs assume responsibility for the development and maintenance of large parts of service software infrastructure, particularly control systems such as load shedding, overload, automation, traffic management, logging, and monitoring.
>
