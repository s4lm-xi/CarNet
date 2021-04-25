import cv2
import numpy as np 
import time
import sys
import os
import argparse

# Take arguments from the user
parser = argparse.ArgumentParser()
parser.add_argument('-thresh', '-t', help='The threshold value of each frame 0-100. lower for darker areas, higher for brighter areas. Default is 30', default=30, type=int)
args = parser.parse_args()

# Intizialing some variables
exit = True
vertices = []
drawing = False 
pt1_x , pt1_y = None , None
index = 0



def line_drawing(event,x,y,flags,param):
    global pt1_x,pt1_y,drawing,index,exit
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        thickness = int(img.shape[0]/80)
        pt1_x,pt1_y=x,y
        cv2.line(img, (pt1_x, pt1_y), (x,y), (0,0,0), 3)
        # Appending the x and y coordinates to create a ROI later on
        vertices.append([x,y])
    
        if index >0:
            # Draw a line
            cv2.line(img,(x,y),(vertices[index-1][0], vertices[index-1][1]),(0,255,255), thickness)
            if len(vertices) == 4:
                cv2.line(img, (x,y), (vertices[0][0], vertices[0][1]), (0,255,255), thickness)
                
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
video = cv2.VideoCapture(0)
while(exit):
    if read:
        _, frame = video.read()
        img = cv2.resize(frame, (278,182))
        read = False

    cv2.imshow('window',img)
    if cv2.waitKey(1) & 0xFF == 27 or not exit:
        time.sleep(3)
        break

cv2.destroyAllWindows()
video.release()

video = cv2.VideoCapture(0)
dim = (278,182)
while (video.isOpened):
    
    # Reading a frame of the video on loop
    _, frame = video.read()

    #print('Done!')
    #print(f'Processed {index} frames!')

    # Resizing based on user input
    res = cv2.resize(frame, (dim))
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
    points = np.array([[[vertices[0][0], vertices[0][1]],
                          [vertices[1][0], vertices[1][1]],
                          [vertices[2][0], vertices[2][1]],
                          [vertices[3][0], vertices[3][1]]]], dtype=np.int32)
    # Fill the mask
    cv2.fillPoly(mask, points, ignore_mask_color)

    masked = cv2.bitwise_and(canny, mask)


    # Extract lines coordinates
    lines = cv2.HoughLinesP(masked, 1, np.pi/180, args.thresh, np.array([]),20,20)
    line_img = np.zeros((*res.shape, 3), dtype=np.uint8)

    blank = np.zeros_like(res[:, :, :])
    # Drawing lines, if found any....
    try:
        for line in lines:
            thickness = int(res.shape[0]/80)
            for z1,b1,z2,b2 in line:
                cv2.line(blank, (z1,b1), (z2,b2), (0,255,255), thickness)
    except:
        pass



    final = cv2.addWeighted(blank ,0.8, res, 1.0,0.)
    
    cv2.imshow('result', final)
    if cv2.waitKey(1) & 0XFF == 27:
        break

video.release()
cv2.destroyAllWindows()