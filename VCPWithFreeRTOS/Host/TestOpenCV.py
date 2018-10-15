#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import cv2

"""グレースケール画像で操作する"""
img = np.zeros((480, 640, 1), np.uint8)

"""7セグ描画テスト"""
POINT_SEG_A = np.array([ [14, 7],  [32, 7],  [33, 8],  [30, 11], [16, 11], [13, 8]  ], np.int32)
POINT_SEG_B = np.array([ [34, 10], [36, 12], [33, 26], [31, 28], [29, 26], [31, 13] ], np.int32)
POINT_SEG_C = np.array([ [30, 31], [33, 34], [30, 48], [29, 49], [26, 46], [28, 33] ], np.int32)
POINT_SEG_D = np.array([ [24, 47], [27, 50], [26, 51], [9, 51],  [8, 50],  [11, 47] ], np.int32)
POINT_SEG_E = np.array([ [9, 30],  [11, 32], [9, 46],  [6, 49],  [4, 47],  [7, 32]  ], np.int32)
POINT_SEG_F = np.array([ [11, 9],  [14, 12], [11, 26], [9, 28],  [7, 26],  [10, 10] ], np.int32)
POINT_SEG_G = np.array([ [13, 27], [27, 27], [29, 29], [27, 31], [13, 31], [11, 29] ], np.int32)

img = cv2.fillPoly(img, [POINT_SEG_A], 255)
img = cv2.fillPoly(img, [POINT_SEG_B], 255)
img = cv2.fillPoly(img, [POINT_SEG_C], 255)
img = cv2.fillPoly(img, [POINT_SEG_D], 255)
img = cv2.fillPoly(img, [POINT_SEG_E], 255)
img = cv2.fillPoly(img, [POINT_SEG_F], 255)
img = cv2.fillPoly(img, [POINT_SEG_G], 255)
img = cv2.circle(img, (35, 49), 3, 255, thickness=-1)

"""文字描画テスト"""
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV', (100, 100), font, 4, 255, 10, cv2.LINE_AA)

cv2.imwrite('test.png', img)
cv2.imshow('title', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
