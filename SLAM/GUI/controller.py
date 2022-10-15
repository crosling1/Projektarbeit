# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 21:02:15 2022

@author: sskky
"""

import board
from adafruit_motorkit import MotorKit
from math import cos, sin, pi, floor
import subprocess

kit = MotorKit(i2c=board.I2C())
PWMvor = 0.75    # 0 bis 1 entspricht 0-100% PWM beim Vorwärtsfahren
korr = 0.8       # Korrekturfaktor
PWMzur = 0.65    # entspricht dem Faktor der PWM beim Rückwärtsfahren
drehen = 0.75    # entspricht dem Faktor der PWM bei der Drehung


def vorwaerts():
    kit.motor1.throttle = PWMvor
    kit.motor2.throttle = korr * PWMvor
    kit.motor3.throttle = PWMvor
    kit.motor4.throttle = korr * PWMvor
    print("start")

def zurueck():
    kit.motor1.throttle = -PWMzur
    kit.motor2.throttle = -PWMzur
    kit.motor3.throttle = -PWMzur
    kit.motor4.throttle = -PWMzur
    print("reverse")
    
def rechtsDrehen():
    kit.motor1.throttle = -drehen
    kit.motor2.throttle = drehen
    kit.motor3.throttle = -drehen
    kit.motor4.throttle = drehen
    print("right")
    
def linksDrehen():
    kit.motor1.throttle = drehen
    kit.motor2.throttle = -drehen
    kit.motor3.throttle = drehen
    kit.motor4.throttle = -drehen
    print("left")
    
def stop():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0
    print("stop")
    
def scan():  
    with subprocess.Popen(
            ['rosrun rplidar_ros rplidarNodeClient'], 
            stdout=subprocess.PIPE,
            shell=True,
            encoding="utf-8",
    ) as result: 
        output = result.stdout.readline()
        print("successed")
        print(output)
    return output



    