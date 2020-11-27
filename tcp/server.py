import socket
import cv2, struct
import numpy as np
import time
import base64

PORT = 1234
STRUCT_FORMAT = "<L"
HOST = 'localhost' #change to self ip
VID_240P = '../240p.mp4'
VID_360P = '../360p.mp4'
VID_480P = '../480p.mp4'
VID_720P = '../720p.mp4'
VID_1080P = '../1080p.mp4'
FRAME_RATE = 30


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("listening at", HOST, PORT)



def start_stream():
    clientSocket, address = sock.accept()
    vid = cv2.VideoCapture(VID_720P) #can change if you want
    try:
        print(f'client {address} connected')
        if clientSocket:
            prev = 0
            frameCounter = 1
            while(vid.isOpened()):
                time_elapsed = time.time() - prev
                if time_elapsed > 1/FRAME_RATE:
                    prev = time.time()
                    img, frame = vid.read()
                    encoded, buffer = cv2.imencode('.jpg', frame)
                    b_frame = base64.b64encode(buffer)
                    message = struct.pack(STRUCT_FORMAT, len(b_frame)) + b_frame
                    clientSocket.sendall(message)
                    print(f'frame: {frameCounter}')
                    cv2.imshow('frame sending', frame)
                    frameCounter = frameCounter + 1
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
    except Exception as e:
        print(f'{address} disconnected')
        pass

while True: 
    start_stream()

sock.close()
cv2.destroyAllWindows()