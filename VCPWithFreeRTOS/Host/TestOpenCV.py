#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import cv2

############################################################
#  前処理
############################################################
"""全体のスケール
1(640, 480)を想定していたが処理速度が
遅かったため、2(320, 240)に変更。"""
SCALE = 2

"""画面サイズ"""
SCREEN_HEIGHT = 480 // SCALE
SCREEN_WIDTH  = 960 // SCALE

"""7セグ1個のサイズ"""
SEG_HEIGHT = 60 // SCALE
SEG_WIDTH  = 40 // SCALE

"""画面内の7セグ数"""
SEG_X_NUM = SCREEN_WIDTH // SEG_WIDTH
SEG_Y_NUM = SCREEN_HEIGHT // SEG_HEIGHT 

"""サイズ(x=40, y=60)における7セグLEDの各セグメント多角形の頂点座標"""
POINT_SEG_A = np.array([ [14, 7],  [32, 7],  [33, 8],  [30, 11], [16, 11], [13, 8]  ], np.int32)
POINT_SEG_B = np.array([ [34, 10], [36, 12], [33, 26], [31, 28], [29, 26], [31, 13] ], np.int32)
POINT_SEG_C = np.array([ [30, 31], [33, 34], [30, 48], [29, 49], [26, 46], [28, 33] ], np.int32)
POINT_SEG_D = np.array([ [24, 47], [27, 50], [26, 51], [9, 51],  [8, 50],  [11, 47] ], np.int32)
POINT_SEG_E = np.array([ [9, 30],  [11, 32], [9, 46],  [6, 49],  [4, 47],  [7, 32]  ], np.int32)
POINT_SEG_F = np.array([ [11, 9],  [14, 12], [11, 26], [9, 28],  [7, 26],  [10, 10] ], np.int32)
POINT_SEG_G = np.array([ [13, 27], [27, 27], [29, 29], [27, 31], [13, 31], [11, 29] ], np.int32)
POINT_SEG_DOT_CENTER = (35, 49)
POINT_SEG_DOT_RADIUS = 3

POINT_SEG_A //= SCALE
POINT_SEG_B //= SCALE
POINT_SEG_C //= SCALE
POINT_SEG_D //= SCALE
POINT_SEG_E //= SCALE
POINT_SEG_F //= SCALE
POINT_SEG_G //= SCALE
POINT_SEG_DOT_CENTER = (POINT_SEG_DOT_CENTER[0] // SCALE,
                        POINT_SEG_DOT_CENTER[1] // SCALE)
POINT_SEG_DOT_RADIUS //= SCALE

def get_points_of_polygon(poly_points):
    """多角形を構成する座標群を返す"""
    img = np.zeros((SEG_HEIGHT, SEG_WIDTH, 1), np.uint8)
    img = cv2.fillPoly(img, [poly_points], 255)

    height = img.shape[0]
    width = img.shape[1]
    pixels = []
    
    for y in range(height):
        for x in range(width):
            if (img[y, x] == 255):
                pixels.append([y, x])

    return pixels

def get_points_of_circle(center, radius):
    """円を構成する座標群を返す"""
    img = np.zeros((SEG_HEIGHT, SEG_WIDTH, 1), np.uint8)
    img = cv2.circle(img, center, radius, 255, thickness=-1)

    height = img.shape[0]
    width = img.shape[1]
    points = []
    
    for y in range(height):
        for x in range(width):
            if (img[y, x] == 255):
                points.append([y, x])

    return points

def get_seven_seg_points():
    return [
        get_points_of_polygon(POINT_SEG_A),
        get_points_of_polygon(POINT_SEG_B),
        get_points_of_polygon(POINT_SEG_C),
        get_points_of_polygon(POINT_SEG_D),
        get_points_of_polygon(POINT_SEG_E),
        get_points_of_polygon(POINT_SEG_F),
        get_points_of_polygon(POINT_SEG_G),
        get_points_of_circle(POINT_SEG_DOT_CENTER, POINT_SEG_DOT_RADIUS),
    ]

def get_all_matching_points(seven_seg_pts):
    """
    走査する全ての座標を備えたリストを作成する。
    all_points[seven_y][seven_x][seg][pts][xy]
     - seven_y[0:8]  : 7セグ1個のy座標([0]=1行目, ..., [7]=8行目)
     - seven_x[0:16] : 7セグ1個のx座標([0]=1列目, ..., [7]=16列目)
     - seg[0:8]      : 7セグの各セグメント([0]=SEG_A, ..., [7]=SEG_DOT)
     - pts[0:N]      : 各セグメントを構成する座標群([0]=SEGの1番目の座標)
     - xy[2]         : 座標[y, x]
    ※ptsは各セグメントによって個数が異なる。
    例: all_points[0][0][0][0][0]=1行1列目の7セグのSEG_Aの1番目のy座標
    """
    seven_y = []
    for y in range(0, SCREEN_HEIGHT, SEG_HEIGHT):
        seven_x = []
        for x in range(0, SCREEN_WIDTH, SEG_WIDTH):
            base = [y, x]
            seven_seg_pts_based = [
                np.array(seven_seg_pts[0]) + np.array(base),
                np.array(seven_seg_pts[1]) + np.array(base),
                np.array(seven_seg_pts[2]) + np.array(base),
                np.array(seven_seg_pts[3]) + np.array(base),
                np.array(seven_seg_pts[4]) + np.array(base),
                np.array(seven_seg_pts[5]) + np.array(base),
                np.array(seven_seg_pts[6]) + np.array(base),
                np.array(seven_seg_pts[7]) + np.array(base),
            ]
            seven_x.append(seven_seg_pts_based)
            
        seven_y.append(seven_x)

    #seven_y = np.array(seven_y)
    
    return seven_y

############################################################
#  リアルタイム処理
############################################################

def is_seg_light(img, seg_pts):
    """入力画像imgに対してseg_ptsで指定した座標群が半分以上閾値以上ならTrueを返す"""
    and_count = 0
    for [y, x] in seg_pts:
        if (img.item(y, x) >= 127):
            and_count += 1
    if (and_count >= len(seg_pts)):
        return True
    else:
        return False

def get_seven_seg_light_pattern(img, seven_seg_pts, base=[0, 0]):
    """入力画像imgに対してseg_ptsで指定した座標群"""
    ptn = 0x00

    # TODO: この座標群を全て事前計算しておくとさらに高速化できそう。
    seven_seg_pts_based = [
        np.array(seven_seg_pts[0]) + np.array(base),
        np.array(seven_seg_pts[1]) + np.array(base),
        np.array(seven_seg_pts[2]) + np.array(base),
        np.array(seven_seg_pts[3]) + np.array(base),
        np.array(seven_seg_pts[4]) + np.array(base),
        np.array(seven_seg_pts[5]) + np.array(base),
        np.array(seven_seg_pts[6]) + np.array(base),
        np.array(seven_seg_pts[7]) + np.array(base),
    ]
    for i in range(8):
        if (is_seg_light(img, seven_seg_pts_based[i])):
            bit = 1
        else:
            bit = 0
        ptn |= (bit << (7 - i))
    return ptn

############################################################
import time

def create_seven_seg_pattern(img, all_matching_points):
    pattern = np.zeros((SEG_Y_NUM, SEG_X_NUM, 1), np.uint8)
    for seven_y in range(SEG_Y_NUM):
        for seven_x in range(SEG_X_NUM):
            seg_a_pts   = all_matching_points[seven_y][seven_x][0]
            seg_b_pts   = all_matching_points[seven_y][seven_x][1]
            seg_c_pts   = all_matching_points[seven_y][seven_x][2]
            seg_d_pts   = all_matching_points[seven_y][seven_x][3]
            seg_e_pts   = all_matching_points[seven_y][seven_x][4]
            seg_f_pts   = all_matching_points[seven_y][seven_x][5]
            seg_g_pts   = all_matching_points[seven_y][seven_x][6]
            seg_dot_pts = all_matching_points[seven_y][seven_x][7]

            bit_pattern = 0x00
            if (is_seg_light(img, seg_a_pts)):
                bit_pattern |= 0x80
            if (is_seg_light(img, seg_b_pts)):
                bit_pattern |= 0x40
            if (is_seg_light(img, seg_c_pts)):
                bit_pattern |= 0x20
            if (is_seg_light(img, seg_d_pts)):
                bit_pattern |= 0x10
            if (is_seg_light(img, seg_e_pts)):
                bit_pattern |= 0x08
            if (is_seg_light(img, seg_f_pts)):
                bit_pattern |= 0x04
            if (is_seg_light(img, seg_g_pts)):
                bit_pattern |= 0x02
            if (is_seg_light(img, seg_dot_pts)):
                bit_pattern |= 0x01
            pattern[seven_y][seven_x] = bit_pattern
    return pattern

def create_matching_image(all_matching_points, pattern):
    img = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 1), np.uint8)
    for y in range(SEG_Y_NUM):
        for x in range(SEG_X_NUM):
            bit_pattern = pattern[y][x]
            for seg in range(8):
                if (bit_pattern & (1 << (7 - seg))):
                    for point in all_matching_points[y][x][seg]:
                        img[point[0], point[1]] = 255
    return img

def print_seven_seg_pattern(pattern):
    for y in range(SEG_Y_NUM):
        for x in range(SEG_X_NUM):
            print('%02X' % int(pattern[y][x]), end='')
        print('')

if __name__ == '__main__':
    #img_test = cv2.imread('mintest.png', cv2.IMREAD_GRAYSCALE)
    #img_7seg = draw_7seg()
    
    #img = cv2.imread('black.png', cv2.IMREAD_GRAYSCALE)
    #img = cv2.imread('white.png', cv2.IMREAD_GRAYSCALE)
    #img = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
    #img = cv2.resize(img, None, fx=1/SCALE, fy=1/SCALE)

    img = np.full((SCREEN_HEIGHT, SCREEN_WIDTH), 255)
    #img = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 1), np.uint8)

    """文字描画テスト"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, '0123456789', (5, 155), font, 4, 0, 10, cv2.LINE_AA)

    seven_seg_points = get_seven_seg_points()
    all_matching_points = get_all_matching_points(seven_seg_points)
    
    start_time = time.time()
    """測定区間ここから"""
    pattern = create_seven_seg_pattern(img, all_matching_points)
    """測定区間ここまで"""
    end_time = time.time()
    print(end_time - start_time)

    print_seven_seg_pattern(pattern)
    
    """パターン出力結果確認"""
    img = create_matching_image(all_matching_points, pattern)
    
    #img = cv2.bitwise_and(img_7seg, img_test)
    cv2.imshow('Title', img)
    #cv2.imwrite('test.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

