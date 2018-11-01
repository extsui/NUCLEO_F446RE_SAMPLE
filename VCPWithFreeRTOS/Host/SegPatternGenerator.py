# -*- coding: utf-8 -*-
import numpy as np
import cv2

class SegPatternGenerator:
    """7セグパターン生成器"""

    """全体のスケール
    1(960, 480)を想定していたが処理速度が
    遅かったため、2(480, 240)に変更。"""
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

    ############################################################
    #  事前処理
    ############################################################
    def __init__(self):
        self.all_matching_points = self.__get_all_matching_points()
        
    def __get_points_of_polygon(self, poly_points):
        """多角形を構成する座標群を返す"""
        img = np.zeros((SegPatternGenerator.SEG_HEIGHT,
                        SegPatternGenerator.SEG_WIDTH), np.uint8)
        img = cv2.fillPoly(img, [poly_points], 255)
        points = []
        for y in range(SegPatternGenerator.SEG_HEIGHT):
            for x in range(SegPatternGenerator.SEG_WIDTH):
                if (img[y, x] == 255):
                    points.append([y, x])
        return points

    def __get_points_of_circle(self, center, radius):
        """円を構成する座標群を返す"""
        img = np.zeros((SegPatternGenerator.SEG_HEIGHT,
                        SegPatternGenerator.SEG_WIDTH), np.uint8)
        img = cv2.circle(img, center, radius, 255, thickness=-1)
        points = []
        for y in range(SegPatternGenerator.SEG_HEIGHT):
            for x in range(SegPatternGenerator.SEG_WIDTH):
                if (img[y, x] == 255):
                    points.append([y, x])
        return points

    def __get_seven_seg_points(self):
        """7セグを構成する座標群を返す"""
        return [
            self.__get_points_of_polygon(SegPatternGenerator.POINT_SEG_A),
            self.__get_points_of_polygon(SegPatternGenerator.POINT_SEG_B),
            self.__get_points_of_polygon(SegPatternGenerator.POINT_SEG_C),
            self.__get_points_of_polygon(SegPatternGenerator.POINT_SEG_D),
            self.__get_points_of_polygon(SegPatternGenerator.POINT_SEG_E),
            self.__get_points_of_polygon(SegPatternGenerator.POINT_SEG_F),
            self.__get_points_of_polygon(SegPatternGenerator.POINT_SEG_G),
            self.__get_points_of_circle(SegPatternGenerator.POINT_SEG_DOT_CENTER,
                                      SegPatternGenerator.POINT_SEG_DOT_RADIUS),
        ]

    def __get_all_matching_points(self):
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
        seven_seg_points = self.__get_seven_seg_points()
        seven_y = []
        for y in range(0, SegPatternGenerator.SCREEN_HEIGHT, SegPatternGenerator.SEG_HEIGHT):
            seven_x = []
            for x in range(0, SegPatternGenerator.SCREEN_WIDTH, SegPatternGenerator.SEG_WIDTH):
                base = [y, x]
                seven_seg_points_based = [ (np.array(seven_seg_points[i]) + np.array(base)) for i in range(8) ]
                seven_x.append(seven_seg_points_based)
            seven_y.append(seven_x)
        return seven_y

    ############################################################
    #  リアルタイム処理
    ############################################################
    def match(self, cv_img):
        """
        画像から7セグパターンとマッチングした結果を返す
        @param cv_img (SCREEN_WIDTH, SCREEN_HEIGHT)のuint8型のNumPy二次元配列
        @return (SCREEN_WIDTH, SCREEN_HEIGHT)のuint8型のNumPy二次元配列
        """
        return self.__create_seven_seg_pattern(cv_img)
    
    def __is_seg_light(self, img, seg_pts):
        """入力画像imgに対してseg_ptsで指定した座標群が半分以上閾値以上ならTrueを返す"""
        and_count = 0
        for [y, x] in seg_pts:
            if (img.item(y, x) >= 127):
                and_count += 1
        if (and_count >= len(seg_pts)):
            return True
        else:
            return False

    def __create_seven_seg_pattern(self, img):
        pattern = np.zeros((SegPatternGenerator.SEG_Y_NUM,
                            SegPatternGenerator.SEG_X_NUM), np.uint8)
        for seven_y in range(SegPatternGenerator.SEG_Y_NUM):
            for seven_x in range(SegPatternGenerator.SEG_X_NUM):
                bit_pattern = 0x00
                for seg in range(8):
                    if (self.__is_seg_light(img, self.all_matching_points[seven_y][seven_x][seg])):
                        bit_pattern |= (1 << (7 - seg))
                pattern[seven_y][seven_x] = bit_pattern
        return pattern

    def create_seven_seg_pattern_image(self, pattern):
        """7セグパターンの画像を作成する(出力結果確認用)"""
        img = np.zeros((SegPatternGenerator.SCREEN_HEIGHT,
                        SegPatternGenerator.SCREEN_WIDTH), np.uint8)
        for y in range(SegPatternGenerator.SEG_Y_NUM):
            for x in range(SegPatternGenerator.SEG_X_NUM):
                bit_pattern = pattern[y][x]
                for seg in range(8):
                    if (bit_pattern & (1 << (7 - seg))):
                        for point in self.all_matching_points[y][x][seg]:
                            img.itemset((point[0], point[1]), 255)
        return img

    def print_seven_seg_pattern(self, pattern):
        """7セグパターンを標準出力に表示する(出力結果確認用)"""
        for y in range(SegPatternGenerator.SEG_Y_NUM):
            for x in range(SegPatternGenerator.SEG_X_NUM):
                print('%02X' % int(pattern[y][x]), end='')
            print('')
        print('')

if __name__ == '__main__':
    from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
    
    spg = SegPatternGenerator()
    font = ImageFont.truetype('C:\Windows\Fonts\meiryob.ttc', 144)
    
    print('Font: Load OK!')

    count = 0
    for i in range(0, 10000, 1):
        """加工元画像"""
        pil_img = Image.new('1', (spg.SCREEN_WIDTH, spg.SCREEN_HEIGHT))
        draw = ImageDraw.Draw(pil_img)
        draw.text(( - (i * 8 % (spg.SCREEN_WIDTH * 4)) + 1000, 10), u'ext@漢字明朝', fill=255, font=font)

        back_img = Image.new('1', (spg.SCREEN_WIDTH, spg.SCREEN_HEIGHT))
        draw_back = ImageDraw.Draw(back_img)

        radius = (i*8) % ((spg.SCREEN_WIDTH * 1.5) // 2)
        fill_color = 0
        if ((i*8) % (spg.SCREEN_WIDTH * 1.5) > radius):
            fill_color = 0
            back_img = ImageChops.invert(back_img)
        else:
            fill_color = 255
        
        box_top_xy = (spg.SCREEN_WIDTH // 2 - radius, spg.SCREEN_HEIGHT // 2 - radius)
        box_bottom_xy = (spg.SCREEN_WIDTH // 2 + radius, spg.SCREEN_HEIGHT // 2 + radius)
        draw_back.ellipse((box_top_xy, box_bottom_xy), fill=fill_color)
        
        pil_img = ImageChops.logical_xor(pil_img, back_img)

        """PIL画像からOpenCV画像に変換"""
        pil_img = pil_img.convert('L')
        cv_img = np.asarray(pil_img)

        """入力画像から7セグパターン生成"""
        pattern = spg.match(cv_img)
        
        """パターン出力結果確認"""
        cv_img = spg.create_seven_seg_pattern_image(pattern)
        cv2.imshow('Title', cv_img)

        k = cv2.waitKey(1)
        if k == 27:
            break
