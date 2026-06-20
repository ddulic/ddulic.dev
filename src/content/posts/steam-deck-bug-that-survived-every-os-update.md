---
title: "The Steam Deck bug that survived every OS update (it was hiding in an overlay)"
published: 2026-06-20
description: "A SteamOS update left my Steam Deck booting to a desktop login that rejected my password — here's the overlayfs corruption behind it and the two-command fix."
tags: [Linux, Gaming]
category: Linux
draft: false
---

You update SteamOS, the Deck reboots, and instead of Game Mode you land on the Plasma desktop login. You type your password. Rejected. You try again, slower this time, certain you fat-fingered it. Rejected.

Here's the twist that makes this one interesting: the usual fixes — rolling back, reinstalling, even jumping to a different SteamOS branch — *cannot* work, because the thing that broke doesn't live in the part of the system any of those touch. I spent a good while learning that the hard way, so you don't have to.

# TL;DR — the fix

Get to a console (more on that below) and run:

```bash
rm -f /var/lib/overlays/etc/upper/passwd
rm -f /var/lib/overlays/etc/upper/shadow
```

Then reboot. This resets the `deck` user back to factory (no password) and restores the automatic boot into Game Mode. If you want to know *why* two `rm` commands fix what a full OS reinstall couldn't, [skip to the explanation](#why-it-works) — it's the good part.

# What broke

It started after the **3.7.25** update. The Deck rebooted, and instead of the gamescope session it dropped me at the SDDM desktop login screen. My password didn't work. No typo, no caps lock — it was simply rejected, every time.

My first assumption was the obvious one: bad build. Updates ship broken occasionally, it happens. So I did what everyone does — I started trying to undo it.

# The dead ends

Each one ruled something out, which is the only reason they were worth the time.

## Rollback and pinning

SteamOS keeps the previous image around, so I rolled back and pinned the working partition:

```bash
rauc status mark-active booted
```

That got me running again — temporarily. But it's a workaround, not a cure. It only chooses *which* OS image to boot; it doesn't touch whatever was actually corrupted. The next update would just bring the problem back.

## Disabling Decky and plugins

Decky and third-party plugins are the usual suspects for "it broke after an update." Disabled the lot. No change. So this wasn't third-party software — it was something in the OS itself. Or so I thought.

## Stable to Beta

If a specific build is bad, a different branch should dodge it. I moved from Stable (**3.7.25**) to the Beta channel (**3.8.x**) — a whole different set of system images.

The symptom survived. That was the first real clue. A bug that lives through an entire branch change isn't *in* the build.

:::note
**Getting to a real console on the Deck.** This tripped me up, so here it is. `Ctrl+Alt+F2` and `F3` are blank and uninitialised — they look dead because they are. **`Ctrl+Alt+F4` is the actual text console.** `Ctrl+Alt+F1` takes you back to the graphical session. Also: the editable GRUB menu is hidden by default, and the button-combo "boot menu" you may already know is the Deck's *own* partition picker — not GRUB.
:::

## passwd deck

On the F4 console I figured I'd just reset the password directly:

```bash
passwd deck
```

I gave it something trivial. It appeared to take. Then I logged in — *"Login incorrect."* Again, with the same trivial password I'd just set. The change wasn't sticking.

That was the second clue, and the one that finally pointed the right way: this wasn't a bad password. The password change itself wasn't persisting.

# The aha

Step back and look at what I now knew:

- It survived a full OS update.
- It survived a jump to a different SteamOS branch.
- It survived a command-line `passwd` change.

Something that outlives the OS image *and* outlives my edits to it has to live somewhere the OS image never overwrites — on the persistent partition, in a layer the updates simply ride straight over.

# The fix

```bash
rm -f /var/lib/overlays/etc/upper/passwd
rm -f /var/lib/overlays/etc/upper/shadow
```

Reboot. Straight into Game Mode, no login wall, like nothing ever happened.

# Why it works

This is the part worth staying for.

SteamOS is an **immutable** OS: the root filesystem is mounted **read-only**. You can't just edit files in `/` and have them stick, because the base system is shipped as a sealed image that updates swap out wholesale.

But plenty of things *do* need to change at runtime — your config in `/etc`, for one. SteamOS handles that with an **overlay filesystem** on `/etc`. An overlayfs stacks two layers and shows you the merged result:

- a **lower layer** — the pristine `/etc` from the read-only OS image, and
- an **upper layer** — a writable override at `/var/lib/overlays/etc/upper/`.

When you read a file, the upper layer wins if it has its own copy; otherwise it falls through to the lower one. When you *write* to `/etc`, the change is written into the upper layer. So when you change a password, the new `passwd` and `shadow` get written as override files into `/var/lib/overlays/etc/upper/`.

Mine were corrupted. And because the upper layer wins, those broken override files were shadowing the perfectly good factory `passwd`/`shadow` underneath. That single fact explains *both* symptoms:

- **Auth failed** — login checked the corrupted upper-layer credentials, so nothing matched.
- **Autologin failed** — the Deck couldn't log `deck` into the gamescope session automatically, so SDDM fell back to the manual desktop login I kept hitting.

Deleting the two override files removes the upper-layer copies. `/etc` falls through to the pristine factory `passwd`/`shadow` in the lower layer — where `deck` is unlocked with no password. Auth works, autologin works, Game Mode returns.

# Why nothing else worked

Now the dead ends make sense. The upper layer lives on the persistent `/var` partition. OS updates and reinstalls only replace the **read-only base image** — the lower layer. `/var/lib/overlays/` rides along, untouched, every single time. That's exactly why the corruption sailed through `3.7.25 → 3.8.x` without a scratch: I kept replacing the one layer that was already fine.

# Aftermath and gotchas

A couple of things to know before you walk away clean:

- **`deck` now has no password.** That's the factory default, and it's fine for normal use — but `sudo` will prompt for one. Set a password (`passwd deck`) and *write it down somewhere*, because you've just seen what happens when credentials go sideways.
- **The SSD was healthy.** I checked. This was config corruption in a writable overlay, not failing hardware — worth confirming so you don't go buying a replacement drive over a 2-byte problem.

# Takeaways

- **Immutable-OS systems fail differently.** When the base is read-only, the interesting failures move into the writable layers stacked on top of it.
- **"Reinstall the OS" isn't a cure-all.** If the corruption lives outside the image, swapping the image changes nothing.
- **Know where your persistent data actually lives.** On SteamOS that's `/var` — and `/var/lib/overlays/etc/upper/` is where your `/etc` changes really go.
- **Surgical beats nuclear.** Two `rm` commands fixed what days of reinstalling couldn't, once I understood the shape of the problem.

If your Deck is stuck at that login wall right now, run the two commands and get back to playing. And then go set a password.

Have fun, and stay safe.
