import cv2
import time
import numpy as np
import HandTrackinkgModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################################
wCam, hCam, = 1280, 700 # camera frame angle
################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
# cTime = 0
detector = htm.handDedector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(0, None)     ###this code line also helps in measuring volume range
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) !=0:
        # print(lmList[4], lmList[8]) # numbers 4 and 8 here represent landmarks

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2) // 2

        cv2.circle(img, (x1, y1), 11, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 11, (0, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.circle(img, (cx, cy), 11, (0, 0, 0), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #print(length)        ### this line of code prints max and min between two fingers

        # Hand range min 50 - max 300
        # Volume range -65 - 0

        vol = np.interp(length, [30, 200], [minVol, maxVol])
        volBar = np.interp(length, [30, 200], [400, 150])
        volPer = np.interp(length, [30, 200], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 11, (255, 255, 255), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400),(0, 0, 255), 2)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, f'Volume:%{int(volPer)} ', (90, 170), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 40), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)









