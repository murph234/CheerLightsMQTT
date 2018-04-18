# CheerLightsMQTT
Python CheerLight client(s) using MQTT

This is a [CheerLights client](http://www.cheerlights.com) designed to run on a Raspberry Pi using [Pimoroni's Blinkt](https://shop.pimoroni.com/products/blinkt) as
the display.  It uses MQTT to get updates as they occur, and displays a random pattern of the last 3 colors.  Enjoy!

Requires the paho-mqtt and blinkt Python modules

```
pip install paho-mqtt
sudo apt-get install python-blinkt
```
