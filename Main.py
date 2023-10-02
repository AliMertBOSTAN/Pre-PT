# Ali Mert BOSTAN
# This is a sports movement control program with mediapipe created by Ali Mert Bostan.

import cv2
import mediapipe as mp
import math
from tkinter import * 
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
import numpy as np 
import tkinter as tk
from PIL import Image
from PIL import ImageTk

class poseDetector():
    def __init__(self, mode= False, upBody=False, smooth=True, detectionCon=0.75, trackCon=0.75):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

            return img
    
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:

            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)

        return self.lmList  

    def findeAngle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2, x1-x2))
        if angle < 0:
            angle = angle + 360
        
        #print(angle)

        if draw:
            cv2.line(img, (x1, y1),(x2,y2),(255,255,255),3)
            cv2.line(img, (x3, y3),(x2,y2),(255,255,255),3)

            cv2.circle(img, (x1,y1), 3,(0, 0, 255), cv2.FILLED)

            cv2.circle(img, (x1,y1), 6,(255, 0, 0), 2)

            cv2.circle(img, (x2,y2), 3,(0, 0, 255), cv2.FILLED)

            cv2.circle(img, (x2,y2), 6,(255, 0, 0), 2)

            cv2.circle(img, (x3,y3), 3,(0, 0, 255), cv2.FILLED)

            cv2.circle(img, (x3,y3), 6,(255, 0, 0), 2)

            cv2.putText(img, str(int(angle)), (x2-20, y2+50),cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255),2)

        return  angle

def DosyaAc ():
    global Dosya 
    Dosya = filedialog.askopenfilenames(title = "Video seç")
    global Dosya_yolu
    Dosya_yolu = Dosya

    return Dosya

def Kamera ():
    global Dosya 
    Dosya = [0,]
    global Dosya_yolu
    Dosya_yolu = Dosya

    return Dosya
        


        

def bicepscurl ():
    cap = cv2.VideoCapture( Dosya_yolu[0] )
    detector = poseDetector()
    count = 0
    dir = 0

    while True:
        success, img = cap.read()
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        angleSag = detector.findeAngle(img, 12, 14, 16)
        angleSol = detector.findeAngle(img, 11, 13, 15)
        per = np.interp(angleSol, (200,270),(0,100))
        if per == 100:
                if dir == 0:
                    count +=0.5
                    dir = 1
        if per == 0:
                if dir == 1:
                    count +=0.5
                    dir =0


        angle1 = detector.findeAngle(img, 13, 11, 23)

        angle2 = detector.findeAngle(img, 14, 12, 24)

        cv2.rectangle(img, (0,0), (10000,90), (0,0,0), -1)
        

        if angle1 > 30:
            cv2.putText(img, "Sol kol cok ayrik", (10,40), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 3)

        if angle2 < 320:
            cv2.putText(img, "Sag kol cok ayrik", (10,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 3)
                
        
        if angle1 <30:
            if angle2 > 320:
                cv2.putText(img, "durus dogru", (10,20), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)


        cv2.putText(img, f'{int(count)}',(300,60), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 6)
        cv2.imshow("image", img)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.imshow("image", img)
        
    cv2.destroyAllframes
    return img



def squat():
    cap = cv2.VideoCapture( Dosya_yolu[0] )
    detector = poseDetector()
    count = 0
    dir = 0

    while True:
        success, img = cap.read()
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        
        while True:
            #sol bacak
            angleSol = detector.findeAngle(img, 23, 25, 27)

            #sağ bacak
            angleSag = detector.findeAngle(img, 24, 26, 28)
            per = np.interp(angleSol, (195,287),(0,100))
            #print(angle,per)

            if per == 100:
                if dir == 0:
                    count +=0.5
                    dir = 1
            if per == 0:
                if dir == 1:
                    count +=0.5
                    dir =0
            #print(count)

            cv2.putText(img, f'{int(count)}',(520,60), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 6)
            cv2.rectangle(img, (0,0), (10000,80), (0,0,0), -1)
            angle1 = detector.findeAngle(img, 25, 23, 11)
            angle2 = detector.findeAngle(img, 26, 24, 12)
            
            if angle1 > 70:
                if angle1 < 100:
                    cv2.putText(img, "Durus dogru", (10,20), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)

                cv2.putText(img, "Durus yanlis", (10,20), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)

            if angle1 <70:
                cv2.putText(img, "Durus yanlis", (10,20), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
            
            cv2.imshow("image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllframes
        return img
        
                
           

            

def shoulderpress ():
    cap = cv2.VideoCapture( Dosya_yolu[0] )
    detector = poseDetector()
    count = 0
    dir = 0

    while True:
        success, img = cap.read()
        #img = cv2.resize(img, (1288, 720))
        #img = cv2.imread("test/test.jpg")
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        print(lmList)

        if True:

            #sol kol
            angleSol = detector.findeAngle(img, 23, 11, 13)

            #sağ kol
            angleSag = detector.findeAngle(img, 24, 12, 14)

            per = np.interp(angleSol, (230,290),(0,100))

            angle1 = detector.findeAngle(img, 11, 13, 15)
            angle2 = detector.findeAngle(img, 12, 14, 16)

            cv2.rectangle(img, (0,0), (10000,80), (0,0,0), -1)

            cv2.putText(img, f'{int(count)}',(520,60), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 6)
            if per == 100:
                if dir == 0:
                    count +=0.5
                    dir = 1
            if per == 0:
                if dir == 1:
                    count +=0.5
                    dir =0

            cv2.putText(img, f'{int(count)}',(50,180), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 5)

            if angle1 > 80:
                cv2.putText(img, "Sol Kol cok acik ", (10,20), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
            
            if angle1 < 40:
                cv2.putText(img, "Sol Kol cok kapali", (10,20), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)

            if angle2 > 310:
                cv2.putText(img, "Sag Kol cok kapali ", (10,60), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
            
            if angle2 < 270:
                cv2.putText(img, "Sag Kol cok acik", (10,60), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)    
            
            if angle1 <80:
                if angle1 >40:
                    if angle2 < 310:
                        if angle2 > 270:
                            cv2.putText(img, "durus dogru", (10,20), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("image", img)
        cv2.waitKey(1)
        cv2.destroyAllframes

        return img
        

#diğer hareketler buraya tanımlanıcak

class imgshow():
    def __init__(self,img):
        self.vid=img
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def getFrame(self):
        if self.vid.isOpened():
            isTrue, frame = self.vid.read()
            if isTrue:
                return(isTrue, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def __del__(self):
        if self.vid.isOpened():
            self.vid.relese()

#hareketler sırasında elden edilen img frame'ini tkinter'da göstermek için tanımlamaya çalıştığın yer

def main():
    LARGE_FONT= ("Verdana", 12)
    class CepteKoc(tk.Tk):
        def __init__(self, *args, **kwargs):  
            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)

            container.pack(side="top", fill="both", expand = True)

            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            self.frames = {}

            for F in (Giris, HareketSayfasi, Goruntu):

                frame = F(container, self)

                self.frames[F] = frame

                frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(Giris)

        def show_frame(self, cont):

            frame = self.frames[cont]
            frame.tkraise()

    class Giris(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self,parent)
            label = tk.Label(self, text="Giriş Yöntemi Seç", font=LARGE_FONT)
            label.pack(pady=10,padx=10)

            ButtonDosya = Button(self, text = "dosya yükle", fg="Black", bg="Pink", command = DosyaAc)
            ButtonDosya.pack()

            #img_Dosya = ImageTk.PhotoImage(Image.open("galeri.gif"))
            #img_Dosya_label = Label(self, image = img_Dosya)
            #img_Dosya_label.pack(fill= "both", expand= False)
            #resim koyamaya çalıştığın yer ancak resim boş olarak geliyor 

            ButtonKamera = Button(self, text = "Kamera", fg="Black", command = Kamera)
            ButtonKamera.pack()

            button = tk.Button(self, text="Onaylama",command=lambda: controller.show_frame(HareketSayfasi))
            button.pack()
            label = tk.Label(self, text="Uyarı: Kamera her zaman tam karşınızda tüm vücudunuzu görür halde olmalı.", font=LARGE_FONT)
            label.pack(pady=10,padx=10)

    class HareketSayfasi(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="HAREKETLER", font=LARGE_FONT)
            label.pack(pady=10,padx=10)

            button1 = tk.Button(self, text="Yöntem Seçmeye geri dön",command=lambda: controller.show_frame(Giris))
            button1.pack()

            ButtonBiceps = Button(self, text = "BiCepsCurl",fg="black", command = bicepscurl)
            ButtonBiceps.pack()

            ButtonSquat = Button(self, text = "Squat",fg="black", command = squat)
            ButtonSquat.pack()

            ButtonShoulderPress = Button(self, text = "ShoulderPress",fg="black", command = shoulderpress)
            ButtonShoulderPress.pack()

            button = tk.Button(self, text="Onaylama",command=lambda: controller.show_frame(Goruntu))
            button.pack()


            ButtonTest = Button(self, text = "test",fg="black",)
            ButtonTest.pack()

    class Goruntu(tk.Frame):
        def __init__(self, parent, controller,img=None):
            tk.Frame.__init__(self, parent)
             
            self.frame.title(self.appName)
            self.frame.resizable(0,0)
            self.frame['bg']='black'
            self.img=img

            self.vid = img
            self.label = Label(self.frame, text= self.appName, font= 15, bg='blue', fg='white').pack(side= TOP, fill= BOTH)
            self.canvas = Canvas(self.frame, width= self.vid.width, height= self.vid.height, bg='red')
            self.canvas.pack()
            #img show'dan aldığı görüntüyü ekrana yazdırmaya çalıştığın yer
            button1 = tk.Button(self, text="Yöntem Seçmeye geri dön",command=lambda: controller.show_frame(Giris))
            button1.pack()
            button2 = tk.Button(self, text="Hareket Seçmeye geri dön",command=lambda: controller.show_frame(HareketSayfasi))
            button2.pack()

    app = CepteKoc()
    app.mainloop()

if __name__ == "__main__":
    main()
        