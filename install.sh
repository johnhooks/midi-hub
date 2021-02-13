script="/usr/bin/python3 -m midihub"

usb=$(cat <<EOF
ACTION=="add|remove", SUBSYSTEM=="usb", DRIVER=="usb", RUN+="$script"
EOF
)

service=$(cat <<- EOF
	[Unit]
	Description=Initial USB MIDI connect

	[Service]
	ExecStart=$script

	[Install]
	WantedBy=multi-user.target
EOF
)

echo "=> Install Packages"
apt-get update
# apt-get upgrade
apt-get --yes install git python3-pip
pip3 install git+https://github.com/johnhooks/midi-hub.git#egg=midi-hub

echo "=> Create USB MIDI rule"
echo $usb > /etc/udev/rules.d/33-midiusb.rules

echo "=> Restart the device manager"
udevadm control --reload
service udev restart

echo "=> Create the service to call midihub on boot"
echo "$service" > tee /lib/systemd/system/midi.service

echo "=> Enable restart systemctl and enable midihub as a service"
systemctl daemon-reload
systemctl enable midi.service
systemctl start midi.service
