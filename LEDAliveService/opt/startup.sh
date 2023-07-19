#!/bin/sh

PYTHON3=$(/usr/bin/which python3)

cd $(dirname $0)
$PYTHON3 startup.py
$PYTHON3 persist.py
