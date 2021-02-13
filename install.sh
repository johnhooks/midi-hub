#!/bin/bash

VERSION=v.0.1.2

SCRIPT="/usr/bin/python3 -m midihub"

MIDI_RULE_FILE=/etc/udev/rules.d/33-midiusb.rules
MIDI_RULE=$(cat <<EOF
ACTION=="add|remove", SUBSYSTEM=="usb", DRIVER=="usb", RUN+="$SCRIPT"
EOF
)

SERVICE_FILE=/lib/systemd/system/midi.service
SERVICE=$(cat <<- EOF
	[Unit]
	Description=Initial USB MIDI connect

	[Service]
	ExecStart=$SCRIPT

	[Install]
	WantedBy=multi-user.target
EOF
)

apt-get --yes install git python3-pip
python3 -m pip install git+https://github.com/johnhooks/midi-hub.git@$VERSION#egg=midi-hub
echo "=> Ensure necessary packages are installed"

echo "$MIDI_RULE" > $MIDI_RULE_FILE
echo "=> Created $MIDI_RULE_FILE"

udevadm control --reload
service udev restart
echo "=> Restarted the device manager"

echo "$SERVICE" > $SERVICE_FILE
echo "=> Created $SERVICE_FILE"

systemctl daemon-reload
systemctl enable midi.service
systemctl start midi.service
echo "=> Restarted systemctl, enabled and started the new midi.service"

unset VERSION
unset SCRIPT
unset MIDI_RULE
unset MIDI_RULE_FILE
unset SERVICE
unset SERVICE_FILE
