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

def exec_csv_spectrum():
    # 仮想COMポートなのでボーレートは無意味
    ser = serial.Serial('COM52', 1000000)
    
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

        # 更新回数表示
        panel[0][23] = num_to_pattern[count // 1 % 10]
        panel[0][22] = num_to_pattern[count // 10 % 10]
        panel[0][21] = num_to_pattern[count // 100 % 10]
        panel[0][20] = num_to_pattern[count // 1000 % 10]
  
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

######################################################################

import wave
import pyaudio
import scipy as sp
import numpy as np
import math

# fftpt=1024 -> 511点を24点にどう集約するか．
# ※1点毎の分解能は約43Hz(=44100Hz/1024pt)
""" 単純置換型
2,  2,  2,  2,
2,  2,  2,  2,
4,  4,  4,  4,
8,  8,  32, 32,
10, 16, 24, 32,
48, 50, 76, 92,
"""
bandHz = [
     1, 1, 1, 1,
     2, 2, 2, 2,
     2, 2, 4, 4,
     4, 4, 8, 8, 
     16,16,32,32,
     64,64,96,128,
]

FFT_SIZE = 1024

def exec_wav_spectrum():
    # 仮想COMポートなのでボーレートは無意味
    ser = serial.Serial('COM52', 1000000)

    hamming_win = sp.hamming(FFT_SIZE)

    wavefile = wave.open('mtank.wav', 'rb')
    frames = wavefile.readframes(wavefile.getnframes())
    # ±1の範囲に正規化
    wavedata = sp.fromstring(frames, dtype='int16') / 32768.0
    wavefile.rewind()
    
    pa = pyaudio.PyAudio()
    print('WAV: [OK]')

    count = 0
    gain = 1.00
    fps = 60.0
    
    def callback(in_data, frame_count, time_info, status):
        frames = wavefile.readframes(frame_count)
        wave = sp.fromstring(frames, dtype='int16')
        
        # 再生音量にもゲイン適用
        gained_wave = wave * gain
        gained_wave = np.clip(gained_wave, -32768, +32767)
        data = bytes(gained_wave.astype(np.int16))

        return (data, pyaudio.paContinue)

    stream = pa.open(format = pa.get_format_from_width(wavefile.getsampwidth()),
                     channels = wavefile.getnchannels(),
                     rate = wavefile.getframerate(),
                     output = True,
                     stream_callback = callback)
    stream.start_stream()

    start_time = time.time()

    while (stream.is_active()):
        # ゲイン調整
        if ((count % 10) == 0):
            gain = read_gain(ser)
            print('gain=%.2f' % gain)

        # 経過時間からフレーム箇所を特定してそこをFFTする
        # data[1024](要正規化) --> spec[24]
        frame_time = time.time() - start_time
        frame_pos = int(frame_time * wavefile.getframerate())

        fft_input = wavedata[frame_pos : frame_pos + FFT_SIZE]

        # ゲイン適用
        fft_input = fft_input * gain
        
        if (len(fft_input) < FFT_SIZE):
            fft_input = np.zeros(FFT_SIZE)
        fft_output = sp.fft(fft_input * hamming_win)
        
        ########################################
        y = []
        
        toStep = 0
        fromStep = 0
        specSize = 513

        for i in range(len(bandHz)):
            bandStep = bandHz[i]
            
            toStep += bandStep
            if (toStep > specSize):
                toStep = specSize

            bandAve = 0.0
            j = fromStep
            while (j < toStep):
                bandDB = 0.0
                if (abs(fft_output[j]) >= 0.001):
                    bandDB = 2 * (20 * ((math.log10(abs(fft_output[j])))))
                    bandDB = (20 * ((math.log10(abs(fft_output[j])))))
                    
                    if (bandDB < 0):
                        bandDB = 0
                bandAve += bandDB
                j += 1
            # 平均値
            bandAve /= bandStep
            fromStep = toStep
            
            # 最終加工
            bandAve /= 1.5

            y.append(int(bandAve))
        ########################################

        spec = y

        panel = spec_to_panel(spec)

        # 更新回数表示
        panel[0][23] = num_to_pattern[count // 1 % 10]
        panel[0][22] = num_to_pattern[count // 10 % 10]
        panel[0][21] = num_to_pattern[count // 100 % 10]
        panel[0][20] = num_to_pattern[count // 1000 % 10]
  
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

    stream.stop_stream()
    stream.close()
    wavefile.close()
    pa.terminate()
    
    print('%f [s]' % elapsed_time)
    print('fps = %f' % (count / elapsed_time))
    print('Done.')
    

if __name__ == '__main__':
    #exec_csv_spectrum()
    exec_wav_spectrum()
    # TODO:
    # exec_mic_spectrum()
