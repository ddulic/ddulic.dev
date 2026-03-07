---
title: "I switched to Markdown"
published: 2017-08-06
description: ""
tags: [Blogging]
category: Blogging
draft: false
---

# **The Why**

I needed to organize my files somehow. I had documents in:

- .docx
- .md
- .txt
- .odt
- .html
- .pages

It was a mess which had to be cleaned and sorted.

Markdown is already widely used, and it's being adopted more and more. It was the format I could make the most use at my job.

Where I can use it:

- GitLab, GitHub, git README.md in general
- Work documentation, which can then easily be copied to a wiki
- This website. It now runs on ghost.

Markdown has an almost unified standard, except that everyone has their own variation, but most of it is the same.

It's prettier. Formatting, formatting, formatting.

Better readability without the need for heavy programs. It's light AF.

Easy copy-paste to a formatted structure from Chrome via [Chrome template extension](https://chrome.google.com/webstore/detail/template/dcjnfaoifoefmnbhhlbppaebgnccfddf). This means I can write the same documentation everywhere and just copy and paste. No more messing around to adapt the formatting.

If you are using [atom](https://atom.io/) it has a few plugins that make writing in .md easier.

# **The How**

I used Nextcloud, and it was OK, but it was too heavy for what I required, and I wanted to get rid of PHP altogether.

I started searching for replacements, looking at various online markdown editors, but none of them worked for me. So, I decided to mix it up. Introducing [Jupyter](http://jupyter.org/) + [Syncthing](https://syncthing.net/).

A combination of these 2 services allows me to achieve everything I wanted; store contents online, which I can now also sync with all my machines and even my phone with syncthing and edit them online if I need to at work with Jupyter.

## **Ghost Setup**

### **Install dependencies**

~~Ghost runs on NodeJS, so we need to install it. In my experience, this is easiest to do with [nvm](https://github.com/creationix/nvm). Just run the `wget` or `curl` scripts from the [install](https://github.com/creationix/nvm#install-script) section on their GitHub. Once that is installed `source` the `.bashrc` and install the latest stable nodejs with~~

```bash
nvm install `nvm ls-remote --lts | grep "Latest LTS: Argon" | awk '{ print $1}'` && nvm use nodeba
```

T~~his will list and find the recommended NodeJS version as of writing this, install it and activate.~~

### **Install Ghost**

~~(you can use [this](https://docs.ghost.org/v1.0.0/docs/installing-ghost-via-the-cli) guide to install it via CLI if you want v1)~~

### **Setup Ghost as a forever service**

~~Inside `start-ghost.sh`~~

```bash
#!/bin/bash
export PATH=/home/ddulic/.nvm/versions/node/v6.11.0/bin/
cd /var/www/ghost
#export NODE_ENV=production
NODE_ENV=production forever -a -l /var/log/ghost start --sourceDir /var/www/ghost index.js
```

~~After that do `crontab -e` and add `@reboot /home/user/ghost-start.sh` at the bottom to start your blog with the forever service at every boot.~~

### **Nginx**

~~Paste the following inside `/etc/nginx/sites-available/ghost` to enable https, this also enables you...~~

```
nginx code was here :O
```

### **Letsencrypt**

~~letsencrypt via letsecnrypt~~

- `~~sudo apt install letsencrypt~~`
- `~~sudo letsencrypt certonly --standalone --webroot-path=/var/www/ghost -d example.com~~`

~~Generate [DH parameters](https://wiki.openssl.org/index.php/Diffie-Hellman_parameters) `sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048`~~

### **Ghost 1.0 -.-'**

With the release of [Ghost 1.0](https://blog.ghost.org/1-0/) it's no longer complicated to install and configure ghost. Follow their [installtion docs](https://docs.ghost.org/docs/install) and if you wish to migrate to 1.0 check out [this](https://docs.ghost.org/docs/migrating-to-ghost-1-0-0).

## **Jupyter**

Install [Jupyter notebook](https://github.com/jupyter/notebook).

### **Configure Jupyter**

- generate password file with `jupyter notebook password`
- generate the config file with `jupyter notebook --generate-config`

Edit the `.jupyter/jupyter_notebook_config.py`: and change the following to your preference

```
c.NotebookApp.base_url = '/files/' # changes our base url, I didn't like the /ipython...
c.NotebookApp.trust_xheaders = True # needed for nginx
c.NotebookApp.open_browser = False # since we aren't running on localhost we don't need a browser which will open when we load jupyter
c.NotebookApp.tornado_settings = {'static_url_prefix': '/files/static/'} # same as base_url, but used for static files
c.NotebookApp.default_url = '/tree/Sync/Ghost' # change to our default directory so we don't have to go to it every time we open jupyter
```

### **Nginx**

Add the following code to `/etc/nginx/sites-available/site` under the https server block

```
location /files { proxy_pass http://localhost:8888; proxy_set_header Host $host; proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "upgrade"; proxy_set_header Origin ""; }
```

### **Systemd config**

Create a systemd startup script by creating a `jupyter.service` file in `/etc/systemd/system` with the following content:

```
[Unit]
Description=Jupyter Notebook

[Service]
Type=simple
PIDFile=/var/run/jupyter-notebook.pid
User=user
Group=user
ExecStart=/home/user/.local/bin/jupyter notebook
WorkingDirectory=/home/user
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable & Start Jupyter

```bash
sudo systemctl daemon-reload
sudo systemctl start jupyter
sudo systemctl enable jupyter
```

There are a few [themes](https://github.com/dunovank/jupyter-themes) you can install. Personally, I like everything to be dark, so I decided on the oceans16 theme. Follow the instructions on the GitHub page on how to install and configure. I also enabled the logout button with `jt -t oceans16 -T -N`, since by default for reasons its disabled.

Now it's time to convert our notebook into a markdown editor. Luckily, there is a plugin which can do this for us - [ipydm](https://github.com/rossant/ipymd).

When creating a new file; `code` is the default parser, we want this to be `markdown`. Go to the `site-packages` directory of your python environment and modify `site-packages/notebook/static/notebook/js/main.min.js`. For me, it's `.local/lib/python3.5/site-packages/notebook/static/notebook/js/main.min.js`. Find `Notebook.options_default` and change `default_cell_type: 'code'`into `default_cell_type: 'markdown'`.

This isn't perfect. Editing a markdown which is divided by cells can be annoying, and I still don't understand how cells work, and saving a file also creates an additional hidden .checkpoint file. If anyone knows how to fix this, feel free to commend below :)

## **Syncthing**

If you are on Debian/Ubuntu, it's recommended to install via the [syncthing repo](https://apt.syncthing.net/).

Once that is done, we just have to set up a [reverse proxy](https://docs.syncthing.net/users/reverseproxy.html). However, the previous instruction doesn't work for me, and I have no idea why. This config, however, works:

```
location /syncthing/ { proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto $scheme; proxy_pass https://localhost:8384/; proxy_read_timeout 600s; proxy_send_timeout 600s; }
```

And that is it. You can now configure syncthing under `example.com/syncthing` [here](https://www.youtube.com/watch?v=iFh27uPsYRw&t) is a good getting started with syncthing.

Enjoy :)
