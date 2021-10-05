# Echo server program
from pynput import keyboard
from threading import Thread
from threading import Event
import hashlib
import pyaudio
import datetime
import socket
import time


start=1
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4
WIDTH = 2
delimiter = "|:|:|";
seqFlag = 0
ta = 0

class packet():
    checksum = 0;
    length = 0;
    seqNo = 0;
    msg = 0;

    def make(self, data):
        self.msg = data
        self.length = str(len(data))
        self.checksum=hashlib.sha1(data).hexdigest()
        
# create ouput stream   
def createOuputStream():
    
  p = pyaudio.PyAudio()
  stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
  return stream,p

class Connect(Thread):
    def __init__(self, HOST, PORT):
       super(Connect, self).__init__()
       # create socket 
       self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       self.s.bind((HOST, PORT))
       # create ouput stream
       self.stream,self.p = createOuputStream()
       self.__flag = Event()
       self.__flag.set()       
       self.__running = Event()      
       self.__running.set()
       
    def run(self):
       while self.__running.isSet():
          self.s.settimeout(None)
          data= "".encode()
          i=1
          self.s.settimeout(0.2)
          while True:
             try:
                data,addr = self.s.recvfrom(65535)
                if not data:
                   continue
                data+=data
                i=i+1
                print (i)
                
                self.stream.write(data)
             except:
                #print('*')
                break
          
       # close output stream
       self.stream.stop_stream()
       self.stream.close()
       self.p.terminate()
    def timeout(self,time):   
        self.s.settimeout(time)
    def send(self,data):
        b = self.s.sendto(data,('127.0.0.1',50008))
        return b
    def recv(self):
        ack,address = self.s.recvfrom(100)
        return ack,address
    def close(self):
        self.s.close()
        
# create input stream and record
class Record(Thread):
    def __init__(self, *args, **kwargs):
        super(Record, self).__init__(*args, **kwargs)
        p = pyaudio.PyAudio()
        self.stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
        self.frames = []
        self.__flag = Event()
        self.__flag.set()       
        self.__running = Event()      
        self.__running.set()      

    def run(self):
       while self.__running.isSet():
            pkt = packet()
            data  = self.stream.read(CHUNK)
            self.frames.append(data)
            x = 0
            start_time=time.time()
            resend = 0;
            while x < (len(data) / 2048):
                msg = data;
                pkt.make(msg);
                finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter# + str(pkt.msg)
                finalPacket = finalPacket.encode() + pkt.msg
                sent = connect.send(finalPacket)
                print('Sent {} bytes back to {}, awaiting acknowledgment..'.format(sent, "('127.0.0.1',50008)"))
                connect.timeout(0.001)
                try:          
                    ack,address = connect.recv()
                    ack = ack.decode()
                    print("got ack")
                except:
                    print ("Time out reached, resending ...",x);
                    resend += 1;
                    print("Resend:",resend)
                    continue;
                if ack.split(",")[0] == str(pkt.seqNo):
                    pkt.seqNo = int(not pkt.seqNo)
                    print ("Acknowledged by: " + ack + "\nAcknowledged at: " + str(
                        datetime.datetime.utcnow()) + "\nElapsed: " + str(time.time() - start_time))
                    x += 1
                    print("x = ",x)
            self.__flag.wait()
        
    def pause(self):
        self.__flag.clear()     
        
    def resume(self):
        self.__flag.set()    
    def stop(self):
        self.__flag.set()       
        self.__running.clear()
# key press
def on_press(key):
    global start
    if (key == keyboard.KeyCode.from_char('s')): 
      if start==1:
            
            print('- Started recording -'.format(key))  
            start=0
            try:
              audio.start()   
            except:
              audio.resume()  #ç¹¼ç?
      else:
        print('.')
        
    else:
        print('incorrect character {0}, press s'.format(key))

# key release
def on_release(key):
    global start
    print('{0} released'.format(key))
    
    if (key == keyboard.KeyCode.from_char('s')):
        print('{0} stop'.format(key))
        
        audio.pause() 
        start=1
    if (key == keyboard.KeyCode.from_char('e')):
        keyboard.Listener.stop
        connect.close()
                
        return False



if __name__ == '__main__':
   print('start....')
   HOST = '127.0.0.1'
   PORT = 50009
   # New Record Tread 
   audio = Record()
   # New Connect Thread and listens
   connect = Connect(HOST,PORT)
   connect.start()
   print('server ready and listening')
   with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
       listener.join()
