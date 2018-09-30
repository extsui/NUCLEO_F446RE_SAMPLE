#!/usr/bin/python
# -*- coding: utf-8 -*-

def to_real_panel(panel):
    """2次元配列から7SegArmorの実配列への変換

    <armor0>        <armor1>         <armor2>
    panel[0][0:8]   panel[0][8:16]   panel[0][16:24]
    panel[1][0:8]   panel[1][8:16]   panel[1][16:24]
    panel[2][0:8]   panel[2][8:16]   panel[2][16:24]
    panel[3][0:8]   panel[3][8:16]   panel[3][16:24]
    
    <armor3>        <armor4>         <armor5>
    panel[4][0:8]   panel[4][8:16]   panel[4][16:24]
    panel[5][0:8]   panel[5][8:16]   panel[5][16:24]
    panel[6][0:8]   panel[6][8:16]   panel[6][16:24]
    panel[7][0:8]   panel[7][8:16]   panel[7][16:24]
    """
    real_panel = [
        [ panel[0][0:8],   panel[1][0:8],   panel[2][0:8],   panel[3][0:8],   ],
        [ panel[0][8:16],  panel[1][8:16],  panel[2][8:16],  panel[3][8:16],  ],
        [ panel[0][16:24], panel[1][16:24], panel[2][16:24], panel[3][16:24], ],
        [ panel[4][0:8],   panel[5][0:8],   panel[6][0:8],   panel[7][0:8],   ],
        [ panel[4][8:16],  panel[5][8:16],  panel[6][8:16],  panel[7][8:16],  ],
        [ panel[4][16:24], panel[5][16:24], panel[6][16:24], panel[7][16:24], ],
    ]
    return real_panel

def to_armor_command(real_panel, finger_cmd):
    """7SegArmorの実配列からコマンドへの変換"""
    command = []
    for armor in range(6):
        for y in range(4):
            command.append(finger_cmd)
            for x in range(8):
                command.append(real_panel[armor][y][x])
    return command

def panel_to_command(panel, finger_cmd):
    """パネルからコマンドへの変換"""
    real_panel = to_real_panel(panel)
    command = to_armor_command(real_panel, finger_cmd)
    
    # 数値のリスト --> 16進文字列のリスト --> 結合
    str_list = [ format(i, '02X') for i in command ]
    str = '#0' + ''.join(str_list) + '\n'
    return str

######################################################################

def spec_to_panel(spec):
    """スペックからパネルに変換

    <org> <LV0> <LV1> <LV2> <LV3> <LV4> 
     ---                     ---        
    |   |                   |   | |   | 
     ---               ---              
    |   |             |   | |   | |   | 
     ---         ---                    
    """
    # 2次元配列[8][24]
    panel = [ [ 0 for x in range(24) ] for y in range(8) ]
    
    LV0 = 0x00
    LV1 = 0x10
    LV2 = 0x2A
    LV3 = 0xEC
    LV4 = 0x6C
    
    bar_table = [
        [ LV0, LV0, LV0, LV0, LV0, LV0, LV0, LV0 ], # 0
        [ LV0, LV0, LV0, LV0, LV0, LV0, LV0, LV1 ], # 1
        [ LV0, LV0, LV0, LV0, LV0, LV0, LV0, LV2 ], # 2
        [ LV0, LV0, LV0, LV0, LV0, LV0, LV0, LV3 ], # 3
        [ LV0, LV0, LV0, LV0, LV0, LV0, LV1, LV4 ], # 4
        [ LV0, LV0, LV0, LV0, LV0, LV0, LV2, LV4 ], # 5
        [ LV0, LV0, LV0, LV0, LV0, LV0, LV3, LV4 ], # 6
        [ LV0, LV0, LV0, LV0, LV0, LV1, LV4, LV4 ], # 7
        [ LV0, LV0, LV0, LV0, LV0, LV2, LV4, LV4 ], # 8
        [ LV0, LV0, LV0, LV0, LV0, LV3, LV4, LV4 ], # 9
        [ LV0, LV0, LV0, LV0, LV1, LV4, LV4, LV4 ], # 10
        [ LV0, LV0, LV0, LV0, LV2, LV4, LV4, LV4 ], # 11
        [ LV0, LV0, LV0, LV0, LV3, LV4, LV4, LV4 ], # 12
        [ LV0, LV0, LV0, LV1, LV4, LV4, LV4, LV4 ], # 13
        [ LV0, LV0, LV0, LV2, LV4, LV4, LV4, LV4 ], # 14
        [ LV0, LV0, LV0, LV3, LV4, LV4, LV4, LV4 ], # 15
        [ LV0, LV0, LV1, LV4, LV4, LV4, LV4, LV4 ], # 16
        [ LV0, LV0, LV2, LV4, LV4, LV4, LV4, LV4 ], # 17
        [ LV0, LV0, LV3, LV4, LV4, LV4, LV4, LV4 ], # 18
        [ LV0, LV1, LV4, LV4, LV4, LV4, LV4, LV4 ], # 19
        [ LV0, LV2, LV4, LV4, LV4, LV4, LV4, LV4 ], # 20
        [ LV0, LV3, LV4, LV4, LV4, LV4, LV4, LV4 ], # 21
        [ LV1, LV4, LV4, LV4, LV4, LV4, LV4, LV4 ], # 22
        [ LV2, LV4, LV4, LV4, LV4, LV4, LV4, LV4 ], # 23
        [ LV3, LV4, LV4, LV4, LV4, LV4, LV4, LV4 ], # 24～
    ]
    
    num_to_pattern = [
        0xfc, # 0
        0x60, # 1
        0xda, # 2
        0xf2, # 3
        0x66, # 4
        0xb6, # 5
        0xbe, # 6
        0xe4, # 7
        0xfe, # 8
        0xf6, # 9
    ]

    for x in range(24):
        if (spec[x] > 24):
            spec[x] = 24
        
        for y in range(8):
            panel[y][x] = bar_table[spec[x]][y]
        
        if (spec[x] / 3 >= 9):
            bottom_num = 9
        else:
            bottom_num = (spec[x] // 3)
        
        # 最下段はスペックの数値表示
        panel[7][x] = num_to_pattern[bottom_num]
    
    # 更新回数表示
    panel[0][23] = num_to_pattern[count // 1 % 10]
    panel[0][22] = num_to_pattern[count // 10 % 10]
    panel[0][21] = num_to_pattern[count // 100 % 10]
    panel[0][20] = num_to_pattern[count // 1000 % 10]
    
    # 最下段は全部点灯した方が奇麗なのでは?
    for x in range(24):
        panel[6][x] |= 0x11
    
    return panel

######################################################################

import time
import serial
import csv
import json

def read_gain(ser):
    """入力パネルからゲイン値読出し"""
    ser.write('#1\n'.encode())
    line = ser.readline()
    input_panel = json.loads(line)
    raw_gain = input_panel['gain']
    gain = (raw_gain * 2 / 4096.0)
    # -----+-------
    # 入力 | ゲイン
    # -----+-------
    # 0    | 0.00
    # 2048 | 1.00
    # 4095 | 2.00
    # -----+-------
    return gain

def write_display(ser, xfer_data):
    ser.write(xfer_data.encode())


if __name__ == '__main__':

    # 仮想COMポートなのでボーレートは無意味
    ser = serial.Serial('COM58', 1000000)
    
    f = open('mtank_16384pt_60fps.csv', 'r')
    reader = csv.reader(f)
    print('CSV: [OK]')
    
    count = 0
    
    gain = 1.00
    fps = 60.0
    start_time = time.time()
    
    for row in reader:        
        # ゲイン調整
        if ((count % 10) == 0):
            gain = read_gain(ser)
            print('gain=%.2f' % gain)
        
        # ゲイン適用
        spec = list(map(lambda x: (int)((int(x) * gain * 1.0 / 1.5)), row))
        
        panel = spec_to_panel(spec)
        xfer_data = panel_to_command(panel, 0x01)
        write_display(ser, xfer_data)
        
        # fpsの値に合わせて規定時間になるまで待つ
        expected_time = start_time + (((1000.0 / fps) * count) / 1000)
        while (time.time() < expected_time):
            time.sleep(0.001)
            print('_', end='')
        
        count += 1
    
    elapsed_time = time.time() - start_time
    ser.close()
    
    print('%f [s]' % elapsed_time)
    print('fps = %f' % (count / elapsed_time))
    print('Done.')
