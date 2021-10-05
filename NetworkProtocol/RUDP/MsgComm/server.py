import socket
import threading
import hashlib
import time
import datetime
import random

# PLP Simulation settings
lossSimualation = False

# Set address and port
serverAddress = "127.0.0.1"
serverPort = 5555


# Delimiter
delimiter = "|:|:|";

# Seq number flag
seqFlag = 0

# Packet class definition
class packet():
    checksum = 0;
    length = 0;
    seqNo = 0;
    msg = 0;

    def make(self, data):
        print(data)
#        data = str(data)
        self.msg = data
        self.length = str(len(data))
        self.checksum=hashlib.sha1(data).hexdigest()
        print ("Length: {}\nSequence number: {}".format(self.length, self.seqNo))


# Connection handler
def handleConnection(address, data):
    drop_count=0
    packet_count=0
    time.sleep(0.5)
    if lossSimualation:
        packet_loss_percentage=float(input("Set PLP (0-99)%: "))/100.0
        while packet_loss_percentage<0 or packet_loss_percentage >= 1:
          packet_loss_percentage = float(input("Enter a valid PLP value. Set PLP (0-99)%: "))/100.0
    else:
        packet_loss_percentage = 0
    start_time=time.time()
    print ("Request started at: " + str(datetime.datetime.utcnow()))
    pkt = packet()
    threadSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Read requested file
        try:
            print ("Opening file",data)
            fileRead = open(data, 'rb')
            data = fileRead.read()
            fileRead.close()

        except:
            msg="FNF";
            pkt.make(msg);
            finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter + pkt.msg
            threadSock.sendto(finalPacket, address)
            print ("Requested file could not be found, replied with FNF")
            return

        # Fragment and send file 500 byte by 500 byte
        x = 0
        
        while x < (len(data) / 500) + 1:
            packet_count += 1
            randomised_plp = random.random()
            if packet_loss_percentage < randomised_plp:
                msg = data[x * 500:x * 500 + 500];
                pkt.make(msg);
                finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter# + str(pkt.msg)
                # Send packet
                finalPacket = finalPacket.encode() + pkt.msg
                sent = threadSock.sendto(finalPacket, address)
                print('Sent {} bytes back to {}, awaiting acknowledgment..'.format(sent, address))
                threadSock.settimeout(2)
                try:
                    ack, address = threadSock.recvfrom(100);
                    ack = ack.decode()
                except:
                    print ("Time out reached, resending ...",x);
                    continue;
                if ack.split(",")[0] == str(pkt.seqNo):
                    pkt.seqNo = int(not pkt.seqNo)
                    print ("Acknowledged by: " + ack + "\nAcknowledged at: " + str(
                        datetime.datetime.utcnow()) + "\nElapsed: " + str(time.time() - start_time))
                    x += 1
            else:
                print("\n------------------------------\n\t\tDropped packet\n------------------------------\n")
                drop_count += 1
        print ("Packets served: " + str(packet_count))
        if lossSimualation:
            print("Dropped packets: " + str(drop_count)+"\nComputed drop rate: %.2f" % float(float(drop_count)/float(packet_count)*100.0))
    except:
        print("Internal server error")



# Start - Connection initiation
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (serverAddress, serverPort)
print ('Starting up on {} port {}'.format(server_address[0],server_address[1]))
sock.bind(server_address)

# Listening for requests indefinitely
#address = ('127.0.0.1',5555)
#sock.sendto('ss'.encode(),address)
while True:
    print ('Waiting to receive message')
    data,address = sock.recvfrom(7000)
    connectionThread = threading.Thread(target=handleConnection, args=(address, data))
    connectionThread.start()
    print ('Received {} bytes from {}'.format(len(data), address))
