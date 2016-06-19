import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import sys
import time
import ImageGrab
import Image
from os import environ
import random
import serial
from math import fabs
import cv2.cv as cv
from common import clock, draw_str



box = (0,500,600,825) # The ImageGrab.grab() function accepts one argument which defines a bounding box. This is a tuple of coordinates following the pattern of (x,y,x,y) - http://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117
# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
method = cv2.TM_CCOEFF_NORMED
ser = 0
img = ImageGrab.grab(box)
img.save('C:\\test.png','PNG')
daEffettuareIlReload = 0
distanza = 0
distanza_penultima = 0
distanza_secondultima = 0
distanza_terzultima = 0
t = clock()



#Function to Initialize the Serial Port
def init_serial():
    COMNUM = 9          #Enter Your COM Port Number Here.
    global ser          #Must be declared in Each Function
    ser = serial.Serial()
    ser.baudrate = 57600
    ser.port = COMNUM - 1   #COM Port Name Start from 0
    ser.timeout = 10
    ser.open()          #Opens SerialPort
    # print port open or closed
    if ser.isOpen():
        print 'Open: ' + ser.portstr
#Function Ends Here



init_serial()
ser.write(chr(13).encode('ascii'))
#temp = raw_input('Type what you want to send, hit enter:\r\n')




while True:

    os.system('cls') #on windows
    
    
    # CERCO TARGET
    img = cv2.imread('C:\\test.png',0)
    img2 = img.copy()
    template = cv2.imread('C:\\test_template.png',0)
    w, h = template.shape[::-1]
    img = img2.copy()
    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img,top_left, bottom_right, 255, 2)
    print("\n\nCoordinata X target (quadrato rosso): "),
    print(top_left[0])
    xTarget = top_left[0]
    yTarget = top_left[1]



    # CERCO OMINO
    template2 = cv2.imread('C:\\test_template2.png',0)
    w, h = template2.shape[::-1]
    img = img2.copy()
    # Apply template Matching
    res = cv2.matchTemplate(img,template2,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img,top_left, bottom_right, 255, 2)
    print("Coordinata X di partenza (omino): "),
    print(top_left[0])
    xOmino = top_left[0]
    yOmino = top_left[1]
    #top_left
    distanza_terzultima = distanza_secondultima
    distanza_secondultima = distanza_penultima
    distanza_penultima = distanza
    if (fabs(distanza-int(xTarget-xOmino))<3): # il risultato della ricerca tamplate puo' variare di qualche pixel
      distanza = distanza
    else:
      distanza = int(xTarget-xOmino)
    print("Distanza: "),
    print(distanza)
    print("Tasto Reload Presente? "),
    if (distanza<30):
      print("Si!")
      daEffettuareIlReload = 1
    else:
      print("No!")
      daEffettuareIlReload = 0

    
    
    if (distanza_penultima==distanza and distanza_secondultima==distanza and distanza_terzultima==distanza):
      # eseguo il tap con il Servo:
      if (daEffettuareIlReload==1):
        ser.write('8')
        ser.write('0')
        ser.write(chr(13).encode('ascii'))
      else:
        if (distanza<99):
          ser.write(distanza/10)
          ser.write(distanza-int((distanza/10))*10)
          ser.write(chr(13).encode('ascii'))
        else:
          ser.write(distanza/100)
          ser.write(int(distanza/10)-(int(distanza/100))*10)
          ser.write(distanza-(int(distanza/10))*10)
          ser.write(chr(13).encode('ascii'))
    
    
    
    ########## Costruisco la finestra grafica #################
    img_rgb = cv2.imread('C:\\test.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('C:\\test_gray.png',img_gray)
    img = cv2.imread('C:\\test_gray.png')
    #draw_str(img, (20, 20), 'Ditanza: %i pixels' % distanza)
    #font = cv2.FONT_HERSHEY_SIMPLEX
    font = cv2.FONT_HERSHEY_TRIPLEX
    cv2.putText(img,'Distanza: %i pixels'%distanza,(110,90), font, 1,(255,0,0),3)
    cv2.rectangle(img, (xTarget-20,yTarget-25), (xTarget+30, yTarget+25), (0,255,0), 2) # disegno il quadrato attorno al target trovato
    cv2.rectangle(img, (xOmino,yOmino), (xOmino+50, yOmino+50), (0,255,0), 2) # disegno il quadrato attorno all'omino trovato
    cv2.imwrite('C:\\res.png',img)
    cv2.imshow('Stick Hero Solver', img)
    if 0xFF & cv2.waitKey(5) == 27:
        break
    ##########################################################

    
       
    if (distanza_penultima==distanza and distanza_secondultima==distanza and distanza_terzultima==distanza):
      #time.sleep(3)
      time.sleep(2.1)
    else:
      print "\n\nNext picture in: 0.2 seconds"
      time.sleep(0.2)
      
      
    img = ImageGrab.grab(box)
    #img.save('C:\Users\Roby\Desktop\\test.jpg','JPEG')
    img.save('C:\\test.png','PNG')
    distanza_secondultima
    
    
cv2.destroyAllWindows()
    