import socket, struct, cv2, base64, numpy, datetime


structFormat = "<L"
PORT = 1234
HOST = 'localhost' #change to server / 'localhost' if not using vm
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
    packedMsg = data[:PAYLOAD_SIZE]
    msgSize = struct.unpack(structFormat, packedMsg)[0]

    data = data[PAYLOAD_SIZE:]

    while len(data) < msgSize:
        data += sock.recv(4*1024)
    frameData = data[:msgSize]
    data = data[msgSize:]
    img = base64.b64decode(frameData)
    npimg = numpy.fromstring(img, dtype=numpy.uint8)
    frame = cv2.imdecode(npimg, 1)
    print(f'frame: {frameCounter}')
    cv2.imshow("Receving video from server", frame)
    frameCounter = frameCounter + 1
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

sock.close()