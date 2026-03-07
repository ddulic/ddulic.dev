---
title: "Plex Anime Setup"
published: 2017-06-20
description: ""
tags: [Plex, Anime, Linux, Media Server]
category: Media
draft: false
---

---


This guide will require a few things:

1. Plex - Just download plex and install it with your preferred package manager.
2. Basic command line understanding; or not? - I will make this as much copy-paste as possible, but your config will vary. This will, of course, be a guide for Linux, but all of this should also be possible to do on Windows.
3. Anime. Which you probably already have if you are looking at this :D

I first tried this setup on a Raspberry Pi 3, but it failed to transcode the subtitles and send them over to my Chromecast, so I had to move over to something beefier, which is my desktop PC. If you just want to do streaming without the need for transcoding, however, the Pi will work just fine ^_^

Full credit to the reddit user [Shuffleshoe](https://www.reddit.com/user/Shuffleshoe) for writing this guide, this is a continuation/modification of that. The original post can be found [here](https://www.reddit.com/r/PleX/comments/2yk49z/guide_plex_and_anime_a_guide_to_combining_movies).

# **Anime from External Storage**

If you are like me, you keep most of your anime on a larger external HDD, we can also make that talk to Plex easily under Linux. If your HDD is formatted in NTFS, you will also need to install an additional `ntfs-3g` package in order for this to work. Then edit `/etc/fstab` and add below at the end

```
/dev/disk/by-uuid/<YOUR EXT HDD UUID> /home/user/WD ntfs-3g nosuid,nodev,nofail,x-gvfs-show 0 0
```

After you can check if the configuration is correct with

```bash
sudo mount -a
```

If there are none, our drive is now mounted on the desired mount point and, since it's in the fstab file, it will mount on every boot.

# **Scanner and Agent**

We need to scan the anime we have, the normal TV/Movie scanner and agent won't do it for us since it doesn't have all the anime info that we need. In case you don't know what a scanner is, you can find more info [here](https://support.plex.tv/hc/en-us/articles/200241548-Scanners), but TLDR, they just search your directory and files in an attempt to match them in their database, so they can serve you the relevant info, like the year it came out, short description, proper images and the actors.

On Ubuntu and Solus, the two distros I tested on, Plex was located at the same location. `/var/lib/plexmediaserver`, but your location will vary, please check where Plex is installed and modify the command below accordingly. If you don't know how to find it, check the locations [here](https://github.com/ZeroQI/Hama.bundle#installation). Copy and paste the commands below if you are on an Ubuntu-based distro. Oh... and make sure you have git installed :)

```bash
sudo apt install git
```

# [**Scanner**](https://github.com/ZeroQI/Absolute-Series-Scanner)

```bash
sudo su
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners/Series'
wget -O '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners/Series/Absolute Series Scanner.py' https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/Scanners/Series/Absolute%20Series%20Scanner.py
chown -R plex:plex '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners'
chmod 775 -R '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners'
```

# [**Agent**](https://github.com/ZeroQI/Hama.bundle)

```bash
service plexmediaserver stop
cd '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins'
git clone https://github.com/ZeroQI/Hama.bundle.git
chown -R plex:plex '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/Hama.bundle'
chmod 775 -R '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/Hama.bundle'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners/Series'
wget -O '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners/Series/Absolute Series Scanner.py' https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/Scanners/Series/Absolute%20Series%20Scanner.py
chown -R plex:plex '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners'
chmod 775 -R '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/AniDB'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/Plex'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/OMDB'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TMDB'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/blank'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/_cache/fanart/original'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/episodes'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/fanart/original'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/fanart/vignette'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/graphical'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/posters'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/seasons'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/seasonswide'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/TVDB/text'
mkdir -p '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama/DataItems/FanartTV'
chown -R plex:plex '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama'
chmod 775 -R '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.hama'
service plexmediaserver restart
```

### **Folder and File Structure**

If you are not certain how to name your folders, search for your show on [anidb](http://anidb.net/) - this is where the agent is pulling data from. You will potentially have to do a manual match on a few shows, even then, it might fail to fetch a poster, which can be quite annoying, so for these shows just download the poster from somewhere online and attach it to the show from the dropdown menu under that show.

For series, if an anime has more than 1 season, create a directory for each season under the main folder, like so:

```
Shingeki no Kyojin
├── Season 1
│   ├── Shingeki no Kyojin - 01.mkv
│   ├── Shingeki no Kyojin - 02.mkv
│   ├── Shingeki no Kyojin - 03.mkv
│   ├── Shingeki no Kyojin - 04.mkv
│   └── ...
└── Season 2
    ├── Shingeki no Kyojin - 26.mkv
    ├── Shingeki no Kyojin - 27.mkv
    ├── Shingeki no Kyojin - 28.mkv
    ├── Shingeki no Kyojin - 29.mkv
    └── ...

2 directories, 38 files
```

For movies, if a series has multiple movies, split them up into their own folder. In the reddit post the [OP](https://www.reddit.com/r/AskReddit/comments/4roags/what_does_op_mean/d52ppma) gives Evangelion to describe the optimal film folder structure:

Example: Neon Genesis Evangelion. It has a show, a film that's the conclusion of the show, and 3 separate movies that retell the story differently.

It's possible some movies with multiple parts (like a trilogy) can only be matched correctly when putting under one entry. This happened to me with the Madoka movies, I think. So, you can do this, or you can use "fix incorrect match" with another scanner. This seldom happens, though.

In the end, your structure will involve experimentation to see what works for you, but the result is worth the time investment :)

### **Add Anime to Plex**

Create a new TV Shows library in Plex and select the folder where all your anime is kept. **IMPORTANT:** Before adding the library, go into “Advanced” and change the **Scanner** to Absolute Series Scanner and the **Agent** to HamaTV and you can keep the rest as default. If you want, you can also change the languages all the way at the bottom, but I like to keep the defaults.

Enjoy watching anime (/^▽^)/
