import socket, pickle, struct, cv2

structFormat = "Q"
PORT = 1234
HOST = '10.0.2.15' #change to server / 'localhost' if not using vm
data = b''
PAYLOAD_SIZE = struct.calcsize(structFormat)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
frameCounter = 1

while True:
    while len(data) < PAYLOAD_SIZE:
        packet = sock.recv(4*1024)
        if not packet: break
        data += packet
    packedMsgSize = data[:PAYLOAD_SIZE]
    msgSize = struct.unpack(structFormat, packedMsgSize)[0]

    data = data[PAYLOAD_SIZE:]

    while len(data) < msgSize:
        data += sock.recv(4*1024)
    frameData = data[:msgSize]
    data = data[msgSize:]
    frame = pickle.loads(frameData)
    print(f'frame: {frameCounter}')
    cv2.imshow("Receving video from server", frame)
    frameCounter = frameCounter + 1
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

sock.close()
