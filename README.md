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

`wget -O Spinnaker-2.7.0.128-Linux.zip https://flir.netx.net/file/asset/54573/original/attachment`

Extract the file:

`unzip Spinnaker-2.7.0.128-Linux.zip`

The CPU structure of Jetson Nano is arm64-bionic so let's jump to the folder:

`cd arm64_bionic`

In this folder, you will see 3 Python zip file which we will deal later.
![alt](/Screenshot%20from%202024-05-20%2022-53-16.png) 

Let's focus on the SDK setting file:

`tar xzvf spinnaker-2.7.0.128-arm64-pkg.tar.gz`

`cd spinnaker-2.7.0.128-arm64`

The install guide will be in the ****README_ARM**** file. I will do the copy paste job:





