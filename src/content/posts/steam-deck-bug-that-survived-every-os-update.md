---
title: "The Steam Deck bug that survived every OS update (it was hiding in an overlay)"
published: 2026-06-20
description: "A SteamOS update left my Steam Deck booting to a desktop login that rejected my password — here's the overlayfs corruption behind it and the two-command fix."
tags: [Linux, Gaming]
category: Linux
draft: false
---

You update SteamOS, the Deck reboots, and instead of Game Mode you land on the Plasma desktop login. You type your password. Rejected. You try again, slower this time, certain you fat-fingered it. Rejected.

Here's the twist that makes this one worth a post: the usual fixes — rolling back, a reinstall, jumping to another SteamOS branch — all act on a part of the system that wasn't the problem, so none of them can work. I worked that out the slow way. You don't have to.

# TL;DR — the fix

Get to a console (more on that below) and run:

```bash
rm -f /var/lib/overlays/etc/upper/passwd
rm -f /var/lib/overlays/etc/upper/shadow
```

Then reboot. This resets the `deck` user back to factory (no password) and restores the automatic boot into Game Mode. If you want to know why two `rm` commands fix what a full OS reinstall couldn't, [skip to the explanation](#why-it-works) — that's the interesting bit.

# What broke

It started after the **3.7.25** update. The Deck rebooted, and instead of the gamescope session it dropped me at the SDDM desktop login. My password didn't work. No typo, no caps lock — just rejected, every time.

My first guess was the obvious one: bad build. Updates ship broken occasionally, it happens. So I did what everyone does — I started trying to undo it.

# The dead ends

Each thing I tried ruled something out, which is the only reason they earned their place here.

SteamOS keeps the previous image around, so I rolled back and pinned the working partition with `rauc status mark-active booted`. That got me running again — for now. But it only chooses *which* OS image to boot; it doesn't touch whatever was actually corrupted, so the next update would just drag the problem back in. Decky and third-party plugins are the usual suspects for "it broke after an update", so I disabled the lot. No change — not third-party software, then.

If one build is bad, a different branch should sidestep it, so I moved from Stable (**3.7.25**) to the Beta channel (**3.8.x**), a completely different set of system images. The symptom came along for the ride. That was the first real clue: a bug that lives through an entire branch change isn't *in* the build.

:::note
**Getting to a real console on the Deck.** This tripped me up, so here it is. `Ctrl+Alt+F2` and `F3` are blank and uninitialised — they look dead because they are. `Ctrl+Alt+F4` is the actual text console. `Ctrl+Alt+F1` takes you back to the graphical session. The editable GRUB menu is also hidden by default, and the button-combo "boot menu" you may already know is the Deck's own partition picker, not GRUB. I ended up editing the GRUB config to add a debug console of my own, which came up on `Ctrl+Alt+F9`.
:::

On the F4 console I figured I'd just reset the password directly with `passwd deck`, and gave it something trivial. It looked like it took. Then I logged in — "Login incorrect." Same trivial password I'd set seconds earlier. The change wasn't sticking, and that was the clue that finally pointed the right way. This was never about guessing the password; the password change itself wasn't persisting.

So lay it out. It survived a full OS update, it survived a jump to a different SteamOS branch, and it survived a command-line `passwd` change. Something that outlives the OS image *and* outlives my edits to it has to live somewhere the image never overwrites — on the persistent partition, in a layer the updates ride straight over.

# Why it works

So I deleted the overlay's copies of those two files, then rebooted:

```bash
rm -f /var/lib/overlays/etc/upper/passwd
rm -f /var/lib/overlays/etc/upper/shadow
```

Straight into Game Mode, no login wall, as if nothing had happened. Here's why.

SteamOS is an **immutable** OS: the root filesystem is mounted read-only. You can't just edit files in `/` and have them stick, because the base system ships as a sealed image that updates swap out wholesale. But plenty of things still need to change at runtime — your config in `/etc`, for one. SteamOS handles that with an overlay filesystem on `/etc`. An overlayfs stacks two layers and shows you the merged result: a **lower layer**, the pristine `/etc` from the read-only OS image, and an **upper layer**, a writable override at `/var/lib/overlays/etc/upper/`. Read a file and the upper layer wins if it has its own copy; otherwise you fall through to the lower one. Write to `/etc` and the change lands in the upper layer — so when you change a password, the new `passwd` and `shadow` get written there.

Mine were corrupted. And because the upper layer wins, those broken override files were shadowing the perfectly good factory `passwd` and `shadow` underneath. That one fact explains both symptoms at once. Auth failed because login checked the corrupted upper-layer credentials, so nothing matched. And autologin failed because the Deck couldn't log `deck` into the gamescope session automatically — so SDDM fell back to the manual desktop login I kept hitting. Deleting the two override files removes the upper-layer copies, and `/etc` falls through to the pristine factory `passwd` and `shadow` in the lower layer, where `deck` is unlocked with no password. Auth works, autologin works, Game Mode comes back.

This is also why nothing else worked. That upper layer sits on the persistent `/var` partition — and `/var` is the one thing image swaps leave alone. Rolling back, changing branch, a reinstall: each of them replaces the base image and steps straight over `/var/lib/overlays/`. The corruption sailed through `3.7.25 → 3.8.x` without a scratch because every "fix" I reached for was swapping the layer that was already fine.

# Aftermath and takeaways

A couple of things to know before you walk away clean. The `deck` user now has no password — that's the factory default and it's fine for normal use, but `sudo` will prompt for one, so set a password with `passwd deck` and write it down somewhere. You've just seen what happens when credentials go sideways. I also checked the SSD, and it was healthy: this was config corruption in a writable overlay, not failing hardware — worth confirming before you go buying a replacement drive over a two-byte problem.

The bigger lesson is that immutable-OS systems fail differently. When the base image is read-only, the interesting failures move into the writable layers stacked on top of it — and those layers outlive the image, so "reinstall the OS" stops being a cure-all. The trick is telling apart the disposable image and the state that persists across it. Two `rm` commands sorted what a week of rolling back and branch-hopping couldn't, once I'd worked out the shape of the problem.

If your Deck is stuck at that login wall right now, run the two commands and get back to playing. And then go set a password.

Have fun, and stay safe.
