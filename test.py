import sys
import time
from Adafruit_IO import MQTTClient
import random

AIO_FEED_ID = ["pump","fan","temperature","humidity","lux"]
AIO_USERNAME = "GutD"
AIO_KEY = "aio_LZPY13RBOSG7OjfScdYdWCcQgctP"

def connected(client):
    print("Ket noi thanh cong ...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + feed_id + ":" + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    temp = random.randrange(1,100)
    client.publish("temperature",temp)    
    time.sleep(20)
    pass