#!/bin/bash

echo -e "--> Preparing..."
sudo apt-get update

echo -e "--> Docker Engine Installation"
sudo apt-get -y install docker.io

echo -e "--> Getting Images Sensor"
sudo docker pull cowrie/cowrie
sudo docker pull ardikabs/dionaea
sudo docker pull ardikabs/glastopf

echo -e "--> Configure Docker API"
sudo sed -i '14c\ExecStart=/usr/bin/dockerd -H fd:// -H=tcp://0.0.0.0:5555' /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo service docker restart

echo -e "--> Docker Installer for Sensor Device Successfully"
