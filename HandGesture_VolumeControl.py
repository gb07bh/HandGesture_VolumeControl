# This Project ha been made by Gaurav Bhanot.
#  Dated : 29th May 2021
import cv2
import mediapipe as mp
import sys
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

cam = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success , img = cam.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
               
                h , w, c = img.shape
                cx , cy =  int(lm.x*w) ,int(lm.y*h)
                lmList.append([id, cx, cy])
            mpDraw.draw_landmarks(img,handLms, mpHands.HAND_CONNECTIONS)
        
        if lmList:
            
            x1 ,x2 = lmList[4][1], lmList[4][2]
            y1, y2 = lmList[8][1], lmList[8][2]
     
            # Making marks on tips of thumb and index fingers
            cv2.circle(img, (x1,x2), 10, (0,0,255), cv2.FILLED)
            cv2.circle(img, (y1,y2), 10, (0,0,255), cv2.FILLED)
           

            cv2.line(img, (x1,x2),(y1,y2),(128,0,0),3)
           
            # To calculate lenth of line we will use math function .hypot
            len = math.hypot(y1- x1, y2-x2)
            # print(len)  # Length varies with distance from the camera as well
            if len < 50:
                a1 = (x1+y1)//2
                a2 = (x2+y2)//2
                cv2.circle(img, (a1,a2), 10, (260,120,100), cv2.FILLED)
            

   
   
    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]

    # Comparing using interp()
    vol = np.interp(len , [20, 165],[minVol, maxVol])# comparing 20  to volume being 0 and  165 to be 100
    volBar = np.interp(len , [20, 165],[400 , 150])  
    volperc = np.interp(len, [20,165],[0,100])
    # please run this command in your system as it varies from device to device.
    volume.SetMasterVolumeLevel(vol, None)  # for my device -65.25 is 0% and 0.00 is 100%
    
   
    cv2.rectangle(img, (50,150), (85,400), (102,35,0), 5)
    cv2.rectangle(img,(50,int(volBar)), (85,400),(53,76,196), cv2.FILLED)
    cv2.putText(img, f'{int(volperc)}%' , (40,430), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0,0,0),2)
    cv2.putText(img, 'Volume',(25,145),cv2.FONT_ITALIC,1,(0,0,0),4) 
    
    
    cv2.imshow("Image", img)
    #Press key 'a' to exit
    if cv2.waitKey(1) == ord('a'):
        sys.exit()

