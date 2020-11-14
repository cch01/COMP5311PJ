import socket
import numpy
import time
import cv2
from pprint import pprint
import random
import base64

HOST = "0.0.0.0"
PORT = 999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
PACKET_SIZE = 65507
PACKET_LOSS_RATE = 0 #10% packet loss

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
        img = base64.b64decode(dataBytes)
        frame = numpy.fromstring (img, dtype=numpy.uint8)
        try:
            frame = cv2.imdecode(frame, 1)
            print(f'frame: {frameCounter}')
            cv2.imshow('Receving video from server',frame)
            frameCounter = frameCounter + 1
        except ValueError:
            None
            # print('incomplete frame');
        dataBytes=b''
        
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

sock.close()