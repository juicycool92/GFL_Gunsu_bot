import numpy as np
import cv2
from matplotlib import pyplot as plt
import pyautogui
import time

class cannyTargetFinder :
    target = 0
    threshold = 0.0
    def __init__(self,_targetURI,_threshold):
        _target = cv2.imread(_targetURI,cv2.IMREAD_GRAYSCALE)
        cannyTargetFinder.target = cv2.Canny(_target,50,200)
        cannyTargetFinder.threshold = _threshold
        print('read done')
    def search(self, _object) :
        gray = cv2.cvtColor(_object,cv2.COLOR_BGR2GRAY)
        tW,tH = (cannyTargetFinder.target).shape[::-1]
        res = cv2.matchTemplate(gray,cannyTargetFinder.target,cv2.TM_CCOEFF)
        loc  = np.where(res >= cannyTargetFinder.threshold)
        ###############
        #cv2.imshow('target',cannyTargetFinder.target)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        # upper codes are for test target image
        #####################
        if len(loc[0]) == 0 :
            returnState = [-1,-1]
            return returnState
        else :
            min_v,max_v,min_loc,max_loc = cv2.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0]+tW,top_left[1]+tH)
            cv2.rectangle(gray,top_left,bottom_right,(0,255,255),5)

            curTime = str(int(time.time()))
            cv2.imwrite(curTime+'['+str(cannyTargetFinder.threshold)+'][canny].jpg',gray)
            returnState = [(top_left[0]+((bottom_right[0] - top_left[0])/2)),(top_left[1] + ((bottom_right[1] - top_left[1])/2))]
            return returnState

class imgFinder :
    target = 0
    threshold = 0.0
    def __init__(self,_targetURI,_threshold):
        imgFinder.target = cv2.imread(_targetURI,cv2.IMREAD_GRAYSCALE)
        imgFinder.threshold = _threshold
        print('read done')
    def search(self, _object) :
        gray = cv2.cvtColor(_object,cv2.COLOR_BGR2GRAY)
        tW,tH = (imgFinder.target).shape[::-1]
        res = cv2.matchTemplate(gray,imgFinder.target,cv2.TM_CCOEFF_NORMED)
        loc  = np.where(res >= imgFinder.threshold)
        #cv2.imshow('target',imgFinder.target)
        #cv2.waitKey(0)
        
        if len(loc[0]) == 0 :
            returnState = [-1,-1]
            return returnState
        else :
            min_v,max_v,min_loc,max_loc = cv2.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0]+tW,top_left[1]+tH)
            cv2.rectangle(gray,top_left,bottom_right,(0,255,255),5)
            #for pt in zip(*loc[::-1]):
            #    cv2.rectangle(gray,pt,(pt[0]+tW,pt[1]+tH),(0,255,255),2)

            curTime = str(int(time.time()))
            cv2.imwrite(curTime+'['+str(imgFinder.threshold)+'][normal].jpg',gray)
            returnState = [(top_left[0]+((bottom_right[0] - top_left[0])/2)),(top_left[1] + ((bottom_right[1] - top_left[1])/2))]
            return returnState

class windowCapture :
    _win = None
    win = None
    def capture(self) :
        self._win = np.array(pyautogui.screenshot())
        self.win = self._win[r[1]:r[1]+r[3] , r[0] : r[0]+r[2]] 
        return self.win

print('pref program')
arriveFinder = cannyTargetFinder('targetAlerm.jpg',1.0)
confirmFinder = imgFinder('targetBtn.jpg',0.5)
winCap = windowCapture()
print('drag ROI and press Enter')
#sc = pyautogui.screenshot()
img = np.array(pyautogui.screenshot())
r = cv2.selectROI('select',img)
cv2.destroyWindow('select')

print('gunsu looper starting...')
time.sleep(1)
while(1) :
    
    winC = winCap.capture()
    arrivePos = arriveFinder.search(winC)

    if arrivePos[0] != -1 :
        pyautogui.moveTo(r[0]+(arrivePos[0]),r[1]+(arrivePos[1]))
        pyautogui.click()
        isFindConfirm = False
        while isFindConfirm == False:
            winC = winCap.capture()
            confirmPos = confirmFinder.search(winC)
            if confirmPos[0] != -1 :
                pyautogui.moveTo(r[0]+(confirmPos[0]),r[1]+(confirmPos[1]))
                pyautogui.click()
                isFindConfirm = True
                print('resend done')
            else :
                time.sleep(5)
    
    #cv2.destroyAllWindows()
    time.sleep(5)
