# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 21:02:15 2022

@author: sskky
"""

import board
import time
from adafruit_motorkit import MotorKit
import curses
import os

class main():
    def __init__(self):
        self.kit = MotorKit(i2c=board.I2C())
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.PWMvor = 0.75    # 0 bis 1 entspricht 0-100% PWM beim Vorwärtsfahren
        self.korr = 0.8       # Korrekturfaktor
        self.PWMzur = 0.65    # entspricht dem Faktor der PWM beim Rückwärtsfahren
        self.drehen = 0.75    # entspricht dem Faktor der PWM bei der Drehung
        
    def vorwaerts(self):
        self.kit.motor1.throttle = self.PWMvor
        self.kit.motor2.throttle = self.korr * self.PWMvor
        self.kit.motor3.throttle = self.PWMvor
        self.kit.motor4.throttle = self.korr * self.PWMvor
        print("start")

    def zurueck(self):
        self.kit.motor1.throttle = -self.PWMzur
        self.kit.motor2.throttle = -self.PWMzur
        self.kit.motor3.throttle = -self.PWMzur
        self.kit.motor4.throttle = -self.PWMzur
        
    def rechtsDrehen(self):
        self.kit.motor1.throttle = -self.drehen
        self.kit.motor2.throttle = self.drehen
        self.kit.motor3.throttle = -self.drehen
        self.kit.motor4.throttle = self.drehen
        
    def linksDrehen(self):
        self.kit.motor1.throttle = self.drehen
        self.kit.motor2.throttle = -self.drehen
        self.kit.motor3.throttle = self.drehen
        self.kit.motor4.throttle = -self.drehen
        
    def stop(self):
        self.kit.motor1.throttle = 0
        self.kit.motor2.throttle = 0
        self.kit.motor3.throttle = 0
        self.kit.motor4.throttle = 0
        print("stop")
        
if __name__ == '__main__':
    main()
    