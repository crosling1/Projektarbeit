import board
import time
from adafruit_motorkit import MotorKit
import curses
import os

kit = MotorKit(i2c=board.I2C())

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

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
    
def rechtsDrehen():
    kit.motor1.throttle = -drehen
    kit.motor2.throttle = drehen
    kit.motor3.throttle = -drehen
    kit.motor4.throttle = drehen
    
def linksDrehen():
    kit.motor1.throttle = drehen
    kit.motor2.throttle = -drehen
    kit.motor3.throttle = drehen
    kit.motor4.throttle = -drehen
    
def stop():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_UP:
            vorwaerts()
        elif char == curses.KEY_DOWN:
            zurueck()
        elif char == curses.KEY_RIGHT:
            rechtsDrehen()
        elif char == curses.KEY_LEFT:
            linksDrehen()
        elif char == 43:
            if PWMvor < 1:
                PWMvor += 0.05
                if PWMvor > 1:
                    PWMvor = 1
            os.system('clear')
            print(round(PWMvor, 2))
            vorwaerts()
        elif char == 45:
            if PWMvor > 0:
                PWMvor -= 0.05
                if PWMvor < 0:
                    PWMvor = 0
            os.system('clear')
            print(round(PWMvor, 2))
            vorwaerts()
        elif char == 32:
            stop()
        
finally:
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    



