#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import serial
import json

# 仮想COMポートなのでボーレートは無意味
ser = serial.Serial('COM58', 1000000)

try_count = 1000
total_time = 0
for i in range(try_count):
    start_time = time.time()

    ###
    ser.write('#1\n'.encode())
    line = ser.readline()
    panel = json.loads(line)
    ###

    elapsed_time = time.time() - start_time
    total_time += elapsed_time

    print('[%d] ' % i, end='')
    print(panel)
    time.sleep(0.010)
    

print(panel)
print('ave = %f[msec]' % (total_time / try_count))

ser.close()
