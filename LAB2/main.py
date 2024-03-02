from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import time
import threading
#import my module

from mqtt import MyMQTTClient
from uart import UARTCommunication
from AI_camera import AI_CAM

AIO_USERNAME = "GutD"
AIO_KEY = "aio_JskM93fdBC86QY0MvHnIugwvbHCh"
AIO_FEED_ID = ["pump", "fan", "temperature", "humidity", "lux","mask"]


mqtt_client = MyMQTTClient(AIO_USERNAME, AIO_KEY, AIO_FEED_ID)
uart = UARTCommunication(baudrate=115200, timeout=1)
camera = AI_CAM("model/keras_model.h5", "model/labels.txt", camera_index=0)

def myProcessData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[0] == "TEMP":
        mqtt_client.publish_data("temperature",splitData[1])
    elif splitData[0] == "LUX":
        mqtt_client.publish_data("lux",splitData[1])
    elif splitData[0] == "HUMI":
        mqtt_client.publish_data("humidity",splitData[1])
    else:
        print("we dont have that measurement to publish")
    

def main():
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # serial init
    uart.processData = myProcessData
    
    #mqtt init
    mqtt_client.start()
    count_ai = 0
    camera.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    while True:
        uart.read_serial()
        
        ret, image = camera.camera.read()
        cv2.imshow("Webcam Image", image)
        if count_ai > 5:
            count_ai = 0

            preprocessed_image = camera.preprocess_image(image)
            class_name, confidence_score = camera.predict_image(preprocessed_image)

            print("Class:", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            mqtt_client.publish_data("mask",class_name[2:])
        else: 
            count_ai += 1

        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)
        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break

        time.sleep(1)
    
if __name__ == "__main__":
    main()


