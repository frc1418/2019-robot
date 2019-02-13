#!/usr/bin/env python3
from cscore import CameraServer, UsbCamera


def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    usb1 = cs.startAutomaticCapture(dev=0)
    usb2 = cs.startAutomaticCapture(dev=1)

    cs.waitForever()


if __name__ == "__main__":

    # To see messages from networktables, you must setup logging
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # You should uncomment these to connect to the RoboRIO
    # import networktables
    # networktables.initialize(server='10.xx.xx.2')

    main()
