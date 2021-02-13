# midi-hub

**Simply connect together all MIDI USB devices on a Raspberry Pi.**

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.

**Warning: Use with Python3 only.** This library is not intended to work with Python2.

## Instructions

### 1. Prepare the microSD card

- Download [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/)
- Download and install [balenaEtcher](https://www.balena.io/etcher/)
- Use Etcher to flash the Raspberry Pi OS Lite image onto the microSD card
- Create the following files inside the `boot` folder of the microSD:

  - `/boot/wpa_supplicant.conf`

    ```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=«your_ISO-3166-1_two-letter_country_code»

    network={
        ssid="«Your SSID»"
        psk="«SSID Password»"
    }
    ```

  - `/boot/ssh`

    To enable ssh, create an empty file named `ssh` (no extension)

- Unmount the microSD, plug it into the Pi and boot it up

### 2. Update and Upgrade System

Recommended to update the package system and upgrade

```bash
sudo apt update
sudo apt upgrade
```

### 3. Run Install Script

You may either download and run the script manually, or use the following cURL or Wget command:

```bash
curl -o- https://raw.githubusercontent.com/johnhooks/midi-hub/v0.1.0/install.sh | sudo bash
```

```bash
wget -qO- https://raw.githubusercontent.com/johnhooks/midi-hub/v0.1.0/install.sh | sudo bash
```

## Inspiration

- [Using a Raspberry Pi as a MIDI USB/5-pin bridge ](http://m635j520.blogspot.com/2017/01/using-raspberry-pi-as-midi-usb5-pin.html)
- [Raspberry Pi as USB/Bluetooth MIDI host](https://neuma.studio/rpi-midi-complete.html)
