#!/bin/sh

systemd_unit_file_path="/etc/systemd/system"
units="foreman poll_webserver push_webserver jabber_bot button_listener"

# find out where the install script is
script_path="$(realpath $(dirname $0))"

# generates a unit file for the service
function template {
name="$1"
exe="$script_path/$name.py"

cat << EOF
[Unit]
Description=$name of ampel
After=network.target

[Service]
ExecStart=$exe
KillMode=process
Restart=always

[Install]
WantedBy=multi-user.target
EOF

}

for u in $units; do
	path=$systemd_unit_file_path/ampel_$u.service
	echo "Creating $path."
	template "$u" > $path
done
