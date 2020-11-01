import socket
import cv2, struct
import numpy as np
import pickle



port = 1234
maxLength = 65000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((socket.gethostname(), port))
structFormat = "Q"
print("listening at", socket.gethostname(), port)


def start_stream():
    vid = cv2.VideoCapture('../nature-360p.mp4')
    while(vid.isOpened()):
        img, frame = vid.read()
        cv2.imshow('Transfering', frame)
        a = pickle.dumps(frame)
        print(len(a))
        while len(a) > 0:
            # s.sendto(bytes(str(len(a)), 'utf-8'), address)
            buffer = struct.pack(structFormat, maxLength) + a[:maxLength]
            a = a[maxLength:]
            print(len(buffer))
            # if len(buffer) > 65535:
            #     print("The message is too large to be sent within a single UDP datagram. We do not handle splitting the message in multiple datagrams")
            #     s.sendto("FAIL".encode('utf-8'),address)
            #     continue
            # We send back the buffer to the client
            
            s.sendto(buffer, address)



incomeData, address = s.recvfrom(4)
incomeData = incomeData.decode('utf-8')
print("income data", incomeData)
print(incomeData == "get")
if incomeData == "get":
    while True: 
        try:
            start_stream()
        except Exception as e:
            print(f'{address} disconnected')
            pass

s.close()
    


