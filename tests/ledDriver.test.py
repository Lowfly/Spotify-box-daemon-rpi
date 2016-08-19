#!/usr/bin/env python

"""

 LedDriver class test file

"""

import sys
sys.path.insert(0, '../src/')
import ledDriver
import time


print("Starting tests")

testled = ledDriver.LedDriver()

print("Test setReading - Sould blink and be blue")
testled.setReading()

time.sleep(3)


print("Test setReady - Sould blink and be green")
testled.setReady()

time.sleep(3)
print("Test setNotReady - Sould blink and be red")
testled.setNotReady()

time.sleep(3)
print("Test setError - Sould blink and be red")
testled.setError()

time.sleep(3)

print("Test setColor - Should stay green")
testled.setColor(0xFF00FF)

time.sleep(3)

print("Test done")
