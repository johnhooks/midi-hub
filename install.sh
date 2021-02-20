#!/bin/bash

VERSION=v0.1.0

if [ "$1" = uninstall ]; then UNINSTALL=true; else UNINSTALL=false; fi

SCRIPT="/usr/bin/python3 -m midihub"

USB_CONNECT_FILE=/usr/local/bin/usb-connect.py
USB_CONNECT_URL="https://raw.githubusercontent.com/johnhooks/midi-hub/$VERSION/usb-connect.py"

MIDI_RULE_FILE=/etc/udev/rules.d/33-midiusb.rules
MIDI_RULE=$(cat <<EOF
ACTION=="add|remove", SUBSYSTEM=="usb", DRIVER=="usb", RUN+="$USB_CONNECT_FILE"
EOF
)

SERVICE_PATH=/lib/systemd/system/midi.service
SERVICE=$(cat <<- EOF
	[Unit]
	Description=Python MIDI Hub Service

	StartLimitIntervalSec=500
	StartLimitBurst=5

	[Service]
	Restart=on-failure
	RestartSec=5s

	ExecStart=$SCRIPT

	[Install]
	WantedBy=multi-user.target
EOF
)

if [ $UNINSTALL = false ]
then
	apt-get --yes install git python3-pip
	python3 -m pip install git+https://github.com/johnhooks/midi-hub.git@$VERSION#egg=midi-hub
	echo "=> Ensure necessary packages are installed"
	curl --output $USB_CONNECT_FILE $USB_CONNECT_URL

	chmod 744 $USB_CONNECT_FILE
	echo "=> Downloaded midi.rule script"

	echo "$MIDI_RULE" > $MIDI_RULE_FILE
	chmod 644 $MIDI_RULE_FILE
	echo "=> Created $MIDI_RULE_FILE"

	udevadm control --reload
	service udev restart
	echo "=> Restarted the device manager"

	echo "$SERVICE" > $SERVICE_FILE
	chmod 644 $SERVICE_FILE
	echo "=> Created $SERVICE_FILE"

	systemctl daemon-reload
	systemctl enable midi.service
	systemctl start midi.service
	echo "=> Restarted systemctl, enabled and started the new midi.service"
else
	python3 -m pip uninstall midihub
	echo "=> Uninstalled the midihub python package"

	rm  $MIDI_RULE_FILE
	echo "=> Removed $MIDI_RULE_FILE"

	udevadm control --reload
	service udev restart
	echo "=> Restarted the device manager"

	systemctl stop midi.service
	systemctl disable midi.service
	echo "=> Stopped and disabled midi.service"

	rm $SERVICE_FILE
	echo "=> Removed $SERVICE_FILE"

	systemctl daemon-reload
	systemctl reset-failed
	echo "=> Restarted systemctl"

	rm $USB_CONNECT_FILE
	echo "=> Removed $USB_CONNECT_FILE"
fi

unset VERSION
unset UNINSTALL
unset SCRIPT
unset MIDI_RULE
unset MIDI_RULE_FILE
unset SERVICE
unset SERVICE_FILE
