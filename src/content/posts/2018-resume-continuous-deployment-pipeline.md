---
title: "2018 Resume Continuous Deployment Pipeline"
published: 2018-03-11
description: ""
tags: []
category: DevOps
draft: false
---

---


# **Introduction**

In my [2018 Website Continuous Deployment Pipeline](https://github.com/ddulic/damir.tech/blob/master/posts/2018-website-pipeline) I forgot to include one crucial part of my website - my [Resume](https://damir.tech/resume/) Page.

I wanted a fresh resume. My previous were total and utter rubbish regarding formatting and readability, so it was time for a new one. I was also getting sick of editing my resume page and forgetting to update my PDF resume, and vice versa, I needed a way to edit once and update both my resume page on my website and my resume PDF.

# **Solution**

Only 2 requirements had to be fulfilled:

- the generated PDF had to be readable and clean
- there had to be an option to generate from Markdown

I stumbled upon a python tool called [grip](https://github.com/joeyespo/grip) which can generate a `.html` page from a markdown file, and I also knew of a tool to generate a `.pdf` from a `.html` named [wkhtmltopdf](https://github.com/wkhtmltopdf/wkhtmltopdf). So, my first idea was to somehow use these two to generate a PDF, but I ran into too many issues and decided to pursue another route.

[markdown-resume](https://github.com/there4/markdown-resume) was the solution. It satisfies all my requirements and adds multiple themes as an extra. This along with [travis ci](https://travis-ci.org/) seemed to offer me everything I required.

# **Flow**

To sum up the general workflow of adding and editing my resume

- `git push` locally edited page to my GitHub [resume](https://github.com/ddulic/resume) repo
- Travis CI is set up to watch the repo and on a commit execute the build details in `.tavis.yaml` in the root of the project
- Travis adds the header and footer, as well as the download button, needed for the page to be full
- Travis generates the `.pdf` from the markdown file and pushes them to [hexo-website](https://github.com/ddulic/hexo-website) which triggers the repo's Travis build

# **Setup**

Just as in my last post, everything is open and can be found on my GitHub, along with the basic understanding of how everything works which is explained in this post you should have no problem 1:1 copying and modifying to fit your needs.

## **AWS**

Unlike the last part, the AWS setup requires the least work and explanation, since it just hooks into the previous AWS setup.

## **Docker**

~~I was in the process of containerizing various services at my job, so why not containerize markdown-resume while at it. After all, practice makes perfect :)~~

~~But it was easier said than done... markdown-resume is in PHP and I had some formatting issues in the resulting PDF. It's been years since I touched PHP to be able to fix it myself, luckily someone helped me with my [issue](https://github.com/there4/markdown-resume/issues/65).~~

~~The final Dockerfiles can be found in my [fork](https://github.com/ddulic/markdown-resume) of the project, which includes the fixes described above.~~

Update: [markdown-resume](https://github.com/there4/markdown-resume/blob/master/Dockerfile) now have their own Dockerfile, so I am using that now.

# **Final Thoughts**

It is so relaxing to be able to edit once and update both my resume PDF and my resume page. The next step is to update my LinkedIn profile via [api](https://developer.linkedin.com/docs/guide/v2/people/profile-edit-api#) 🤔

---


---
