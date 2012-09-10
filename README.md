rPi-XPT2046-Touchscreen-Python
==============================

Python proof of concept for interfacing an XPT2046 Touch Screen Controller
to a Raspberry Pi using SPI (via bit-banged GPIO).

This sample uses the SPI pins on the Raspberry Pi Expansion header.
(With the intention that no wiring changes should be required to use SPI
drivers, rather than bit-banged GPIO).

More information on Raspberry Pi GPIO can be found here:
http://elinux.org/RPi_Low-level_peripherals

This sample code is dependent on the RPi.GPIO library available here:
http://pypi.python.org/pypi/RPi.GPIO/

To run:

$ sudo python3 touchMyPi.py
