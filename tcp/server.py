import socket
import cv2, struct
import numpy as np
import pickle

port = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), port))
s.listen(1)
structFormat = "Q"
print("listening at", socket.gethostname(), port)


def start_stream():
    clientSocket, address = s.accept()
    vid = cv2.VideoCapture('../nature-720p.mp4')
    try:
        print(f'client {address} connected')
        if clientSocket:
            while(vid.isOpened()):
                img, frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack(structFormat, len(a)) + a
                clientSocket.send(message)
                cv2.imshow('Transfering', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except Exception as e:
        print(f'{address} disconnected')
        pass

while True: 
    start_stream()

s.close()
    