#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import time
import paho.mqtt.client as paho
from paho import mqtt
import json
from multiprocessing.pool import ThreadPool
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5 import uic
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import QThreadPool
from PySide2.QtCore import QTimer 

receive_json=0
H_value=400
C_value=0
E_value=0
N_value=0
T_value=0
run = True

class Runnable(QRunnable):
    def __init__(self):
        super().__init__()
        self.is_running = True
    def run(self):
        while run:
            client.loop_start()
            print("ok")
            client.loop_stop()
            time.sleep(2)
    def cancel(self):
        run = False    

class MyUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_main3.ui",self)
        self.show()
        self.label_2.setText("ok")
       
    def update_label(self,C_value,T_value,H_value,N_value,E_value):
        print("update:",H_value)
        self.label_2.setNum(C_value)
        self.label_6.setNum(T_value)
        self.label_10.setNum(H_value)
        self.label_N.setNum(N_value)
        self.label_E.setNum(E_value)

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
C_value=0
# print message, useful for checking if it was successful
def on_message(client, userdata, msg):

    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    receive_json = str(msg.payload, 'utf-8')
    print(receive_json)
    receive_json = receive_json.strip()
    try:
        # Phân tích chuỗi JSON
        data = json.loads(receive_json)
        C_value = data.get('C')
        T_value = data.get('T')
        H_value = data.get('H')
        N_value = data.get('N')
        E_value = data.get('E')

        # Sử dụng các giá trị đã lấy
        print("C_value:", C_value)
        print("T_value:", T_value)
        print("H_value:", H_value)
        print("N_value:", N_value)
        print("E_value:", E_value)
        myui.update_label(C_value,T_value,H_value,N_value,E_value)
    except json.decoder.JSONDecodeError:
        print("Chuỗi không phải là JSON hợp lệ.")
   
    
    

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("DATN24", "Hieu123@")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("5f74af7626e84491927a97c093cacdb1.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("iot/66", qos=1)

# a single publish, this can also be done in loops, etc.
client.publish("encyclopedia/temperature", payload="hot", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop





if __name__== "__main__":
    pool = QThreadPool.globalInstance() 
    runnable = Runnable()
    pool.start(runnable)
    app = QApplication([])
    myui = MyUI()
    # Thiết lập QTimer
    timer = QTimer()
    timer.timeout.connect(myui.update_label(C_value,T_value,H_value,N_value,E_value))
    timer.start(2000)  # 2000 milliseconds = 2 seconds
    sys.exit(app.exec_())


    
   
         


   