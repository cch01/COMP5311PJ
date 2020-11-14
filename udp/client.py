import socket
import numpy
import time
import cv2
from pprint import pprint
import random

HOST = "0.0.0.0"
PORT = 999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
PACKET_SIZE = 65507
PACKET_LOSS_RATE = 0 #10% packet loss

VID_240P = (240, 426, 3)
VID_480P = (480, 854, 3)
VID_720P = (720, 1280, 3)
VID_720P = (720, 1280, 3)
VID_1080P = (1080, 1920, 3)
frameCounter = 0

dataBytes = b''

while True:
    frameSize = None
    data, addr = sock.recvfrom(30) # b'eframe' is 6 byte long
    if 'frameSize' in data.decode('utf-8'):
        frameSize = int(data.decode('utf-8').split('frameSize')[1])
        while True:
            sock.sendto(b'getFrameContent', addr)
            data, addr =  sock.recvfrom(PACKET_SIZE)
            if data == b'endFrame':
                break
            if random.random() > PACKET_LOSS_RATE:
                dataBytes += data
    if len(dataBytes) >= frameSize:
        frame = numpy.fromstring (dataBytes, dtype=numpy.uint8)
        try:
            frame = frame.reshape (VID_720P) #can change if you want
            print(f'frame: {frameCounter}')
            cv2.imshow('frame receiving',frame)
            frameCounter = frameCounter + 1
        except ValueError:
            None
            # print('incomplete frame');
        dataBytes=b''
        
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

sock.close()