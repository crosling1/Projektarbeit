# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 21:02:15 2022

@author: sskky
"""

import board
from adafruit_motorkit import MotorKit
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar

kit = MotorKit(i2c=board.I2C())
PWMvor = 0.75    # 0 bis 1 entspricht 0-100% PWM beim Vorwärtsfahren
korr = 0.8       # Korrekturfaktor
PWMzur = 0.65    # entspricht dem Faktor der PWM beim Rückwärtsfahren
drehen = 0.75    # entspricht dem Faktor der PWM bei der Drehung
SCAN_BYTE = b'\x20'
SCAN_TYPE = 129
scan_data = [0]*360
# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)


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
    
    
def _process_scan(raw):
    '''Processes input raw data and returns measurment data'''
    new_scan = bool(raw[0] & 0b1)
    inversed_new_scan = bool((raw[0] >> 1) & 0b1)
    quality = raw[0] >> 2
    if new_scan == inversed_new_scan:
        #raise RPLidarException('New scan flags mismatch')
        lidar_measurments()      
    check_bit = raw[1] & 0b1
    if check_bit != 1:
        raise RPLidarException('Check bit not equal to 1')
    angle = ((raw[1] >> 1) + (raw[2] << 7)) / 64.
    distance = (raw[3] + (raw[4] << 8)) / 4.
    return new_scan, quality, angle, distance

    
def lidar_measurments(self, max_buf_meas=500):
       
        lidar.set_pwm(660)
        status, error_code = self.health
        
        cmd = SCAN_BYTE
        self._send_cmd(cmd)
        dsize, is_single, dtype = self._read_descriptor()
        if dsize != 5:
            raise RPLidarException('Wrong info reply length')
        if is_single:
            raise RPLidarException('Not a multiple response mode')
        if dtype != SCAN_TYPE:
            raise RPLidarException('Wrong response data type')
        while True:
            raw = self._read_response(dsize)
            self.log_bytes('debug', 'Received scan response: ', raw)
            if max_buf_meas:
                data_in_buf = self._serial_port.in_waiting
                if data_in_buf > max_buf_meas*dsize:
                    self.log('warning',
                             'Too many measurments in the input buffer: %d/%d. '
                             'Clearing buffer...' %
                             (data_in_buf//dsize, max_buf_meas))
                    self._serial_port.read(data_in_buf//dsize*dsize)
            yield _process_scan(raw)
    
def lidar_scans(self, max_buf_meas=500, min_len=5):
        
        scan = []
        iterator = lidar_measurments(lidar,max_buf_meas)
        for new_scan, quality, angle, distance in iterator:
            if new_scan:
                if len(scan) > min_len:
                    yield scan
                scan = []
            if quality > 0 and distance > 0:
                scan.append((quality, angle, distance))
    
#pylint: disable=redefined-outer-name,global-statement
def process_data():
    global max_distance
    print("start")  
    for scan in lidar_scans(lidar):
       for (_, angle, distance) in scan:
           scan_data[min([359, floor(angle)])] = distance
           print(angle, distance)

    for angle in range(360):
        distance = scan_data[angle]
        print(angle, distance)                  # ignore initially ungathered data points
            




    