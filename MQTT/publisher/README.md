RPi-SenseStation MQTT publisher
===============================

## Setup
### Install(reinstall) system prerequisites
```sh
$ sudo apt install python3 python3-pip python3-rpi.gpio

# Below is optional
$ sudo apt install --reinstall iputils-ping
```
This will *reinstall* `iputils-ping` package for `ping` command. This might be helpful if segmentation fault causes when you execute `ping` command.

### Install Python requiements
```sh
$ sudo pip3 install -r requirements.txt
```

### Run publisher script
```sh
$ python3 ./main.py

# Or you can run the script as background process
$ nohup python3 ./main.py &
```
