****This is the instruction for aqquiring images from GigE Camera and display them on Jetson Nano****
# Prerequisites

- [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/buy/jetson-nano-devkit)

The Jetson Nano is flash with [Jetpack SDK 4.6.1](https://developer.nvidia.com/embedded/jetpack-sdk-461) with a 64 Gb microUSB. You can find the official guide from Nvidia website: https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#intro

- GigE camera

In this instruction, we will use Grasshopper2 GigE, you can see the official camera document from the manufacturer website: https://www.flir.asia/support/products/Grasshopper2-GigE/#Documents

# Installation

- ### Spinnaker SDK

In order to detect the camera, the Jetson Nano must have the SDK which contains all documentation, example source code, precompiled examples, and libraries required to develop application.

First go to this website (you might have to create an account and log in): https://www.flir.com/support-center/iis/machine-vision/downloads/spinnaker-sdk-download/spinnaker-sdk--download-files/ 

From the website, you can see the latest version of the SDK is **Spinnaker 4.0.0.116 for Ubuntu 22.04 (December 21, 2023)**. Since the Jetson Nano is running on Ubuntu 18.04, we won't use this version.

Scroll to the bottom to the page, you can see the archived version. Here we will use version 2.7.0.128, just hit the download button. If you don't have a screen, just move to your download folder then run:

`$wget -O Spinnaker-2.7.0.128-Linux.zip https://flir.netx.net/file/asset/54573/original/attachment`

Extract the file:

`$unzip Spinnaker-2.7.0.128-Linux.zip`

The CPU structure of Jetson Nano is arm64-bionic so let's jump to the folder:

`$cd arm64_bionic`

In this folder, you will see 3 Python zip file which we will deal later.

![img1](https://i.imgur.com/BlK7x1K.png)

Let's focus on the SDK setting file:

`$tar xzvf spinnaker-2.7.0.128-arm64-pkg.tar.gz`

`$cd spinnaker-2.7.0.128-arm64`

The install guide will be in the ****README_ARM**** file. I will do the copy paste job:

`$sudo apt-get install libusb-1.0-0`

`$sudo sh install_spinnaker_arm.sh`


- ### GigE camera settings:

****DISABLE REVERSE PATH FILTERING (RPF):****

`$sudo gedit /etc/sysctl.d/10-network-security.conf`

Comment out the lines below in /etc/sysctl.d/10-network-security.conf:

```
# Turn on Source Address Verification in all interfaces to
# in order to prevent some spoofing attacks.
## net.ipv4.conf.default.rp_filter=1
## net.ipv4.conf.all.rp_filter=1
```
***
****INCREASE RECEIVE BUFFER SIZE:****

`$sudo gedit /etc/sysctl.conf`

Add the following lines to the bottom of the /etc/sysctl.conf file:

```
net.core.rmem_max=10485760
net.core.rmem_default=10485760
```

Make it permanent:
`$sudo sysctl -p`
***
****ENABLE JUMBO PACKET:****

`$sudo gedit /etc/network/interfaces`

Add the following lines:

```
iface eth0 inet static
address 169.254.0.64
netmask 255.255.0.0
mtu 9000

auto eth0
```
To enable Jumbo Packet for the GigE camera, change SCPS Packet Size
(GevSCPSPacketSize) to 9000 in SpinView or via Spinnaker API.

Reboot the computer before using any GigE cameras.

- ### Spinnaker SDK Python library (PySpin)

Now head back to the three python file above, notice that Jetson Nano is using **python 3.6.9**, thus we will use the corresponding package:

`$cd ..`

`$tar xzvf spinnaker_python-2.7.0.128-cp36-cp36m-linux_aarch64.tar.gz `

Again, the instruction will be in the ****README.txt**** file.

`$sudo apt-get install python-pip python3-pip`

`$pip install --upgrade pip`

`$sudo pip install keyboard`

`$pip install Pillow numpy==1.19.4`

`$pip install spinnaker_python-2.7.0.128-cp36-cp36m-linux_aarch64.whl`

# Testing

In the Examples folder, there are python scripts for taking the image from the camera and display them and lots more examples. You can use whatever you want








