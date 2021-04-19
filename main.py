import cv2
import numpy as np 
import time
import sys
import argparse
import warnings
import os
import detect

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('input',help='Location of the input video')
parser.add_argument('-show', '-s', default=0, help='Show the output video immediately when the processing is finished. 0 or 1', type=int)
parser.add_argument('-alert', '-a', default=0, help='Play an alert sound when detection is finished. 0 or 1', type=int)
args = parser.parse_args()

if not os.path.exists(args.input):
    print('No such file or directory!')
    sys.exit()



exit = True
vertices = []
drawing = False 
pt1_x , pt1_y = None , None
index = 0



def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing,index,exit
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        pt1_x,pt1_y=x,y
        cv2.line(img, (pt1_x, pt1_y), (x,y), (0,0,0), 3)
        vertices.append([x,y])
    
        if index >0:
            cv2.line(img,(x,y),(vertices[index-1][0], vertices[index-1][1]),(0,255,255), 3)
            if len(vertices) == 4:
                cv2.line(img, (x,y), (vertices[0][0], vertices[0][1]), (0,255,255), 3)
                
                cv2.putText(img, 'Maximum points reached!',
                    (int(img.shape[0]/2-45), int(img.shape[1]/2-100)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                   [0,0,255], 1)
                cv2.imshow('window',img)
                if cv2.waitKey(1) & 0xFF ==27:
                    pass
                exit = False
            
        index +=1 
        




cv2.namedWindow('window')
cv2.setMouseCallback('window',line_drawing)


read = True
video = cv2.VideoCapture(args.input)


while(exit):
    if read:
        _, frame = video.read()
        img = cv2.resize(frame, detect.dim)
        read = False

    cv2.imshow('window',img)
    if cv2.waitKey(1) & 0xFF == 27 or not exit:
        time.sleep(3)
        break

cv2.destroyAllWindows()

detect.detect(args.input,   vertices[0][0], vertices[0][1],   vertices[1][0], vertices[1][1],   vertices[2][0], vertices[2][1],   vertices[3][0], vertices[3][0], args.alert, args.show)


