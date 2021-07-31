#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def zme_IsRunningOnPi():
    return os.uname()[4].startswith("arm");

if zme_IsRunningOnPi():
    import smbus 

def zmePiEmulPrint(s):
    print(s)
def zme_init_I2C(interface_number):
    bus =  None
    if zme_IsRunningOnPi():
        bus = smbus.SMBus(interface_number)
    else:
        zmePiEmulPrint("zme_init_I2C(%d). "%(interface_number))
    return bus