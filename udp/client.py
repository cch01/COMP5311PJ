import socket, pickle, struct, cv2

maxLength = 65008
structFormat = "Q"
port = 1234
data = b''
frameSize = None
payloadSize = struct.calcsize(structFormat)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(bytes('get','utf-8'), (socket.gethostname(), port))
while True:
    while len(data) < payloadSize:
        packet = s.recvfrom(maxLength)[0]
        # if len(packet.decode('utf-8')) < maxLength:
        #     print(packet.decode('utf-8'))
        #     frameSize = int(packet.decode('utf-8'))
        if not packet: break
        data += packet
    packedMsgSize = data[:payloadSize]
    msgSize = struct.unpack(structFormat, packedMsgSize)[0]
    data = data[payloadSize:]
    print(packedMsgSize)
    while len(data) < msgSize:
        data += s.recvfrom(maxLength)[0]
    frameData = data[:msgSize]
    data = data[msgSize:]
    frame = pickle.loads(frameData)
    cv2.imshow("Receving video from server", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
s.close()
