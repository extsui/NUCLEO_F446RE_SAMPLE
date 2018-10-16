#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import cv2

SEG_HEIGHT = 60
SEG_WIDTH = 40

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
    pixels = []
    
    for y in range(height):
        for x in range(width):
            if (img[y, x] == 255):
                pixels.append([y, x])

    return pixels

def get_seg_points():
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

def is_seg_light(img, seg_pts):
    """入力画像imgに対してseg_ptsで指定した座標群が半分以上白ならTrueを返す"""
    and_count = 0
    for [y, x] in seg_pts:
        if (img[y, x] == 255):
            and_count += 1
    if (and_count >= len(seg_pts)):
        return True
    else:
        return False

def get_seg_light_pattern(img, seg_pts, base):
    """aaa"""
    # TODO: baseを足す
    ptn = 0x00
    for i in range(8):
        if (is_seg_light(img_test, seg_pts[i])):
            bit = 1
        else:
            bit = 0
        ptn |= (bit << (7 - i))
    return ptn

def draw_7seg():
    """7セグ描画"""
    img = np.zeros((SEG_HEIGHT, SEG_WIDTH, 1), np.uint8)
    img = cv2.fillPoly(img, [POINT_SEG_A], 255)
    img = cv2.fillPoly(img, [POINT_SEG_B], 255)
    img = cv2.fillPoly(img, [POINT_SEG_C], 255)
    img = cv2.fillPoly(img, [POINT_SEG_D], 255)
    img = cv2.fillPoly(img, [POINT_SEG_E], 255)
    img = cv2.fillPoly(img, [POINT_SEG_F], 255)
    img = cv2.fillPoly(img, [POINT_SEG_G], 255)
    img = cv2.circle(img, POINT_SEG_DOT_CENTER,
                     POINT_SEG_DOT_RADIUS, 255, thickness=-1)
    return img

"""文字描画テスト"""
"""
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV', (100, 100), font, 4, 255, 10, cv2.LINE_AA)
"""

if __name__ == '__main__':
    img_test = cv2.imread('mintest.png', cv2.IMREAD_GRAYSCALE)
    img_7seg = draw_7seg()
    
    seg_pts = get_seg_points()

    # ベース座標。これを移動させることでマッチングを進める。
    base_y = 0
    base_x = 0
    base = [ base_y, base_x ]

    pattern = get_seg_light_pattern(img_test, seg_pts, base)
    print('%02X' % pattern)
    
    img = cv2.bitwise_and(img_7seg, img_test)
    cv2.imshow('Title', img)
    #cv2.imwrite('test.png', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

