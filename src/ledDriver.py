#!/usr/bin/env python

"""

 ledDriver.py for SpotifyBox project

 Made by Antoine Guittet
 Email <ag612@kent.ac.uk>

 University Of Kent

 Home made led driver. This driver works with a SeeedStudio RGB led chainable where the p9813 chipset has been removed.
 The led is actually wired on 3 GPIO - 17 - 27 - 22 and use the BCM mode.

 The led Mapping algorithm is from the Sunfounder - https://www.sunfounder.com/

"""


import RPi.GPIO as GPIO
import time


class LedDriver():

    pins = {'pin_R': 17, 'pin_G': 27, 'pin_B': 22}  # pins is a dict

    def __init__(self):

        # Set GPIO pins
        GPIO.setmode(GPIO.BCM)
        for i in self.pins:
            GPIO.setup(self.pins[i], GPIO.OUT)
            GPIO.output(self.pins[i], GPIO.HIGH)

        self.p_R = GPIO.PWM(self.pins['pin_R'], 2000)
        self.p_G = GPIO.PWM(self.pins['pin_G'], 2000)
        self.p_B = GPIO.PWM(self.pins['pin_B'], 5000)

        self.p_R.start(0)
        self.p_G.start(0)
        self.p_B.start(0)

    def mapLed(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def setColor(self,col):
        R_val = (col & 0xFF0000) >> 16
        G_val = (col & 0x00FF00) >> 8
        B_val = (col & 0x0000FF) >> 0

        R_val = self.mapLed(R_val, 0, 255, 0, 100)
        G_val = self.mapLed(G_val, 0, 255, 0, 100)
        B_val = self.mapLed(B_val, 0, 255, 0, 100)

        self.p_R.ChangeDutyCycle(R_val)
        self.p_G.ChangeDutyCycle(G_val)
        self.p_B.ChangeDutyCycle(B_val)

    def setNotReady(self):
        self.setColor(0x00FFFF)
        time.sleep(0.1)
        self.setColor(0x000000)
        time.sleep(0.1)
        self.setColor(0x00FFFF)
        time.sleep(0.1)
        self.setColor(0x000000)
        time.sleep(0.1)
        self.setColor(0x00FFFF)

    def setError(self):
        self.setColor(0x00FFFF)
        time.sleep(0.1)
        self.setColor(0x000000)
        time.sleep(0.1)
        self.setColor(0x00FFFF)
        time.sleep(0.1)
        self.setColor(0x000000)
        time.sleep(0.1)
        self.setColor(0x00FFFF)
        time.sleep(0.1)
        self.setColor(0x000000)
        time.sleep(0.1)
        self.setColor(0xFF00FF)
        
    def setReady(self):
        self.setColor(0xFF00FF)
        time.sleep(0.1)
        self.setColor(0x000000)
        time.sleep(0.1)
        self.setColor(0xFF00FF)
        time.sleep(0.1)
        self.setColor(0x000000)
        time.sleep(0.1)
        self.setColor(0xFF00FF)

    def setReading(self):
        self.setColor(0xFFFF00)
        time.sleep(0.1)
        self.setColor(0x000000)
        time.sleep(0.1)
        self.setColor(0xFFFF00)
        time.sleep(0.1)
        self.setColor(0x000000)
