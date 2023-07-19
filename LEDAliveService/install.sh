#!/bin/sh
# Please run as root

pushd $(dirname $0)

OPT_DIR=/opt/somni/sensehub/led-alive
FILES_DIR=./opt

mkdir -p $OPT_DIR
cp $FILES_DIR/* $OPT_DIR/

cp led-alive-startup.service /etc/systemd/system/led-alive-startup.service
chmod 644 /etc/systemd/system/led-alive-startup.service

cp led-alive-shutdown.service /etc/systemd/system/led-alive-shutdown.service
chmod 644 /etc/systemd/system/led-alive-shutdown.service

systemctl daemon-reload
systemctl enable led-alive-startup.service
systemctl enable led-alive-shutdown.service

popd
