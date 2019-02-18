#!/usr/bin/env python3
from cscore import CameraServer, UsbCamera
from networktables import NetworkTables


def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    usb0 = cs.startAutomaticCapture(dev=0)
    usb1 = cs.startAutomaticCapture(dev=1)

    camera0 = NetworkTables.getTable('CameraPublisher/USB Camera 0')
    camera1 = NetworkTables.getTable('CameraPublisher/USB Camera 1')

    cs.waitForever()


if __name__ == "__main__":

    # To see messages from networktables, you must setup logging
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # You should uncomment these to connect to the RoboRIO
    # import networktables
    # networktables.initialize(server='10.xx.xx.2')

    main()
