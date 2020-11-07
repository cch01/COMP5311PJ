import socket
import cv2
from pprint import pprint

HOST = '127.0.0.1'
PORT = 999
VIDEO_SOURCE = '../nature-360p.mp4'
PACKET_SIZE = 65500
# PACKET_DIVIDER = 20

vid = cv2.VideoCapture(VIDEO_SOURCE)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
def splitIn(x):
    return iter(range(x))

frameCounter = 1

while (True):
    ret, frame = vid.read()
    print(f'frame: {frameCounter}')
    cv2.imshow('frame sending', frame)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    flattenedFrame = frame.flatten()
    frameBytes = flattenedFrame.tobytes()
    sock.sendto(bytes(('frameSize'+str(len(frameBytes))).encode('utf-8')), (HOST, PORT))
    for i in splitIn(len(frameBytes)//PACKET_SIZE + 1 if len(frameBytes)%PACKET_SIZE > 0 else 0):
        data, addr = sock.recvfrom(15)
        if data == b'getFrameContent':
            sock.sendto(frameBytes[i * PACKET_SIZE: (i + 1) * (PACKET_SIZE) if (len(frameBytes) - i * PACKET_SIZE > PACKET_SIZE) else None], (HOST, PORT))

    data, addr = sock.recvfrom(15)
    sock.sendto(b'endFrame', (HOST, PORT))
    frameCounter = frameCounter + 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()