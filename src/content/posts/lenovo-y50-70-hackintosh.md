---
title: "Lenovo y50-70 Hackintosh"
published: 2015-11-26
description: ""
tags: [Hackintosh, macOS, Dual Boot, Lenovo, Hardware]
category: Personal
draft: false
---

# Introduction

One day, I was bored, and I decided to try and put OS X on my laptop and transform it from an ordinary Lenovo y50-70 into a **LENOVO y50-70 HACKINTOSH** (yes, the caps are needed).

This will **NOT** be a comprehensive guide on how to put OS X on your Lenovo y50-70. These are some tips on where to start and fixes for various problems I faced when following some guides.

First, where to start. When I started I made a mistake, I followed a guide on YouTube thinking that it is good since it was posted about half a year ago at the time of posting this, but I was wrong, in those 6 months a lot has changed, and a lot has been made easier and this laptop is good for Hackintosh, as mentioned [here](http://blazinglist.com/top-10-best-laptops-hackintosh-2015/).

[RehabMan’s post on tonymacx86](http://www.tonymacx86.com/el-capitan-laptop-guides/168612-guide-lenovo-y50-uhd-1080p-using-clover-uefi-10-11-a.html) offers an excellent and in-depth guide on how to transform your laptop into a Hackintosh. Read the post a few times**,** so you have a good understanding of what you will be doing, **backup** all that you find dear, and you do not wish to lose.


# OSX USB Preparation

Before we even get started, there is a small issue, OS X can only be installed to USB (which is how we will be doing it) from OS X itself. The best way of tackling this is to install it on a VM. There are a few useful guides on how to do this on YouTube. I recommend putting OS X El Capitan on this laptop since it works great, to achieve this, follow [this](https://www.youtube.com/watch?v=tafqhSUfKnY) video (it’s a guide for Yosemite) on YouTube and once you get it up and running download OS X El Capitan from within the App Store, when you save it on your drive you can follow [this post](https://www.tonymacx86.com/threads/guide-booting-the-os-x-installer-on-laptops-with-clover.148093/) and use the `Option 2 (GPT, one partition)` since the SSD/HDD on your Lenovo y50-70 is most likely in GPT format, but we will need to wipe everything in most cases if you want dual boot, it’s just the easiest, if you wish to try without wiping you can follow [this post](https://www.tonymacx86.com/threads/mavericks-windows-8-on-same-drive-without-erasing.133940/). Keep in mind, when adding kexts, for the internet to work after the installation we will need `RealtekRTL8111.kext` which can be found in the same post, you don’t need any other internet kexts and the `GenericUSBXHCI.kext` is not needed. You will, however, require the `USBXHCI_y50.kext` which can be found [here](https://github.com/RehabMan/Lenovo-Y50-DSDT-Patch/archive/master.zip). Just follow the guide on installing OS X to USB and the hardest part is finished.

# Dual Boot

Now comes the part of installing and configuring dual boot. To do this properly our drive needs to be in GPT format, and we require an EFI partition which is at least 200mb (this is important, if it’s lower than 200mb you can’t install OS X since it requires a minimum of 200mb EFI for some reason, I found this out the hard way -.-‘). I would recommend grabbing another USB and putting Windows install onto it in GPT format, [Rufus](https://rufus.akeo.ie/) is a good tool if you are on Windows and you can find guides on Google on how to do this. Once Windows is on our USB, shutdown the laptop and boot it via the recovery key left of the shutdown/startup button with your USB inserted in the right USB 2.0 slot (it can sometimes cause problems when in the USB 3.0 slot, so it's always best to use the 2.0 for installing systems). Once booted via the recovery key, we need to configure our bios following [RehabMan’s post](https://www.tonymacx86.com/threads/guide-lenovo-y50-uhd-or-1080p-using-clover-uefi-10-11.168612/) under the `BIOS settings` part of the guide. After you have set up your bios, shutdown, and boot once again via the recovery and install Windows from USB. NOW, THIS IS **IMPORTANT**: We will need to manually make the EFI partition (Windows does this automatically once you select the partition on which you wish to install Windows, but it makes a 128mb EFI, and we need a minimum of 200mb). To accomplish this, we first need to format our drive to GPT. Follow these steps to convert to GPT and create the EFI partition:

- boot Windows installer USB
- at first, screen press `Shift+F10` to get command prompt
- type: `diskpart`
- type: `list disk` (to you're certain on the disk you're working with, in my case confirms disk 0)
- type: `select disk 0`
- type: `clean` (don't blame me if you don't know what this does :-) )
- type: `convert gpt`
- type: `create partition efi size=200`
- type: `format quick fs=fat32 label="EFI"`
- type: `create partition msr size=128`
- type: `exit`
- type: `exit`

After this, just continue your standard Windows installation via the `Custom` menu. When creating partitions for Windows I would recommend 50gb for C:/, 140gb for D:/ and leave the rest unallocated (we will use this for OS X). Finish up and check if Windows boots. If it boots, good job, you have installed Windows.

# Installing OSX

Next, we need to install OS X. Insert the OS X USB we have prepared in the 2.0 USB slot and boot via the recovery key from USB. Once you boot the installer you will have to format the remaining unallocated space in Disk Utility which can be found in the menus on the top left. Once this is done, install the system on your SSD/HDD. If you are not certain how to, follow this [guide](https://www.tonymacx86.com/threads/guide-booting-the-os-x-installer-on-laptops-with-clover.148093/#post917904).

# Post Installation

After you have installed OS X El Capitan all you have to do is configure it to suit the laptop, this has been made a LOT easier over the past few months, check out [RehabMan’s post](http://www.tonymacx86.com/el-capitan-laptop-guides/168612-guide-lenovo-y50-uhd-1080p-using-clover-uefi-10-11-a.html) under `Post Installation`. There shouldn’t be any problems here, it’s all elementary, just copy and paste the commands, and you are done.

Enjoy your Lenovo y50-70 Hackintosh ^^
