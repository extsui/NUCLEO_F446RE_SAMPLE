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

    
    # <長方形版>
    LV0 = 0x00
    LV1 = 0x10
    LV2 = 0x2A
    LV3 = 0xEC
    LV4 = 0x6C
    

    """
    # <天井のみ版>
    LV0 = 0x00
    LV1 = 0x10
    LV2 = 0x02 #0x2A
    LV3 = 0x10 #0xEC
    LV4 = 0x00 #0x6C
    """

    """
    # <影版>→没。歯抜け見たいでカッコ悪い。
    LV0 = 0x00
    LV1 = 0x10
    LV2 = 0b22
    LV3 = 0bE0
    LV4 = 0b60
    """
    
    """
    # <一直線版> ドットを削ると控え目になる。
    LV0 = 0x00
    LV1 = 0x01 & 0xFE
    LV2 = 0x21 & 0xFE
    LV3 = 0x61 & 0xFE
    LV4 = 0x61 & 0xFE
    """
    
    """
    # <二直線版>→没。長方形版の下位互換。
    LV0 = 0x00
    LV1 = 0x00
    LV2 = 0x28
    LV3 = 0x6C
    LV4 = 0x6C
    """
    
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
    
        """
        モード切り替え判定
        """
        ser.write('md\n'.encode())
        line = ser.readline()
        if (int(line) is 1):
            print('Mode Switch!')
            break

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
    
    if (elapsed_time > 0):
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

FFT_SIZE = 1024*4

def exec_wav_spectrum():
    # 仮想COMポートなのでボーレートは無意味
    ser = serial.Serial('COM52', 1000000)

    hamming_win = np.hamming(FFT_SIZE)

    wavefile = wave.open('mtank.wav', 'rb')
    frames = wavefile.readframes(wavefile.getnframes())
    # ±1の範囲に正規化
    wavedata = np.frombuffer(frames, dtype='int16') / 32768.0
    wavefile.rewind()
    
    pa = pyaudio.PyAudio()
    print('WAV: [OK]')

    count = 0
    gain = 1.00
    fps = 60.0
    
    def callback(in_data, frame_count, time_info, status):
        frames = wavefile.readframes(frame_count)
        wave = np.frombuffer(frames, dtype='int16')
        
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

        """
        モード切り替え判定
        """
        ser.write('md\n'.encode())
        line = ser.readline()
        if (int(line) is 1):
            print('Mode Switch!')
            break

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
        fft_output = sp.fft.fft(fft_input * hamming_win)
        
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

    if (elapsed_time > 0):
        print('%f [s]' % elapsed_time)
        print('fps = %f' % (count / elapsed_time))
    print('Done.')

######################################################################

import numpy as np

def read_input_panel(ser):
    """入力パネルから各種情報読出し"""
    ser.write('#1\n'.encode())
    line = ser.readline()
    return json.loads(line)

def exec_badapple():
    # 仮想COMポートなのでボーレートは無意味
    ser = serial.Serial('COM52', 1000000)

    fps = 29.97
    gain = 1.00

    """ 表示 """
    bindata = np.fromfile('BADAPPLE_30FPS.7SM', np.uint8)
    print('BadApple: [OK]')
    frame_num = len(bindata) / 128
    
    """ 音声 """
    wavefile = wave.open('badapple.wav', 'rb')
    frames = wavefile.readframes(wavefile.getnframes())
    wavefile.rewind()
    pa = pyaudio.PyAudio()
    print('WAV: [OK]')

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

    """ 再生 """
    count = 0
    start_time = time.time()

    while (count < frame_num):

        """
        モード切り替え判定
        """
        ser.write('md\n'.encode())
        line = ser.readline()
        if (int(line) is 1):
            print('Mode Switch!')
            break

        """
        # ゲイン調整
        if ((count % 10) == 0):
            gain = read_gain(ser)
            print('gain=%.2f' % gain)
        """
        # 1フレーム毎に読み込んでも特に遅延無し
        gain = read_gain(ser)

        panel = [ [ 0 for x in range(24) ] for y in range(8) ]

        frame_data = bindata[count*128 : (count+1)*128]

        panel[0][0:16] = frame_data[16*0:16*1]
        panel[1][0:16] = frame_data[16*1:16*2]
        panel[2][0:16] = frame_data[16*2:16*3]
        panel[3][0:16] = frame_data[16*3:16*4]
        panel[4][0:16] = frame_data[16*4:16*5]
        panel[5][0:16] = frame_data[16*5:16*6]
        panel[6][0:16] = frame_data[16*6:16*7]
        panel[7][0:16] = frame_data[16*7:16*8]

        # 更新回数表示
        panel[0][23] = num_to_pattern[count // 1 % 10]
        panel[0][22] = num_to_pattern[count // 10 % 10]
        panel[0][21] = num_to_pattern[count // 100 % 10]
        panel[0][20] = num_to_pattern[count // 1000 % 10]
  
        # 各種パラメータ表示
        input_panel = read_input_panel(ser)

        panel[2][23] = num_to_pattern[input_panel['gain'] // 1 % 10]
        panel[2][22] = num_to_pattern[input_panel['gain'] // 10 % 10]
        panel[2][21] = num_to_pattern[input_panel['gain'] // 100 % 10]
        panel[2][20] = num_to_pattern[input_panel['gain'] // 1000 % 10]

        panel[4][23] = num_to_pattern[input_panel['brightness'] // 1 % 10]
        panel[4][22] = num_to_pattern[input_panel['brightness'] // 10 % 10]
        panel[4][21] = num_to_pattern[input_panel['brightness'] // 100 % 10]
        panel[4][20] = num_to_pattern[input_panel['brightness'] // 1000 % 10]

        panel[6][23] = num_to_pattern[input_panel['cycle'] // 1 % 10]
        panel[6][22] = num_to_pattern[input_panel['cycle'] // 10 % 10]
        panel[6][21] = num_to_pattern[input_panel['cycle'] // 100 % 10]
        panel[6][20] = num_to_pattern[input_panel['cycle'] // 1000 % 10]

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
    if (elapsed_time > 0):
        print('%f [s]' % elapsed_time)
        print('fps = %f' % (count / elapsed_time))
    print('Done.')
    
######################################################################

import copy
import math

class MicSpectrum:  
    """ 単純置換型
    2, 2, 2, 2,
    2, 2, 2, 2,
    4, 4, 4, 4,
    8, 8, 32, 32,
    10, 16, 24, 32,
    48, 50, 76, 92,
    """
    bandHz = [
        2, 2, 2, 2,
        2, 2, 2, 2,
        4, 4, 4, 4,
        8, 8, 32, 32,
        10, 16, 24, 32,
        48, 50, 76, 92,
    ]

    def __init__(self):
        # マイクインプット
        self.CHUNK = 1024
        # 8000だと異常に遅くなる。おそらくH/Wサポート外の可能性有り。
        self.RATE = 44100
        self.update_msec = 50
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format = pyaudio.paInt16,
                                      channels = 1,
                                      rate = self.RATE,
                                      frames_per_buffer = self.CHUNK,
                                      input = True,
                                      output = False,
                                      stream_callback = self.audio_input)
        
        # 音声データの格納場所(プロットデータ)
        self.buffer = np.zeros(self.CHUNK)
        
    """
    TODO:
    ある程度データを貯めてから一気に処理する．
    これはプロットにかかる時間よりもPyAudioの処理に時間がかかるため．
    """
    def audio_input(self, data, frame_count, time_info, status_flag):
        # frames_per_bufferサイズずつ渡される(=frame_count)
        self.buffer = np.frombuffer(data, dtype="int16") / 32768.0
        return (data, pyaudio.paContinue)

    def analyze(self):
        signal = copy.copy(self.buffer)
        spec = self.stft(signal)

        toStep = 0
        fromStep = 0
        specSize = 513

        result = []
        for i in range(len(bandHz)):
            bandStep = bandHz[i]
            
            toStep += bandStep
            if (toStep > specSize):
                toStep = specSize

            bandAve = 0.0
            j = fromStep
            while (j < toStep):
                bandDB = 0.0
                if (abs(spec[j]) >= 0.001):
                    bandDB = 2 * (20 * ((math.log10(abs(spec[j])))))
                    bandDB = (20 * ((math.log10(abs(spec[j])))))
                    
                    if (bandDB < 0):
                        bandDB = 0
                bandAve += bandDB
                j += 1
            # 平均値
            bandAve /= bandStep
            fromStep = toStep
            
            # 最終加工
            bandAve /= 1.5

            result.append(int(bandAve))

        return result

    def stft(self, data):
        data = np.hamming(len(data)) * data
        data = np.fft.fft(data)
        #data = np.abs(data)
        
        # スペクトルデータの加工
        #data = np.sqrt(data) * 2
        #data = map(int, data)
        
        return data

def exec_mic_spectrum():
    # 仮想COMポートなのでボーレートは無意味
    ser = serial.Serial('COM52', 1000000)

    mic_spec = MicSpectrum()

    count = 0
    gain = 1.00
    fps = 60.0
    
    start_time = time.time()

    while (True):
        """
        モード切り替え判定
        """
        ser.write('md\n'.encode())
        line = ser.readline()
        if (int(line) is 1):
            print('Mode Switch!')
            break

        # ゲイン調整
        if ((count % 10) == 0):
            gain = read_gain(ser)
            print('gain=%.2f' % gain)

        spec = mic_spec.analyze()
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

    if (elapsed_time > 0):
        print('%f [s]' % elapsed_time)
        print('fps = %f' % (count / elapsed_time))
    print('Done.')

######################################################################

from SegPatternGenerator import *
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
from datetime import datetime

def exec_display():
    
    ser = serial.Serial('COM52', 1000000)

    spg = SegPatternGenerator()
    font = ImageFont.truetype('C:\Windows\Fonts\msgothic.ttc', 180)

    count = 0
    fps = 2.0

    start_time = time.time()

    while (True):
        """
        モード切り替え判定
        """
        ser.write('md\n'.encode())
        line = ser.readline()
        if (int(line) is 1):
            print('Mode Switch!')
            break
        
        pil_img = Image.new('1', (spg.SCREEN_WIDTH, spg.SCREEN_HEIGHT))
        draw = ImageDraw.Draw(pil_img)
        
        """時計表示"""
        now = datetime.now()
        text = '%02d:%02d' % (now.hour, now.minute)
        """0.5秒置きにコロンを点滅"""
        if ((now.microsecond / 1000) >= 500):
            text = text.replace(':', ' ')
        draw.text((10, 31), text, fill=255, font=font)
        
        """右上の一部領域を塗りつぶし"""
        draw.polygon(((420, 0), (480, 60), (480, 0)), fill=255)

        """ネガの方が見やすいので反転"""
        pil_img = ImageChops.invert(pil_img)

        """PIL画像からOpenCV画像に変換"""
        pil_img = pil_img.convert('L')
        cv_img = np.asarray(pil_img)

        """入力画像から7セグパターン生成"""
        pattern = spg.match(cv_img)
        
        """秒表示"""
        pattern[0][22] = num_to_pattern[now.second // 10 % 10]
        pattern[0][23] = num_to_pattern[now.second // 1 % 10]
        """微調整"""
        pattern[0][21] &= ~0b0000_0001
        pattern[1][23] |=  0b0000_0001
        '''
        """パターン出力結果確認"""
        cv_img = spg.create_seven_seg_pattern_image(pattern)
        cv2.imshow('Title', cv_img)
        
        k = cv2.waitKey(1)
        if k == 27:
            break
        '''
        xfer_data = panel_to_command(pattern, 0x01)
        write_display(ser, xfer_data)

        # fpsの値に合わせて規定時間になるまで待つ
        expected_time = start_time + (((1000.0 / fps) * count) / 1000)
        while (time.time() < expected_time):
            time.sleep(0.001)
            print('_', end='')
        print('')
        
        count += 1
    
    elapsed_time = time.time() - start_time
    
    ser.close()

    if (elapsed_time > 0):
        print('%f [s]' % elapsed_time)
        print('fps = %f' % (count / elapsed_time))
    print('Done.')

######################################################################

if __name__ == '__main__':
    while (True):
        exec_csv_spectrum()
        exec_wav_spectrum()
        exec_mic_spectrum()
        exec_badapple()
        exec_display()
    