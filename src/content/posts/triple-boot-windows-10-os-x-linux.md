---
title: "Triple Boot - Windows 10 / OS X / Linux"
published: 2016-07-16
description: ""
tags: [Linux]
category: Linux
draft: false
---

This will be an addition to my previous post: [Lenovo y50-70 Hackintosh](https://github.com/ddulic/damir.tech/blob/master/posts/lenovo-y50-70-hackintosh), where I explained how to put OS X on this laptop.

Recently, I wanted to play around with Linux a bit more, get to know the desktop better (and I was just bored again), so I wanted to see how to do triple boot. I didn’t find many guides online saying how to do it, and even if I found something, it was irrelevant to me because I used [Clover](https://sourceforge.net/projects/cloverefiboot) as a bootloader (cuz Hackintosh) and not Windows/Grub.

As a third option, I will be adding GNU/Linux.

The first decision I had to do is pick a distro, I of course immediately went over to [antergos.com](https://antergos.com/) to download Antergos.

The installation is standard, but for the `/boot/efi` (you also have to run the USB in EFI mode in order for the triple boot to work) we have to choose the EFI partition where Clover and the other bootloaders reside.

![](../../assets/images/triple-boot-windows-10-os-x-linux/quad_boot.jpg)


This will install antergos grub to this partition, so Clover can attempt to find it. After finishing the installation you should all know by now, reboot the machine, and it will boot into Antergos(🙌 hooray… kinda), the direct boot into Antergos is normal since a fresh OS install always replaces the default bootloader to the one in the system you are installing uses. To see if this was successful, we need to boot Clover and see if it was added to the boot list. Reboot into the UEFI and put Clover (OS X) to be the default boot again and boot up. We can see that we didn’t screw up the other systems since they are showing up, but there is no Linux… what?!?! The problem here is that it seems Clover doesn’t auto-detect Arch Linux (which is what Antergos is) by default like it does with Windows and Ubuntu/Fedora (as I found out later). I Googled a bit and couldn’t find a way to correctly edit the config.plist to add Arch manually so Clover would see it. I don’t know about you, but I want everything to be in a single bootloader, I see no point in swapping bootloaders to boot into the system I want.

Soooo, since I can’t run Arch I wanted to test if Clover auto-detects Linux systems as it should, so I installed the most distributed one – Ubuntu. + I can test how Ubuntu 16 works, since I didn’t have the chance to test the update yet. After downloading and installing [Ubuntu Gnome 16.04](https://ubuntugnome.org/ubuntu-gnome-16-04-lts-is-here) I rebooted, changed the bootloader to Clover again and once I saw Clover – BOOM, there is Ubuntu, a giant U staring back at me 🙂

After a few days of testing, Ubuntu 16 made me sick, the desktop crashes a few minutes into boot (not much of a problem but annoying), the audio jitter for me is still there, the Wi-Fi keeps disconnecting and for some reason, I can’t seem to install the [newest realtek wifi drivers](https://github.com/lwfinger/rtlwifi_new). So, I will pass on Ubuntu for now…

Moving on.

Listening to the Linux Action Show a few weeks ago I heard their review of [Fedora 24](https://getfedora.org/en/workstation/download), and it piqued my interest, I have never tried Fedora before, so why not try it, who knows, I might even like it.

I freed up some more space (I didn’t want to remove Ubuntu because I didn’t know if Fedora would also show up in Clover) and I proceeded to the installation. After *decrypting* the partition manager and making sure it wouldn’t format my EFI partition (I also had a backup of course) I booted into Fedora, and it was fluid, everything just seemed to work. I can feel that Gnome’s place is in Fedora, it feels like the default desktop that it is. And during boot, after selecting Fedora from Clover it doesn’t show Grub like Ubuntu did, it just boots straight into Fedora. The only thing that felt janky was the Wi-Fi, but I had no problem installing the new drivers from above. All but one of my Gnome extensions work.

I think I will be keeping Fedora for a while. I will also be posting a customization guide to Fedora soon 🙂

Thanks for reading and have a great day ^_^

---


---
