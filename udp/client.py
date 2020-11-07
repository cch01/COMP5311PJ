import socket
import numpy
import time
import cv2
from pprint import pprint

HOST = "127.0.0.1"
PORT = 999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
PACKET_SIZE = 65500
frameCounter = 0

dataBytes = b''

while True:
    frameSize = None
    data, addr = sock.recvfrom(30) # b'eframe' is 6 byte long
    if 'frameSize' in data.decode('utf-8'):
        frameSize = int(data.decode('utf-8').split('frameSize')[1])
        while True:
            sock.sendto(b'getFrameContent', addr)
            data, addr = sock.recvfrom(PACKET_SIZE)
            if data == b'endFrame':
                break
            dataBytes += data
    if len(dataBytes) == frameSize:
        frame = numpy.fromstring (dataBytes, dtype=numpy.uint8)
        frame = frame.reshape (360,640, 3)
        print(f'frame: {frameCounter}')
        cv2.imshow('frame receiving',frame)
        frameCounter = frameCounter + 1
        dataBytes=b''
        
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

sock.close()