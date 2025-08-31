import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import time
from tracker import*
import firebase_admin
from firebase_admin import db, credentials
# load Tarined Model
model=YOLO('yolov8s.pt')

# #connect with firebase database
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred,{
#     'databaseURl':'https://vehicels-tracking-count-default-rtdb.firebaseio.com/'
# })

#tracker event
def Traffic_Track(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        point = [x, y]
        # print(point)
  
        
#video and live camera load
cap=cv2.VideoCapture('tf.mp4')
#cap=cv2.VideoCapture(0)

#dataset load
my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

# requires variables
trackerc=Tracker()
trackerb=Tracker()
trackert=Tracker()
trackerm=Tracker()
cy1=184
cy2=209
offset=8
count=0
encar={}
levcar={}
countercaren=[]
countercarlev=[]

downbus={}
counterbusdown=[]
upbus={}
counterbusup=[]

entruck={}
countertrucken=[]
levtruck={}
countertrucklev=[]

enmotorcycle={}
countermotorcycleen=[]
levmotorcycle={}
countermotorcyclelev=[]

# Initialize timer
last_update_time = time.time()

while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(1020,500))
    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    listc=[] #car class
    listb=[] #bus class
    listt=[] #truck class
    listm=[] #motorcycle class
    for index,row in px.iterrows():
#        print(row)
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'car' in c:
           listc.append([x1,y1,x2,y2])
          
        elif'bus' in c:
            listb.append([x1,y1,x2,y2])
          
        elif 'truck' in c:
             listt.append([x1,y1,x2,y2])

        elif 'motorcycle' in c:
            listm.append([x1, y1, x2, y2])
            
    #for car
    bbox_idxc=trackerc.update(listc)
    #for bus
    bbox_idxb = trackerb.update(listb)
    #for truck
    bbox_idxt = trackert.update(listt)
    #For motorcycle
    bbox_idxm = trackerm.update(listm)


##################################FOR CAR COUNTING################################################
    for bboxc in bbox_idxc:
        x3,y3,x4,y4,idc=bboxc
        cx3=int(x3+x4)//2
        cy3=int(y3+y4)//2
        # -----------------------------car up------------------------------
        if cy1<(cy3+offset) and cy1>(cy3-offset):
            encar[idc]=(cx3,cy3)
        if idc in encar:
            if cy2 < (cy3 + offset) and cy2 > (cy3 - offset):
                cv2.circle(frame,(cx3,cy3),4,(255,0,0),-1)
                cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,255),2)
                cvzone.putTextRect(frame,f'{idc}',(x3,y3), 1,1)
                if countercaren.count(idc)==0:
                    countercaren.append(idc)
#-----------------------------car Down------------------------------
        if cy2<(cy3+offset) and cy2>(cy3-offset):
            levcar[idc]=(cx3,cy3)
        if idc in levcar:
            if cy1 < (cy3 + offset) and cy1 > (cy3 - offset):
                cv2.circle(frame,(cx3,cy3),4,(255,255,0),-1)
                cv2.rectangle(frame,(x3,y3),(x4,y4),(255,0,255),2)
                cvzone.putTextRect(frame,f'{idc}',(x3,y3), 1,1)
                if countercarlev.count(idc)==0:
                    countercarlev.append(idc)

##################################FOR BUS COUNTING ################################################
    for bboxb in bbox_idxb:
        x5,y5,x6,y6,idb=bboxb
        cx4=int(x5+x6)//2
        cy4=int(y5+y6)//2
        # -----------------------------BUS up------------------------------
        if cy1 < (cy4 + offset) and cy1 > (cy4 - offset):
            upbus[idb] = (cx4, cy4)
        if idb in upbus:
            if cy2 < (cy4 + offset) and cy2 > (cy4 - offset):
                cv2.circle(frame, (cx4, cy4), 4, (255, 0, 0), -1)
                cv2.rectangle(frame, (x5, y5), (x6, y6), (255, 0, 255), 2)
                cvzone.putTextRect(frame, f'{idb}', (x5, y5), 1, 1)
                if counterbusup.count(idb) == 0:
                    counterbusup.append(idb)
 # -----------------------------BUS Down------------------------------
        if cy2 < (cy4 + offset) and cy2 > (cy4 - offset):
            downbus[idb] = (cx4, cy4)
        if idb in downbus:
            if cy1 < (cy4 + offset) and cy1 > (cy4 - offset):
                cv2.circle(frame, (cx4, cy4), 4, (255, 255, 0), -1)
                cv2.rectangle(frame, (x5, y5), (x6, y6), (255, 0, 255), 2)
                cvzone.putTextRect(frame, f'{idb}', (x5, y5), 1, 1)
                if counterbusdown.count(idb) == 0:
                    counterbusdown.append(idb)

####################################### FOR TRUCK COUNTING  ######################################################
    for bboxt in bbox_idxt:
        x7,y7,x8,y8,idt=bboxt
        cx5=int(x7+x8)//2
        cy5=int(y7+y8)//2

        # -----------------------------TRUCK ENTERING------------------------------
        if cy1<(cy5+offset) and cy1>(cy5-offset):
            entruck[idt]=(cx5,cy5)
        if idt in entruck:
            if cy2 < (cy5 + offset) and cy2 > (cy5 - offset):
                cv2.circle(frame,(cx5,cy5),4,(255,0,0),-1)
                cv2.rectangle(frame,(x7,y7),(x8,y8),(255,0,255),2)
                cvzone.putTextRect(frame,f'{idt}',(x7,y7), 1,1)
                if countertrucken.count(idt)==0:
                    countertrucken.append(idt)
 # -----------------------------TRUCK LEAVING ------------------------------
        if cy2 < (cy5 + offset) and cy2 > (cy5 - offset):
            levtruck[idt] = (cx5, cy5)
        if idt in levtruck:
            if cy1 < (cy5 + offset) and cy1 > (cy5 - offset):
                cv2.circle(frame, (cx5, cy5), 4, (255, 255, 0), -1)
                cv2.rectangle(frame, (x7, y7), (x8, y8), (255, 0, 255), 2)
                cvzone.putTextRect(frame, f'{idt}', (x7, y7), 1, 1)
                if countertrucklev.count(idt) == 0:
                    countertrucklev.append(idt)

####################################### FOR MOTORCYCLE COUNTING  ######################################################
    for bboxm in bbox_idxm:
        x9, y9, x10, y10, idm = bboxm
        cx6 = int(x9 + x10) // 2
        cy6 = int(y9 + y10) // 2

        # -----------------------------MOTORCYCLE ENTERING------------------------------
        if cy1 < (cy6 + offset) and cy1 > (cy6 - offset):
            enmotorcycle[idm] = (cx6, cy6)
        if idm in enmotorcycle:
            if cy2 < (cy6 + offset) and cy2 > (cy6 - offset):
                cv2.circle(frame, (cx6, cy6), 4, (255, 0, 0), -1)
                cv2.rectangle(frame, (x9, y9), (x10, y10), (255, 0, 255), 2)
                cvzone.putTextRect(frame, f'{idm}', (x9, y9), 1, 1)
                if countermotorcycleen.count(idm) == 0:
                    countermotorcycleen.append(idm)
        # -----------------------------MOTORCYCLE LEAVING ------------------------------
        if cy2 < (cy6 + offset) and cy2 > (cy6 - offset):
            levmotorcycle[idm] = (cx6, cy6)
        if idt in levmotorcycle:
            if cy1 < (cy6 + offset) and cy1 > (cy6 - offset):
                cv2.circle(frame, (cx6, cy6), 4, (255, 255, 0), -1)
                cv2.rectangle(frame, (x9, y9), (x10, y10), (255, 0, 255), 2)
                cvzone.putTextRect(frame, f'{idm}', (x9, y9), 1, 1)
                if countermotorcyclelev.count(idm) == 0:
                    countermotorcyclelev.append(idm)

    cv2.line(frame,(1,cy1),(1018,cy1),(0,255,0),2)
    cv2.line(frame,(3,cy2),(1016,cy2),(0,0,255),2)
    #COUNTING THROUGH A VARIABLE
    caren=len(countercaren)
    carlev=len(countercarlev)
    busen=len(counterbusup)
    buslev=len(counterbusdown)
    trucken=len(countertrucken)
    trucklev=len(countertrucklev)
    motorcycleen=len(countermotorcycleen)
    motorcyclelev=len(countermotorcyclelev)
#=============================== UPDATE DATA TO FIREBASE DATABSE ==============================
    # # Update database every 10 seconds
    # current_time = time.time()
    # if current_time - last_update_time >= 10:
    #     last_update_time = current_time
    #
    #     # # For CAR
    #     refc = db.reference(f'VEHICELS_STATUS/CAR')
    #     refc.child('Entering_CAR').set(caren)
    #     refc.child('Leaving_CAR').set(carlev)
    #
    #     # For BUS
    #     refb = db.reference(f'VEHICELS_STATUS/BUS')
    #     refb.child('Entering_BUS').set(busen)
    #     refb.child('Leaving_BUS').set(buslev)
    #
    #     # #For TRUCK
    #     reft = db.reference(f'VEHICELS_STATUS/TRUCK')
    #     reft.child('Entering_TRUCK').set(trucken)
    #     reft.child('Leaving_TRUCK').set(trucklev)
    #
    #     # FOR MOTORCYCLE
    #     refm = db.reference(f'VEHICELS_STATUS/MOTORCYCLE')
    #     refm.child('Entering_MOTORCYCLE').set(motorcycleen)
    #     refm.child('Leaving_MOTORCYCLE').set(motorcyclelev)

########################### SHOWING INFORMATION ON THE SCREEN ############################
    cvzone.putTextRect(frame, "NUMBER OF VEHICLES ENTERING:", (10, 30), 1.5, 2,(255, 255, 255),(0, 220, 0))
    cvzone.putTextRect(frame, "NUMBER OF VEHICLES LEAVING:", (620, 30), 1.5, 2,(255, 255, 255),(0, 0, 220))
    cvzone.putTextRect(frame, "Authorized BY: MASUM", (220, 490), 1.5, 2,(255, 255, 255),(0, 0, 220))

    ################# INFORMATION FOR ENTERING VEHICLES ############################################
    cvzone.putTextRect(frame, f'CAR: {caren}', (20, 75), 2, 2,(0, 0, 220),(255, 255, 255))
    cvzone.putTextRect(frame, f'BUS: {busen}', (160, 75), 2, 2,(0, 0, 220),(255, 255, 255))
    cvzone.putTextRect(frame, f'TRUCK: {trucken}', (20, 125), 2, 2,(0, 0, 220),(255, 255, 255))
    cvzone.putTextRect(frame, f'BIKE: {motorcycleen}', (300, 75), 2, 2,(0, 0, 220),(255, 255, 255))

    ################# INFORMATION FOR LEAVING  VEHICLES ############################################
    cvzone.putTextRect(frame, f'CAR: {carlev}', (620, 75), 2, 2)
    cvzone.putTextRect(frame, f'BUS: {buslev}', (760, 75), 2, 2)
    cvzone.putTextRect(frame, f'TRUCK: {trucklev}', (860, 125), 2, 2)
    cvzone.putTextRect(frame, f'BIKE: {motorcyclelev}', (900, 75), 2, 2)

    cv2.imshow("Traffic_Track", frame)
    # if cv2.waitKey(0)&0xFF==27:
    #     break
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
