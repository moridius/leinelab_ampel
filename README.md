# leinelab_ampel

## Requirements

* python3
  * pip3 (python package manager)
  * RPI.GPIO
* systemd (other init systems are not implemented yet)

## Config

**Copy** the ```jabber.ini.example``` to ```jabber.ini``` and edit it to your needs.

## Install

The following instructions should be executed as root.

```shell
$ pip install -r requirements.txt
$ sh INSTALL.sh  # create and update systemd.service files
$ systemctl enable ampel_foreman
$ systemctl enable ampel_poll_webserver
$ systemctl enable ampel_push_webserver
$ systemctl enable ampel_jabber_bot
$ systemctl enable ampel_button_listener
```

## Commandline Interface

You need ```netcat-openbsd``` and root rights.

```shell
$ echo -n 'OpenLab' | nc -U /var/run/ampel.sock
```

## Internals

### Foreman

* Handles Output GPIO Pins
* Opens unix socket at ```/var/run/ampel.sock```
  * Commands are ```OpenLab```, ```CloseLab```, ```ButtonPressed``` (toggles state), ```BlinkLab``` and ```Status```

### Poll Webserver

* Opens a http remote url
* The content of this remote is interpreted as commmand
* Command is submitted to the unix socket of *Foreman*
* Polling intervall is currently 15 seconds

### Push Webserver

* Polls the unix socket of *Foreman* (every 1 sec)
* If the status has changed, it will call a remote http url

### Jabber-Bot

* Receives commands via Jabber
* Submits them to unix socket of *Foreman*
* Status of the Jabber Account is set to the command

### Button Listener

* Handles Input GPIO Pin
* Submits the ```ButtonPressed``` command to unix socket of *Foreman*
