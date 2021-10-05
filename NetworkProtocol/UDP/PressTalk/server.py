# Echo server program
from pynput import keyboard
from threading import Thread
from threading import Event
import pyaudio
import wave
import socket
import time

start=1
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4
WIDTH = 2

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
       #print(HOST,PORT)
       #self.s.listen(1)
       # create ouput stream
       self.stream,self.p = createOuputStream()
       self.__flag = Event()
       self.__flag.set()       
       self.__running = Event()      
       self.__running.set()
       
    def run(self):
       # listen
       #self.conn, self.addr = self.s.accept()
       #print('Connected by', self.addr)
       # recv data
       while self.__running.isSet():
          self.s.settimeout(None)
#          start get value
          #try:
          #  print("Waiting")
          #  data,addr = self.s.recvfrom(1024)
          #  print("Connected from",addr)
          #except:
          #  break
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
              #  print('*')
                break
          
       # close output stream
       self.stream.stop_stream()
       self.stream.close()
       self.p.terminate()
    def send(self,data):
       # self.s.sendto(data,('192.168.0.2',50008))
        self.s.sendto(data,('127.0.0.1',50008))
    def close(self):
     #   self.conn.close()
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
       i = 0
       while self.__running.isSet():            
            data  = self.stream.read(CHUNK)
            self.frames.append(data)
            connect.send(data)
            i += 1
            print(i)
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
              audio.resume()  #繼續
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
        
        audio.pause() #暫停
        start=1
    if (key == keyboard.KeyCode.from_char('e')):
        keyboard.Listener.stop
        connect.close()
                
        return False



if __name__ == '__main__':
   print('start....')
  # HOST = '192.168.0.3'                 # Symbolic name meaning all available interfaces
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
