import socket
import hashlib
import os

# Set address and port
serverAddress = "127.0.0.1"
serverPort = 5555

# Delimiter
delimiter = "|:|:|";
b_delimiter = b'|:|:|'

# Start - Connection initiation
while 1:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(10);
    server_address = (serverAddress, serverPort)
    #data,address = sock.recvfrom(100)
    userInput = input("\nRequested file: ")
    message = userInput;
    seqNoFlag = 0
    f = open("r_test.py", 'wb');

    try:
        # Connection trials
        connection_trials_count=0
        # Send data
        print("Requesting ",message)
        sent = sock.sendto(message.encode(), server_address)
        # Receive indefinitely
        while 1:
            # Receive response
            print("Waiting to receive..")
            try:
                data, server = sock.recvfrom(4096)
                # Reset failed trials on successful transmission
                connection_trials_count=0;
            except:
                connection_trials_count += 1
                if connection_trials_count < 5:
                    print ("Connection time out, retrying")
                    continue
                else:
                    print ("\nMaximum connection trials reached, skipping request\n")
                    os.remove("r_" + userInput)
                    break

            new_data = data.split(b_delimiter)[3]
            data = data.split(b_delimiter)[0] + b_delimiter + data.split(b_delimiter)[1] + b_delimiter + data.split(b_delimiter)[2]
            data = data.decode()
            seqNo = data.split(delimiter)[1]
            clientHash = hashlib.sha1(new_data).hexdigest()
            print ("Server hash: " + data.split(delimiter)[0])
            print ("Client hash: " + clientHash)
            if data.split(delimiter)[0] == clientHash and seqNoFlag == int(seqNo == True):
                packetLength = data.split(delimiter)[2]
                if new_data == "FNF":
                    print ("Requested file could not be found on the server")
                    os.remove("r_" + userInput)
                else:
                    print(new_data,type(new_data))
                    f.write(new_data);
                print ("Sequence number: {}\nLength: {}".format(seqNo, packetLength))
                print ("Server: {} on port {}".format(server ,server))
                sent = sock.sendto((str(seqNo)+ "," + packetLength).encode(), server)
            else:
                print ("Checksum mismatch detected, dropping packet")
                print ("Server: %s on port %s".format(server))
                continue;
            if int(packetLength) < 500:
                seqNo = int(not seqNo)
                break

    finally:
        print ("Closing socket")
        sock.close()
        f.close()
