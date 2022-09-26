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

class controller():
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
        try:
            while True:
                self.char = self.screen.getch()
                if self.char == ord('q'):
                    break
                elif self.char == curses.KEY_UP:
                    self.vorwaerts()
                elif self.char == curses.KEY_DOWN:
                    self.zurueck()
                elif self.char == curses.KEY_RIGHT:
                    self.rechtsDrehen()
                elif self.char == curses.KEY_LEFT:
                    self.linksDrehen()
                elif self.char == 43:
                    if self.PWMvor < 1:
                        self.PWMvor += 0.05
                        if self.PWMvor > 1:
                            self.PWMvor = 1
                    os.system('clear')
                    print(round(self.PWMvor, 2))
                    self.vorwaerts()
                elif self.char == 45:
                    if self.PWMvor > 0:
                        self.PWMvor -= 0.05
                        if self.PWMvor < 0:
                            self.PWMvor = 0
                    os.system('clear')
                    print(round(self.PWMvor, 2))
                    self.vorwaerts()
                elif self.char == 32:
                    self.stop()
                
        finally:
            curses.nocbreak(); self.screen.keypad(0); curses.echo()
            curses.endwin()
        
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
        
if __name__ == '__main__':
    app = controller()
    