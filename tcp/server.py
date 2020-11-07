import socket
import cv2, struct
import numpy as np
import pickle

PORT = 1234
STRUCT_FORMAT = "Q"
HOST = '127.0.0.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("listening at", HOST, PORT)


def start_stream():
    clientSocket, address = sock.accept()
    vid = cv2.VideoCapture('../nature-360p.mp4')
    try:
        print(f'client {address} connected')
        if clientSocket:
            frameCounter = 1
            while(vid.isOpened()):
                img, frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack(STRUCT_FORMAT, len(a)) + a
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

vid.release()
sock.close()
cv2.destroyAllWindows()