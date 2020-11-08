import socket
import cv2, struct
import numpy as np
import pickle

PORT = 1234
STRUCT_FORMAT = "Q"
HOST = 'localhost'#change to client ip
VID_360P = '../360p.mp4'
VID_720P = '../720p.mp4'
VID_1080P = '../1080p.mp4'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("listening at", HOST, PORT)


def start_stream():
    clientSocket, address = sock.accept()
    vid = cv2.VideoCapture(VID_1080P) #can change if you want
    try:
        print(f'client {address} connected')
        if clientSocket:
            frameCounter = 1
            while(vid.isOpened()):
                img, frame = vid.read()
                frameBytes = pickle.dumps(frame)
                message = struct.pack(STRUCT_FORMAT, len(frameBytes)) + frameBytes
                clientSocket.send(message)
                print(f'frame: {frameCounter}')
                cv2.imshow('Transfering', frame)
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