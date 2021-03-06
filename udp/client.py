import socket, numpy, time, cv2, random, base64

HOST = "0.0.0.0"
PORT = 999
PACKET_SIZE = 65507
PACKET_LOSS_RATE = 0.1 #10% packet loss

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

frameCounter = 0

dataBytes = b''

while True:
    frameSize = None
    data, addr = sock.recvfrom(30) # b'eframe' is 6 byte long
    if 'frameSize' in data.decode('utf-8'):
        frameSize = int(data.decode('utf-8').split('frameSize')[1])
        while True:
            sock.sendto(b'getFrameContent', addr)
            data, addr =  sock.recvfrom(PACKET_SIZE)
            if data == b'endFrame':
                break
            if random.random() > PACKET_LOSS_RATE:
                dataBytes += data
    if len(dataBytes) >= frameSize:
        try:
            img = base64.b64decode(dataBytes)
            frame = numpy.fromstring (img, dtype=numpy.uint8)
            frame = cv2.imdecode(frame, 1)
            print(f'frame: {frameCounter}')
            cv2.imshow('frame receiving',frame)
            frameCounter = frameCounter + 1
        except:
            None
        dataBytes=b''
        
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

sock.close()