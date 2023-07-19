#!/bin/sh
# Please run as root

OPT_DIR=/opt/somni/sensehub/led-alive

systemctl stop led-alive-startup.service
systemctl disable led-alive-startup.service

systemctl stop led-alive-shutdown.service
systemctl disable led-alive-shutdown.service

rm -rf $OPT_DIR
rm -f /etc/systemd/system/led-alive-startup.service
rm -f /etc/systemd/system/led-alive-shutdown.service

systemctl daemon-reload
