#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import cv2

"""
Blog:   http://testpy.hatenablog.com/entry/2017/07/13/003000
GitHub: https://github.com/iShoto/testpy/tree/master/samples/util
"""

def video_to_frames(video_file='F:/Project/7SegMatrixMovieCutter/Movie/original/badapple.mpg',
                    image_dir='F:/Project/7SegMatrixMovieCutter/Movie/original/image_dir/',
                    image_file='s%s.bmp'):
    # Delete the entire directory tree if it exists.
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)

    # Make the directory if it doesn't exist.
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Video to frames
    i = 0
    cap = cv2.VideoCapture(video_file)
    while(cap.isOpened()):
        flag, frame = cap.read()  # Capture frame-by-frame
        if flag == False:  # Is a frame left?
            break
        
        # 画像を7セグ用にリサイズ
        resized_frame = cv2.resize(frame, (640, 480))

        cv2.imwrite(image_dir + image_file % str(i).zfill(4), resized_frame)  # Save a frame

        print('Save', image_dir + image_file % str(i).zfill(4))
        i += 1

    cap.release()  # When everything done, release the capture

if __name__ == '__main__':
    video_to_frames()
    
