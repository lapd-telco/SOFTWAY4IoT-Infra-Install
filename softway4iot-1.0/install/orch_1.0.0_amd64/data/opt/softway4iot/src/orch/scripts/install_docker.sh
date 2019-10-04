#!/bin/bash

#update packages
apt-get update

#upgrade
apt-get upgrade

#install sudp
apt install sudo

#set username sudo
usermod -aG sudo gmtest

#uninstall old version
apt-get remove docker docker-engine docker.io

#update packages
apt-get update

#install gnupg2
apt-get install -y gnupg2

#install curl
apt-get install curl

#add GPG key Docker Repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

#install software-properties-common
apt-get install software-properties-common

#add Docker Repository to APT
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

#update packages
apt-get update

#install docker-ce
apt-get install docker-ce

#print Docker version
docker version

#add Docker to sudo group
usermod -aG docker $(whoami)