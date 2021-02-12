# Python MIDI Hub

**Simply connect together all MIDI USB devices on a Raspberry Pi.**

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.

**Warning: Use with Python3 only.** This library is not intended to work with Python2.

## Instructions

### 1. Prepare the microSD card

- Download [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/)
- Download and install [balenaEtcher](https://www.balena.io/etcher/)
- Using Etcher, flash the Raspberry Pi OS Lite image to an microSD card
- Inside the microSD `boot` folder create the following files:

  - `wpa_supplicant.conf` with the contents:

    ```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=«your_ISO-3166-1_two-letter_country_code»

    network={
        ssid="«Your SSID»"
        psk="«SSID Password»"
    }
    ```

  - Create an empty file named `ssh` (no extension)

- Unmount the microSD and plug it on the Raspberry

### 2. Install packages

- Boot the Raspberry Pi
- Find its IP address
- `ssh` in using username `pi` and password `raspberry`
- Issue the following commands
  ```bash
  sudo apt update
  sudo apt upgrade
  sudo apt install git python3-pip
  sudo pip3 install git+https://github.com/johnhooks/midi-hub.git#egg=midi-hub
  ```

### 3. Configure automatic MIDI connection

- Test that the `midi-hub` python package was installed correctly

  ```bash
  python3 -m midi-hub
  ```

- And check the results

  ```bash
  aconnect -l
  ```

- Create the file `/etc/udev/rules.d/33-midiusb.rules`

  ```bash
  echo 'ACTION=="add|remove", SUBSYSTEM=="usb", DRIVER=="usb", RUN+="/usr/bin python3 -m midi-hub"' | sudo tee /etc/udev/rules.d/33-midiusb.rules
  ```

- Issue the following commands

  ```bash
  sudo udevadm control --reload
  sudo service udev restart
  ```

- Configure MIDI connection at system boot

  - Create the file `/lib/systemd/system//midi.service` with the contents:

    ```
    [Unit]
    Description=Initial USB MIDI connect

    [Service]
    ExecStart=/usr/bin python3 -m midi-hub

    [Install]
    WantedBy=multi-user.target
    ```

  - Restart `systemctl` and enable `midi.service`

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable midi.service
    sudo systemctl start midi.service
    ```

## Inspiration

- [Using a Raspberry Pi as a MIDI USB/5-pin bridge ](http://m635j520.blogspot.com/2017/01/using-raspberry-pi-as-midi-usb5-pin.html)
- [Raspberry Pi as USB/Bluetooth MIDI host](https://neuma.studio/rpi-midi-complete.html)
