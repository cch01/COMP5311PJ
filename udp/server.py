import socket
import cv2
from pprint import pprint
import time
import base64

HOST = 'localhost' #change to destination ip / 'localhost' if not using vm
PORT = 999
VID_240P = '../240p.mp4'
VID_360P = '../360p.mp4'
VID_480P = '../480p.mp4'
VID_720P = '../720p.mp4'
VID_1080P = '../1080p.mp4'
PACKET_SIZE = 65507
FRAME_RATE = 30
# PACKET_DIVIDER = 20

vid = cv2.VideoCapture(VID_480P) #change to VID_XXXXP if want
def splitIn(x):
    return iter(range(x))

frameCounter = 1
prev = 0

while (True):
    time_elapsed = time.time() - prev
    if time_elapsed > 1/FRAME_RATE:
        prev = time.time()
        img, frame = vid.read()
        encoded, buffer = cv2.imencode('.jpg', frame)
        b_frame = base64.b64encode(buffer)
        print(f'frame: {frameCounter}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cv2.imshow('frame sending', frame)
        sock.sendto(bytes(('frameSize'+str(len(b_frame))).encode('utf-8')), (HOST, PORT))
        for i in splitIn(len(b_frame)//PACKET_SIZE + 1 if len(b_frame)%PACKET_SIZE > 0 else 0):
            data, addr = sock.recvfrom(15)
            if data == b'getFrameContent':
                sock.sendto(b_frame[i * PACKET_SIZE: (i + 1) * (PACKET_SIZE) if (len(b_frame) - i * PACKET_SIZE > PACKET_SIZE) else None], (HOST, PORT))

        data, addr = sock.recvfrom(15)
        sock.sendto(b'endFrame', (HOST, PORT))
        frameCounter = frameCounter + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()