import numpy as np
import cv2
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import argparse
import sys
import detect


parser = argparse.ArgumentParser()
parser.add_argument('image', help='Path to the input image')
parser.add_argument('--show', '-s', help='Show the proccessed output. 0 or 1', type=int, default=0)
args = parser.parse_args()

if not (os.path.exists(args.image)):
    print('No such file or directory!')
    sys.exit()

vertices = []
index = 0
exit = True

img = cv2.imread(args.image)
img = cv2.resize(img, detect.dim)

frame = img.copy()

def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing,index,exit
    if event==cv2.EVENT_LBUTTONDOWN:
        thickness = int(img.shape[1]/80)
        drawing=True
        pt1_x,pt1_y=x,y
        cv2.line(img, (pt1_x, pt1_y), (x,y), (0,0,0), 3)
        vertices.append([x,y])
        if index >0:
            cv2.line(img,(x,y),(vertices[index-1][0], vertices[index-1][1]),(0,255,255), thickness)
            if len(vertices) == 4:
                cv2.line(img, (x,y), (vertices[0][0], vertices[0][1]), (0,255,255), thickness)
                
                cv2.putText(img, 'Maximum points reached!',
                    (int(img.shape[0]/2-45), int(img.shape[1]/2-100)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                   [0,0,255], 1)
                cv2.imshow('window',img)
                exit = False

                if cv2.waitKey(1) & 0xFF ==27:
                    pass
            
        index +=1 
        




cv2.namedWindow('window')
cv2.setMouseCallback('window',line_drawing)



while(exit):
    cv2.imshow('window',img)
    if cv2.waitKey(1) & 0xFF == 27 or exit == False:
        time.sleep(3)
        break
cv2.destroyAllWindows()




frame = cv2.resize(frame, dsize=detect.dim)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5,5), 0)

canny = cv2.Canny(blur, 50, 355)

mask = np.zeros_like(frame[:, :, 0])

if len(frame.shape) > 2:
    channel_count = frame.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
else:
    ignore_mask_color = 255

points = np.array([[[vertices[0][0], vertices[0][1]],
                    [vertices[1][0], vertices[1][1]],
                    [vertices[2][0], vertices[2][1]],
                    [vertices[3][0], vertices[3][1]]]], dtype=np.int32)

cv2.fillPoly(mask, points, ignore_mask_color)

masked = cv2.bitwise_and(canny, mask)


lines = cv2.HoughLinesP(masked, 1, np.pi/180, 30, np.array([]),20,20)
line_img = np.zeros((*frame.shape, 3), dtype=np.uint8)

thickness = int(frame.shape[1]/80)

blank = frame[:, :, :]
# Drawing lines
try:
    for line in lines:
        for a1,b1,a2,b2 in line:
            cv2.line(blank, (a1,b1), (a2,b2), (0,255,255), thickness)
except:
    pass
frame = cv2.addWeighted(blank, 0.5, frame, 1., 0.)
output_path = 'output/image/output.jpg'

cv2.imwrite(output_path, frame)



if(args.show) == 1:
    cv2.imshow('Result', frame)
    while True:
        if cv2.waitKey(1) & 0xff == 27:
            print('BYEEEE')
            cv2.destroyAllWindows()
            break
