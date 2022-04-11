# main.py 
# import the kivy module 
import kivy  
import random  
# It’s required that the base Class  
# of your App inherits from the App class. 
from kivy.app import App 
from kivy.uix.gridlayout import GridLayout 
from kivy.properties import StringProperty
from kivy.clock import Clock
import time
from kivy.graphics import Color
from kivy.animation import Animation
from datetime import datetime
import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import socketio
import os
import sys
import sched
import multiprocessing
from kivy.core.window import Window
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="telep",
  password="pannon01",
  database="admin_olaj"
)


  
# This class stores the info of .kv file 
# when it is called goes to my.kv file

data="asd"

#!/usr/bin/env python



# standard Python
sio = socketio.Client()

GPIO.setwarnings(False)

@sio.event
def connect_error(message):
  sio.disconnect()
  print('Connection was rejected due to ' + message)
   

    
reader = SimpleMFRC522()
sio.connect('http://localhost:3000/')





s = sched.scheduler(time.time, time.sleep)
def do_something(sc,): 
    print("Doing stuff...")
    sio.emit('Kartyaebrentarto', "Helloka ebren")
    # do your stuff
    s.enter(240, 1, do_something, (sc,))

def f():
    time.sleep(1)
    print ("Adatküldszervernek")
    s.enter(30, 1, do_something, (s,))
    s.run()
    
def defulatSteuper():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT kartyaszam FROM felhasznalok WHERE belepve=1")

    myresult = mycursor.fetchall()
    array=[]
    for x in myresult:
        print(x)
        array.append(x[0])

    print(array)
    for i in array:
        print(i)
    return array


def olvaso():
 while 1:
   try:
       id,text = reader.read()
       print(id)
       print(text)
       sio.emit('Belepteto', {'adat': id})

   except KeyboardInterrupt:
    GPIO.cleanup()
    sio.disconnect()
   finally:
     GPIO.cleanup()
   return str(id)




class MainWidget(GridLayout):
    crudeclock =  StringProperty()
    name =  StringProperty()
    Status= StringProperty()
    kiBe= StringProperty()

    class myThread2(threading.Thread):
        def __init__(self, threadID, name):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            
 
        def run(self):
            print ("Starting " + self.name)
            f()

            print ("Exiting " + self.name)
            

    class myThread(threading.Thread):
        def __init__(self, threadID, name,prev):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.prev=prev
            self.dict={'935869655226':0,'41930105169':0,'1003584332203':0,'385729077513':0,'726662748537':0,'886481144583':0 }
            self.dict2={'935869655226':'Adminisztrátor','41930105169':'Csaba','1003584332203':'Berci','385729077513':'Pistuka','726662748537':'Józsi(Boss)','886481144583':'Ottó' }
        def run(self):
            print ("Starting " + self.name)
            Basicdata = defulatSteuper()
            for data in Basicdata:
                self.dict[data]=1
            print(self.dict)
            while(1):
                x=olvaso()
                if(self.dict.get(x)==0):
                    self.prev.setKiBe("Beléptetve")
                    self.dict[x]=1
                else:
                    self.prev.setKiBe("Kiléptetve")
                    self.dict[x]=0
                
                self.prev.setName(self.dict2.get(x))
                time.sleep(6)
                self.prev.setName("")
                self.prev.setKiBe("")




    

    def __init__(self, **kwargs):
        thread2 = self.myThread2(2, "Thread-2")
        thread1 = self.myThread(1, "Thread-1",self)
        try:
            thread1.daemon=True
            thread2.daemon=True       
            thread2.start()
            thread1.start()

        except (KeyboardInterrupt, SystemExit):
            #thread1.join()
            #thread2.join()
            sio.disconnect()
            GPIO.cleanup()
            sys.exit() 


        Clock.schedule_interval(self.update, 1)
        super(MainWidget, self).__init__(**kwargs)
    

        
    
    def setName(self,data):
        self.name=data

    def setKiBe(self,data):
        self.kiBe=data
        


    def update(self, *args):
        now = datetime.now()
        self.crudeclock = now.strftime("%Y/%m/%d/, %H:%M:%S")





  
# we are defining the Base Class of our Kivy App 
class myApp(App):

    def build(self): 
        # return a MainWidget() as a root widget
        return MainWidget()

    def setName(self,data):
        MainWidget.name=data
  
def indit():
    try:
        Window.size = (1920, 1080)
        myApp().run()
    except (KeyboardInterrupt, SystemExit):
        
        sio.disconnect()
        GPIO.cleanup()
        sys.exit()



indit()
time.sleep(2.4)
sys.exit()
