# Setup instructions

## Initialisation
- Start with a Raspbian installation
- `sudo apt update`
- `sudo apt upgrade`

## Bluetooth setup

- `sudo apt install bluetooth pi-bluetooth bluez blueman`
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
  Exec=/usr/bin/python /home/pi/Projects/car-data/script.py --log=False --port=/dev/rfcomm0```