#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Tom Mladenov, Niyusha'

import time
from threading import Thread

import datetime
from adafruit_bus_device.i2c_device import I2CDevice

CMD_ID = 0x33
PARAM_ID = 0x54


class Controller(Thread):

    alive_flag = True
    running = False

    def __init__(self, parent, i2c_instance):
        super().__init__()
        self.parent = parent
        self.i2c_bus = i2c_instance
        self.controller_device = I2CDevice(self.i2c_bus, self.parent.parent.datapool.ADDR_REMOTE_CONTROL)

    def is_alive(self):
        # Poll if device reachable
        command = bytearray([0xFF, 0x00, 0xFF, 0x00])
        response = bytearray(2)  # Initialize the response variable
        self.controller_device.write_then_readinto(command, response)
        if response.decode('utf-8') == 'OK':
            return True
        else:
            return False

    def enable(self):
        self.running = True

    def disable(self):
        self.running = False

    def run(self):
        while self.alive_flag:
            time.sleep(1)
            while self.running:
                try:
                    if PARAM_ID == 0x53:
                        command = '{command_id};{param_id};{gps_lat};{gps_lon}'.format(command_id=CMD_ID,
                                                                                       param_id=PARAM_ID, gps_lat=50.02,
                                                                                       gps_lon=8.4013)
                        rList = command.encode('utf-8')
                    elif PARAM_ID == 0x54:
                        now = datetime.datetime.utcnow()
                        command = [CMD_ID, PARAM_ID, int(now.hour), int(now.minute), int(now.second),
                                   int(now.year) - 2000, int(now.month), int(now.day)]
                        rList = command

                    arr = bytearray(rList)
                    payload = arr  # + bytearray.fromhex(str(crc))
                    self.controller_device.write(payload)
                    print(str(payload))

                except Exception as e:
                    print(e)

                time.sleep(1)
