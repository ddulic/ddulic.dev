---
title: "Steam Remote Play with Linux Host"
published: 2023-08-22
description: ""
tags: [Linux, Steam, Gaming, Steam Deck, Streaming]
category: Gaming
draft: false
---

# Introduction

I have a problem… a real first world problem, I can no longer game with a mouse and keyboard at my desk. I can’t get detached enough to be able to relax, given that I also work at the same desk 😕

My solution? Stream the games from my PC. I find it is beneficial for several reasons:

- Allows for gaming on a larger screen, such as a TV
- Better graphics and a better battery life, especially when streaming to a device like the [Steam Deck](https://store.steampowered.com/steamdeck)

Low latency game streaming has come a long way in the last few years, on a good network, there is only a few ms of delay.

I will mainly be covering streaming to the Steam Deck, as that is my primary use-case. I like the additional touchpad support for [FPS](https://en.wikipedia.org/wiki/First-person_shooter) games, it offers the ability to play anywhere. It is my primary gaming device.

Now, I have done this in the past on Windows, and I have had a much better experience, having none of the headache around the setup and various issues mentioned in this post. Alas, I refuse to use Windows for numerous reasons and gaming on Linux has got a lot better over the past few years, mainly thanks to Valve pushing https://github.com/ValveSoftware/Proton and supporting tools.

That said, it isn’t without issues, especially when it comes to Steam. New features take a while to be  implemented on Linux without problems, one such example is [Transfer speed between two high-performance PC limited around 140 Mbps · Issue #9364 · ValveSoftware/steam-for-linux](https://github.com/ValveSoftware/steam-for-linux/issues/9364), it was faster for me to download the game again then transfer it over LAN.

Valve developers are active in the mentioned repo and over 7000 issues have already been closed off. It is refreshing to see how much Valve cares about Linux.

On to the post…

# Assumptions

I am making a few assumptions here, I have to because Linux is so vastly configurable, I am assuming that you

- have a fresh [Arch](https://archlinux.org/) installation, ideally [EndeavourOS](https://endeavouros.com/)
- are using [X11](https://en.wikipedia.org/wiki/X_Window_System), booting with [grub](https://en.wikipedia.org/wiki/GNU_GRUB) and [systemd](https://en.wikipedia.org/wiki/Systemd)
- posses a desktop with an Nvidia GPU
- are comfortable using a terminal and Linux in general

If your situation varies, please adapt the changes to your environment.

I will be using Steam Remote Play. Why not Sunshine and Moonlight, you ask, given the Nvidia GPU?

While they do offer better generally performance, especially at 4k, the solution is not native, and it is difficult to configure the controller settings, something that is a must for me as I use the touchpad and gyro on the Steam Deck quite often.

It also had its issues that I couldn’t find solutions for.

# Setup Steam

There is an excellent guide on how to do this over on the EndeavourOS Forums. The post can also be applied to Arch distros in general.

[Linux gaming [Guide]](https://forum.endeavouros.com/t/linux-gaming-guide/7339)

## Host


A small side note; I will be using the term Host and PC interchangeably in this post.

- [Set Steam to launch minimized](https://github.com/ValveSoftware/steam-for-linux/issues/6832#issuecomment-575690226) (`/usr/bin/steam-runtime -silent -gamepadui %U`)
- https://github.com/DavidoTek/ProtonUp-Qt⁣ – available as `protonup-qt` in AUR as you might want to switch Proton versions depending on the game
- [Patch the card to enable NVENC and NvFBC](https://github.com/keylase/nvidia-patch) and verify with [Verify-NVENC-patch](https://github.com/keylase/nvidia-patch/wiki/Verify-NVENC-patch). This change is required on every driver update!

    This isn’t required, as it doesn’t currently work - [Does NVFBC actually work on consumer level graphic cards on linux (Geforce)? · Issue #4811 · ValveSoftware/steam-for-linux](https://github.com/ValveSoftware/steam-for-linux/issues/4811), I haven’t checked it myself, but for some reason I keep enabling it after every driver update in the hopes that Valve decides to magically patch it. Below is an explanation of the different video encoding technologies that Steam can utilize

    [Explanation: NvFBC, NvIFR, NvENC :: Steam Remote Play](https://steamcommunity.com/groups/homestream/discussions/0/451850849186356998/#c451850849191050105)

- In Steam “Advanced Host Options” preferences, under Remote Play:
    - Disable “Play audio on host”, feel free to keep it on if you are a monster
    - “Enable hardware encoding”
    - Increase the “Number of software encoding threads” to `8`
    - Enable “Prioritize network traffic”

## Client


Make sure Remote Play is enabled in the settings. You will need to do an initial pairing. After that is done, configure the Remote Play Settings as follows:

- I have set “Video” to “Beautiful”. At the Steam Deck resolution, most networks should be able to handle this throughput
- “Enable hardware encoding” if your device supports it (at the time of writing this post, the Steam Deck doesn’t)
- “HEVC Video”  or [H.265](https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding) should be off, as of writing this post our Linux Host doesn’t support it

# Streambox

At this stage, you should be able to connect to your PC and stream games.

Let’s move on to configuring our PC to be more friendly to streaming.

## Install LTS Kernel

We want some stability, I always prefer to use a [lts](https://en.wikipedia.org/wiki/Long-term_support) kernel. This step is optional

```bash
uname -r # make sure you don't have an lts kernel already
sudo pacman -S linux-lts linux-lts-headers
sudo grub-mkconfig -o /boot/grub/grub.cfg # register with grub
```

I also like to keep the non-lts kernel around, just in case I there are useful fixes.

## Enable WOL

Not much use of if we need to walk over to the PC and turn it on every time. The Steam Link app supports waking up the PC, as for the Steam Deck, the solution is lower in this post.

Let’s enable [WOL](https://wiki.archlinux.org/title/Wake-on-LAN). I will be using [ethtool](https://archlinux.org/packages/?name=ethtool) for this purpose

```bash
ip address show # find your network interface
```

Mine is called `enp42s0`, so I will be using that interface going forward

```bash
ethtool enp42s0 | grep Wake-on # check if wol is already enabled
```

```bash
ethtool -s enp42s0 wol g # enable wol temporarily, reset on reboot
```

To make it permanent, create a systemd service and enable it

```
[Unit]
Description=Wake-on-LAN for %i
Requires=network.target
After=network.target network-online.target

[Service]
ExecStart=/usr/bin/ethtool -s %i wol g
Type=oneshot

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable --now wol@enp42s0.service
```

## Modify Grub Timeout

The default grub boot is usually far too long. I went for 2 seconds, enough to modify the entry if I run into issues and need to quickly get into a tty.

The shorter the timeout, the quicker your PC will boot from a cold start, duh.

You are welcome to use [Grub Customizer](https://itsfoss.com/install-grub-customizer-ubuntu/) or simply edit the file directly, modifying the obvious line

```bash
sudo vim /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg # save the config
```

## Modify Power Settings

There are a few settings that will prove troublesome, and we should disable them, such as

- Automatic sleep
- Automatic screen lock

Make sure to enable Suspend in your system if it isn’t enabled already!

These options will depend on your distro as to where they are located, they are often exposed somewhere in the settings GUI.

## Autologin

This is personal preference, lightdm supports enabling autologin, but the Security person in me isn’t ok with this. If you wish to enable it without any additional protections, look it up. Most display managers have something similar as well.

I am using a Security Key to make the login quicker, Xfce supports auto-unlocking the lock screen with the pam module, sadly the gtk-greeter that lightdm uses doesn’t - [Add config option to auto-start session with PAM by smanilov · Pull Request #127 · Xubuntu/lightdm-gtk-greeter](https://github.com/Xubuntu/lightdm-gtk-greeter/pull/127)

So I have to manually press the “Enter” key for now, at least until the above PR is merged and released.

# Squash Issues


This section will attempt to resolve the issues even with the games who don’t have the “Remote Play” flag enabled in Steam.

I have found that games who have that flag on have the least number of issues, mainly when it comes to adjusting the correct resolution and properly exiting a gaming session. This is most likely because the proper triggers are implemented as part of [ISteamRemotePlay Interface (Steamworks Documentation)](https://partner.steamgames.com/doc/api/ISteamRemotePlay).

There are a few historical issues that I have experienced, such as [Steam Remote Play drops to 30 fps when running games using Proton. · Issue #8423 · ValveSoftware/steam-for-linux](https://github.com/ValveSoftware/steam-for-linux/issues/8423), but as these have been fixed, I won’t be including them.

I wanted to use this section to go more into the issue and explain the solutions. All the proposed fixes are being triggered remotely, as explained in the “Manage PC Remotely” part of this post.

If you encounter other issues, I would recommend the page below as a good source of information

[Steam/Troubleshooting](https://wiki.archlinux.org/title/Steam/Troubleshooting)

## Host Widescreen

[Remote play frozen if resolution is fullscreen or too high on Linux Host · Issue #7130 · ValveSoftware/steam-for-linux](https://github.com/ValveSoftware/steam-for-linux/issues/7130)

---

This was my biggest pain point. I have a widescreen monitor, whose aspect ratio seems to cause many problems.

One immediate solution that comes up when searching is to use [gamescope](https://github.com/ValveSoftware/gamescope), but couldn’t hack it… when configuring it

- `gamescope -b` caused the controller not to work
- `gamescope` without `-b` caused crashes every 2nd run
- `gamescope -f` made the game not to start over Steam Link
- Changing desktop aspect ratio to 16:9 allows me to launch `gamescope` with `-f`, but the performance is the same, still 30 fps…

In the end, I ended up going with [autorandr](https://github.com/phillipberndt/autorandr).

We will be using this tool later on in the Manage PC Remotely section. Install and configure as follows:

1. Change Resolution to desired device
2. Run `autorandr --save <device>` to save that profile

You can also always just use `xrandr` directly, the underlying tool that autorandr uses.

## Sound on Host

[Steam Remote Play plays sound on both the client and the host, when the "Play sound on host" option is disabled. · Issue #6512 · ValveSoftware/steam-for-linux](https://github.com/ValveSoftware/steam-for-linux/issues/6512)

---

I have fixed this in a slightly unconventional way, not seeing a point in the monitor running at all, wasting power and generating heat. I opted for an HDMI Dummy Plug.

They are cheap, you can find them readily online. When buying, make note of the supported resolutions and refresh rates.

This introduces another set of issues. Steam has to be restarted to no longer detect the original resolution it was launched with. If we don’t do this, the Remote Play session can fail to adjust the resolution correctly on launch.

If using the DisplayPort Dummy Plug, configuring autorandr is a bit fiddly

1. Set the DP resolution under the Display Settings to either Steam Deck or TV
2. Open a terminal and have `autorandr --save sd` command ready to be executed
3. Temporarily disable the main monitor and double alt-tab to the terminal and press enter to execute the command
4. The settings should reset after 10 seconds, but the correct configuration should be saved

There is probably a better way to do this, possibly via the config files exposed at `$HOME/.config/autorandr`, but I couldn’t be bothered to figure it out, especially since the refresh rates seem to change with the resolution, making it hard to figure out the proper config.


# Manage PC Remotely

If you are like me, your Linux PC isn’t just for Streaming Games, you might want to occasionally want to use it like a PC, so most of the above fixes should be temporary or configurable, which is why we should have the ability to trigger them remotely.

There are a couple of prerequisites that we need to configure

1. Enable and start `sshd`

    ```bash
    sudo systemctl enable --now sshd
    ```

    Modify the [sshd_config](https://www.man7.org/linux/man-pages/man5/sshd_config.5.html) to

    - Remove password auth
    - Change the default port
2. Update the [sudoers](https://man.archlinux.org/man/sudoers.5) (`sudo visudo`) file to allow anyone in the wheel group to run sudo commands with no password.

    ```bash
    %wheel ALL=(ALL:ALL) NOPASSWD: ALL
    ```

3. Configure your host to have a Static IP

    This should ideally be done in the Router, but it can also be configured in the Network Manager.


---

Before you can use Remote Play, the game needs to be launched at least once on the PC because

- Custom game launchers might need configuring
- EULA acceptance requirement in Steam blocks Streaming

## Steam Deck Script

The Steam Deck can’t natively wake up the PC, unlike the Steam Link app, luckily, it runs Linux.

We can do almost anything, including adding a custom game that launches a script. I have shared mine at [steam-remote-play-linux](https://github.com/ddulic/steam-remote-play-linux/blob/main/manage_pc.sh) that does the following:

- Wake up the Host
- Set resolution to match the Steam Deck
- Restart Steam is not a fresh boot

It uses [zenity](https://help.gnome.org/users/zenity/stable/) and other tools that are available on the Steam Deck. Let’s set it up!

1. Boot into Steam Deck Desktop Mode (look up a guide on how to use Desktop Mode)
2. Open the Terminal Application
3. Download the file from GitHub and set it as an executable

    ```bash
    wget https://raw.githubusercontent.com/ddulic/steam-remote-play-linux/main/manage_pc.sh
    chmod +x manage_pc.sh
    ```

4. Add non-Steam Game
    1. There are plenty of guides online on how to do this
    2. Add the script required variables before the launch options
    3. `USER`, `IP`, and `MAC` (grabbed via `ip addr` on the PC)
5. Bonus: [Steam Deck Quickie: Setting All Five Custom Artworks for A Non-Steam Application/Game](https://www.youtube.com/watch?v=CJsoGik7hLo)

---

Simply launch the “game” from Steam and follow the on-screen prompts.

## Auto-Suspend Host

The beauty of the Steam Deck is being able to pick up and leave it, I still do that. It helps that with a decent desktop, entering and exiting games is quite fast, so we aren’t really missing the Steam Deck suspend feature (I suspect this is working on the Steam Deck because of gamescope as it is currently broken on Linux, there are plenty of issues open that relate to suspending/sleeping the PC, even without Remote Play. Maybe a future project?).

What I often forget is to suspend my PC after I am done playing, so I wrote a little bash script that can be added as a systemd service to help us with this.

Here's a brief summary of what the script does:

- Enters an infinite loop
- Checks which autorandr profile is currently loaded
- If the Steam Deck resolution profile is loaded, it checks if Steam is running
- If Steam is running, it starts a timer to suspend the PC after a certain amount of time
- If a Remote Play stream is started, the timer is reset, checking for `>>> Stopped desktop stream` the last couple of lines
- It will not automatically suspend if the Steam Deck resolution profile is not loaded

---

So, to set this up:

1. Clone the repository to `$HOME/opt`

    ```bash
    git clone git@github.com:ddulic/steam-remote-play-linux.git $HOME/opt/steam-remote-play-linux
    ```

2. `cd` into the root of the repo, symlink the systemd service to `/etc/systemd/system`


    ```bash
    systemctl link --user ${PWD}/auto-suspend.service
    ```

3. Enable, start and check the systemd service

    ```bash
    systemctl --user status auto-suspend
    systemctl --user enable --now auto-suspend
    ```

4. `daemon-reload` if you make/pull changes

    ```bash
    systemctl --user daemon-reload
    systemctl --user restart auto-suspend
    systemctl --user status auto-suspend
    ```


## Siri Shortcut

I created a shortcut that lets me:

- Wake up my PC
- Choose between PC (ultrawide), TV (1440p) or SD (1280x800) autorandr presets
- Restart Steam
- Sleep PC
- Shutdown PC

I wanted to share my shortcut, but as I have a key already generated, it looks like it would have shared it according to [PSA: Sharing a shortcut with the Run Script over SSH action will also share your SSH password or private key : r/shortcuts](https://www.reddit.com/r/shortcuts/comments/n6h08w/psa_sharing_a_shortcut_with_the_run_script_over/), beyond stupid, but it is what it is. Creating a new Shortcut uses the same values from the SSH action…

---

Instead, I will tell you the building blocks of the shortcut and let you manage it.

I am using an app called [Wolow](https://wolow.site) to simplify WOL on iOS (yes you can technically wake up over ssh alone, but enabling that flag in the WOL Host config caused my PC to be woken up randomly, probably from other devices on the network running discovery).

Once my device is added in Wolow, I use the Siri Shortcut actions it allows, along with the “Run script over SSH” built-in action. Below is a good guide on how you can set up the functionality, including generating and adding the key to your PC.

[Setting up SSH for Shortcuts](https://www.thoughtasylum.com/2020/06/01/setting-up-ssh-for-shortcuts/)

With the [Choose from Menu](https://support.apple.com/en-gb/guide/shortcuts/apdd7bf369da/6.0/ios/16.0) action, it was rudimentary to set up something similar to the Steam Deck Script, all the ssh commands are the same after all.

I would recommend looking at the guides by [u/keveridge](https://www.reddit.com/r/shortcuts/comments/al13xj/writing_functions/) over on Reddit, I find them really useful.

# Conclusion

In conclusion, streaming games from a PC has become a viable solution for those of us who cannot game at our desks. With low latency game streaming and the ability to play on larger screens, such as TVs, the experience has become much more enjoyable. While there are some issues that need to be addressed, especially when it comes to gaming on Linux, the benefits outweigh the challenges. As a passionate gamer, I am excited to see how game streaming technology will continue to develop and improve in the future.

Thank you for taking the time to read, hopefully it will provide some benefit.
