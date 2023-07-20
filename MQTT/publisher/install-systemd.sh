#!/bin/sh
# Please run as root

pushd $(dirname $0)

SERVICE_FILE_NAME="odroid-sensehub-mqtt-publisher.service"
SERVICE_FILE_PATH="/etc/systemd/system/$SERVICE_FILE_NAME"
CUR_DIR=$(pwd)

echo "" > $SERVICE_FILE_PATH

echo "[Unit]" >> $SERVICE_FILE_PATH
echo "Description=somni Odroid-Sensehub MQTT Publisher" >> $SERVICE_FILE_PATH
echo "After=multi-user.target mosquitto.service" >> $SERVICE_FILE_PATH
echo "" >> $SERVICE_FILE_PATH
echo "[Service]" >> $SERVICE_FILE_PATH
echo "Type=simple" >> $SERVICE_FILE_PATH
echo "ExecStart=/usr/bin/python3 $CUR_DIR/main.py" >> $SERVICE_FILE_PATH
echo "TimeoutStartSec=0" >> $SERVICE_FILE_PATH
echo "Restart=on-failure" >> $SERVICE_FILE_PATH
echo "RestartSec=10" >> $SERVICE_FILE_PATH
echo ""
echo "[Install]" >> $SERVICE_FILE_PATH
echo "WantedBy=multi-user.target" >> $SERVICE_FILE_PATH

chmod 644 $SERVICE_FILE_PATH

systemctl daemon-reload
systemctl enable $SERVICE_FILE_NAME

popd
