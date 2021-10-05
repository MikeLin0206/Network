
from pynput import keyboard
from threading import Thread
from threading import Event
import pyaudio
import ssl
import socket
import time
#import dtls
#do_patch()

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

class Record(Thread):
    def __init__(self, *args, **kwargs):
        super(Record, self).__init__(*args, **kwargs)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
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
            data  = self.stream.read(CHUNK)
            self.frames.append(data)
            connect.send(data)
            self.__flag.wait()
            
    def pause(self):
        self.__flag.clear()     
        
    def resume(self):
        self.__flag.set()    

    def stop(self):
        self.__flag.set()       
        self.__running.clear()
        
class Connect(Thread):
   def __init__(self, HOST, PORT):
      super(Connect, self).__init__()
      self.sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.sc.bind((HOST, PORT))
      self.stream,self.p = createOuputStream()

      self.__flag = Event()
      self.__flag.set()       
      self.__running = Event()      
      self.__running.set()
      
   def run(self):
      while self.__running.isSet():
         self.sc.settimeout(None)
         data=0
         i=1
         self.sc.settimeout(0.2)
         while True:
            try:
               data,addr = self.sc.recvfrom(2048)
               if i == 1:
                   ta = time.time()
               if i == 512 :
                   print("total time:",time.time() - ta)
               if not data:
                  continue
               #data+=data
               i=i+1
               print (i)
               #print(type(data))
               self.stream.write(data)
               
            except:
               print('*')
               break


      self.stream.stop_stream()
      self.stream.close()
      self.p.terminate()
   def send(self,data):
        self.sc.sendto(data,('127.0.0.1',50009))
   def close(self):
        self.sc.close()
def on_press(key):
    global start
    if (key == keyboard.KeyCode.from_char('c')): 
      if start==1:
            print('- Started recording -'.format(key))
            # New Tread        
            start=0
            print('connect')
            
            try:
              audio.start()
            except:
              audio.resume()  
 
      else:
        print('.')
        
    else:
        print('incorrect character {0}, press s'.format(key))


def on_release(key):
    global start
    print('{0} released'.format(key))
    
    if (key == keyboard.KeyCode.from_char('c')):
        print('{0} stop'.format(key))
        audio.pause()
        start=1
    if (key == keyboard.KeyCode.from_char('e')):
        keyboard.Listener.stop
        connect.close()
        return False
    


if __name__ == '__main__':
   print('Start connecting to server....') 
   HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
   PORT = 50008
   audio = Record()
   # New Connect Thread and listens
   connect = Connect(HOST,PORT)
   connect.start()
   
   with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
       listener.join()
       
   """listener = keyboard.Listener(on_press=on_press, on_release=on_release)
   listener.start()"""
   
