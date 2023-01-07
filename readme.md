# Setup instructions

Start with:
- Raspberry Pi Model B3
- A Raspbian installation - 32-bit, full desktop version
- LCD35 screen
- ELM 327 bluetooth OBD reader

## Set up access to your local network:

- Create wpa_supplicant.conf in the root of the D drive:

```
country=gb
update_config=1 
ctrl_interface=/var/run/wpa_supplicant

network={
scan_ssid=1
ssid="xxx"
psk="xxx"
}
```

## Enable SSH
- Create empty file called `ssh` in the root of the D drive.

## Software

SSH to your Raspberry Pi from another machine, then:

Set up the screen:
- `git clone https://github.com/goodtft/LCD-show.git`
- `chmod -R 755 LCD-show`
- `cd LCD-show/`
- `sudo ./LCD35-show`
- Restart the Pi.

General updates:

- `sudo apt update`
- `sudo apt upgrade`

Get this code:

- `git clone https://github.com/evansabove/car-data.git`
- `python -m pip install obd`

Use bluetoothctl to get MAC address of OBDII adapter. Keep a note of it.

## Bluetooth setup - dont do this

- `bluetoothctl`
- `agent on`
- `scan on`
- `pair [XX:XX:XX:XX:XX:XX]`
- `trust [XX:XX:XX:XX:XX:XX]`

where `[XX:XX:XX:XX:XX:XX]` is the MAC address of the OBD adapter.

## Script setup
- `mkdir /home/pi/.config/autostart`
- `nano /home/pi/.config/autostart/cardata.desktop`
- Add the following code to the file:
  ```
  [Desktop Entry]
  Type=Application
  Name=CarData
  Exec=/usr/bin/python3 /home/pi/Projects/car-data/script.py --log=False --port=/dev/rfcomm0
  ```




00:1D:A5:68:98:8B



sudo rfcomm connect hci0 00:1D:A5:68:98:8B 0h