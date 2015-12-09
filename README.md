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
