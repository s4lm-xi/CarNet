import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import subprocess as s
from tqdm import tqdm
import pygame
import math
import sys
import os
import shutil

# Dimensions
dim = (278,182)

def detect(input_path, x1,y1,x2,y2,x3,y3,x4,y4, alert, show):
    video = cv2.VideoCapture(input_path)
    index = 0
    folder = 'frames/'
    x = True
    
    # Delete frames folder content
    print(f'Deleting contents of {folder}...')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print('Done!')
    print('.')
    print('.')
    print('.')
            
    while True:
        # Reading a frame of the video on loop
        _, frame = video.read()
        if not _:
            print('Done!')
            print(f'Processed {index} frames!')
            break
        else:
            # Resizing based on user input
            res = cv2.resize(frame, dim)
            # Grayscaling
            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            # Blurring the image for better edge detection
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            # Edge detection
            canny = cv2.Canny(blur, 50, 355)
            # Creating a mask of the intitial image
            mask = np.zeros_like(gray[:, :])

            if len(res.shape) > 2:
                channel_count = res.shape[2]  
                ignore_mask_color = (255,) * channel_count
            else:
                ignore_mask_color = 255
            # Specifing the points of the polygon to set the ROI
            vertices = np.array([[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]], dtype=np.int32)
            # Fill the mask
            cv2.fillPoly(mask, vertices, ignore_mask_color)

            masked = cv2.bitwise_and(canny, mask)
          

            # Extract lines coordinates
            lines = cv2.HoughLinesP(masked, 1, np.pi/180, 30, np.array([]),20,20)
            line_img = np.zeros((*res.shape, 3), dtype=np.uint8)

            blank = np.zeros_like(res[:, :, :])
            # Drawing lines, if found any....
            try:
                for line in lines:
                    for z1,b1,z2,b2 in line:
                        cv2.line(blank, (z1,b1), (z2,b2), (0,255,255), 3)
            except:
                pass
                    
            
                
            final = cv2.addWeighted(blank ,0.8, res, 1.0,0.)
  
            # Saving the processed image
            cv2.imwrite(f'frames/{index}.jpg', final)
            index+=1
            
            
            
    fps = 30
    path = 'frames/'
    name = 'output/output.avi'



    img_file = [path+str(i)+'.jpg' for i in range(len(os.listdir(path)))]

    video = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'XVID'), fps, dim)
    print('Processing an output video..')
    
    for image in tqdm(img_file):
        video.write(cv2.imread(image))
    print(f'Saved video as {name}')

    cv2.destroyAllWindows()
    video.release()
            
    if alert==1:
        pygame.mixer.init()
        pygame.mixer.music.load("alert.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue        
        s.call(['notify-send', 'Detection Done!'])
        do = False
    
    if show==1:
        video = cv2.VideoCapture(name)

        while True:
            try:
                _, frame = video.read()
                cv2.imshow('output video', frame)

                if cv2.waitKey(30) & 0xff==27:
                    break
            except:
                break
    cv2.destroyAllWindows()