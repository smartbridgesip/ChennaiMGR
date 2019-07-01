import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.cleanup()
import datetime
import time
import cv2
import pyrebase
import uuid
import requests

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
p = GPIO.PWM(13, 50)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
p.start(0)
#cv2.namedWindow("test")
# to use Raspberry Pi board pin numbers

def stream_handler(message):
    d=(message["data"])
    #print(d)
    #f=int(d)
    #p.start(7.5)
    #time.sleep(1)
    if (d=="0"):
        p.ChangeDutyCycle(12.5)  # turn towards 0 degree
        #time.sleep(1)
        #print("motor is on")
    elif (d=="1"):
        p.ChangeDutyCycle(2.5) # turn towards 180 degree
        #time.sleep(1)
        #print("motor is off")

config = {
  "apiKey": "AIzaSyB_UDoyW0hbHAA4QLklyXnEjbt9ti8F1As ",
  "authDomain": "intelligentdoor-17ab0.firebaseapp.com",
  "databaseURL": "https://intelligentdoor-17ab0.firebaseio.com/",
  "storageBucket": "intelligentdoor-17ab0.appspot.com"
}
firebase = pyrebase.initialize_app(config)
storage=firebase.storage()
db = firebase.database()



 
while True:
    input_state =GPIO.input(12)
    if(input_state==0):
        cam = cv2.VideoCapture(0)
        #p.start(7.5)
        print("Somebody is at the door!")
        requests.get("https://api.msg91.com/api/sendhttp.php?mobiles=8189901155&authkey=279707Aiw2753w5cf74ea1&route=4&sender=TESTIN&message=Someone is at the door!&country=91")
        ret, frame = cam.read()
        currentDT = datetime.datetime.now()
        #print(str(currentDT))
        #cv2.imshow("test", frame)
        if not ret:
            break
        img_name = str(currentDT)+".png"
        cv2.imwrite(img_name, frame)
        #print("{} written!".format(img_name))
        cam.release()
        storage.child("Images").child(img_name).put(img_name)
        url=storage.child("Images").child(img_name).get_url(img_name)
        #print(url)
        data = {"url": url}
        db.set(data)
        #print("The image is uploaded")
        my_stream = db.child("command").stream(stream_handler)
        #cv2.destroyAllWindows()
        
        
    

