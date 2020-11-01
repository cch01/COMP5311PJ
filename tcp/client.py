import socket, pickle, struct, cv2

structFormat = "Q"
port = 1234
data = b''
payloadSize = struct.calcsize(structFormat)
print('payloadSize',payloadSize)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), port))
while True:
    while len(data) < payloadSize:
        packet = s.recv(4*1024)
        if not packet: break
        data += packet
    packedMsgSize = data[:payloadSize]
    print(payloadSize)
    msgSize = struct.unpack(structFormat, packedMsgSize)[0]
    print(msgSize)

    data = data[payloadSize:]
    
    while len(data) < msgSize:
        data += s.recv(4*1024)
    frameData = data[:msgSize]
    data = data[msgSize:]
    frame = pickle.loads(frameData)
    cv2.imshow("Receving video from server", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
s.close()
