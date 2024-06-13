###Relevant parts taken from a larger project.
###This is what was used to generate the original 3, 19TET/19EDO Wave Files.

import wave
from struct import pack
from math import sin,pi
class FunctionList:
    def __init__(self,dictionary={}):
        for key in dictionary:
            setattr(self,key,dictionary[key])

######## Equal Temperament Definitions
TwelveTone=FunctionList({"NoteToFrequency":lambda notenum,cents=0,middleA=440:middleA*2**((notenum+cents/100-49)/12),
                         "Notes":{}})

####Define 96 Notes By Name
for i in range(96):
    Letter=["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"][i%12]
    Octave=(1 if i%12 >=3 else 0)
    Octave+=int(i/12)
    name=Letter+str(Octave)
    TwelveTone.Notes[name]=TwelveTone.NoteToFrequency(i+1)
    if Letter[-1]=="#":
       name2="%s%s"%(["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"][(i+1)%12],"b")
       name2+=str(int((i+1)/12)+(1 if i%12 >=3 else 0))
       TwelveTone.Notes[name2]=TwelveTone.NoteToFrequency(i+1)

NineteenTone=FunctionList({"NoteToFrequency":lambda notenum,cents=0,middleA=437.36:middleA*2**((notenum+cents/100-77)/19)})###tuned to ensure they share almost the same G

EqualTemperament=FunctionList({"TwelveTone":TwelveTone,"NineteenTone":NineteenTone})

def saw(x):
    return (x/pi-1)%2-1
    
def blip(freq,length,mag=(2**15-1)):
    func=lambda x:min(1,max(0,(1/(2*x+1))-x/3))
    return [int(sin(n*freq*pi/44100)*func(n/(length*44100))*mag) for n in range(int(length*44100))]

def blip2(freq,length,mag=(2**15-1)):
    func=lambda x:min(1,max(0,(1/(2*x+1))-x/3))
    return [int((sin(n*freq*pi/44100)*3+sin(n*2*freq*pi/44100)*2+sin(n*3*freq*pi/44100)+sin(n*4*freq*pi/44100))*func(n/(length*44100))*mag/7) for n in range(int(length*44100))]

def blip3(freq,length,mag=(2**15-1)):
    func=lambda x:min(1,max(0,(1/(2*x+1))-x/3))
    return [int(saw(n*freq*pi/44100)*func(n/(length*44100))*mag) for n in range(int(length*44100))]

Space=[0]*2000

def savesound(l,name="default.wav"):
    #f=wave.open("blues _ 3rd.wav","w")
    f=wave.open(name,"w")
    f.setframerate(44100)
    f.setnchannels(2)
    f.setsampwidth(2)
    for val in l:
        val=-32768 if val<-32768  else val
        val=32767 if val>32767  else val
        f.writeframes(pack("h",val))
        f.writeframes(pack("h",val))
    return f


#### Make Sine
out=[]
for Note in range(19*3,19*6+1):
    freq=NineteenTone.NoteToFrequency(Note)
    out+=blip(freq,0.25)
    out+=Space
savesound(out,"19tone_Sin.wav")

#### Make Sine OT
out=[]
for Note in range(19*3,19*6+1):
    freq=NineteenTone.NoteToFrequency(Note)
    out+=blip2(freq,0.25)
    out+=Space
savesound(out,"19tone_Sin_OverTones.wav")

#### Make Saw
out=[]
for Note in range(19*2,19*5+1):
    freq=NineteenTone.NoteToFrequency(Note)
    out+=blip3(freq,0.25)
    out+=Space
savesound(out,"19tone_Saw_OverTones.wav")
