# -*- coding: utf-8 -*-



import cv2
from tensorflow.keras.models import load_model
from detect1 import pre_dect
import os
import numpy as np
prototxtPath = "./face_detector/deploy.prototxt"
weightsPath ="./face_detector/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath,weightsPath)
model=load_model('mask_detector.model')
def get_img():
    f=[]
    for file in os.listdir('./imgssave/'):
        f.append(file)
    path="./imgssave/"+f[0]
    frame=cv2.imread(path,cv2.IMREAD_COLOR)
    try:
        (locs, preds)=pre_dect(frame,faceNet,model)
        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            cla=np.argmax(pred[0])
            label = "Mask" if cla==0 else "No Mask"
            color = (0, 255, 0) if cla == 0 else (0, 0, 255)

    		# include the probability in the label
            label = "{}: {:.2f}%".format(label, max(pred[0]) * 100)
            cv2.putText(frame, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        try:
            for i in os.listdir('./static/detectedimgs/'):
                file='./imgssave/detectedimgs/'+i
                os.remove(file)          
        except:
            pass
        #cv2.imshow('frame',frame)
        cv2.imwrite('./static/detectedimgs/img_3.jpg',frame)
    except :
        pass