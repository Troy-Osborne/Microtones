from math import sin,pi,cos
from matplotlib import pyplot as plt
FrameRate=44100

def HarmonicEnv(length,harmonicnumber,decayexponent):
    attacktime=480#frames
    releasetime=int((length/harmonicnumber**decayexponent)*FrameRate-attacktime)
    #convert length into seconds divide by harmonic number and subtract attack
    factor=harmonicnumber**decayexponent
    return [(frame/attacktime)/factor for frame in range(attacktime)]+[(1-frame/releasetime)/factor for frame in range(releasetime)]
    

class Pluck:
    def __init__(self,overtones=64,lengthfunc=lambda length,octave:(4*length)/(octave),envelopes=lambda length,harmonicnumber,decayexponent:HarmonicEnv(length,harmonicnumber,decayexponent),decayexponent=1.5,fundamentalvoices=16,detunecents=8):
        self.overtones=overtones
        self.envelopes=envelopes
        self.lengthfunc=lengthfunc
        self.decayexponent=decayexponent
        self.fundamentalvoices=fundamentalvoices
        self.detunecents=detunecents
    def makepluck(self,notenum,TonesPerOctave=19,Tuning=437.36,cents=0):
        offset=(4*TonesPerOctave+1)
        Freq=Tuning*2**((notenum+cents/100-offset)/TonesPerOctave)
        Octave=(notenum+cents/100-offset)/TonesPerOctave+4
        MainEnv=self.envelopes(self.lengthfunc(1,Octave),1,self.decayexponent)
        out=[MainEnv[i]*sin(i*Freq*pi*2/44100) for i in range(len(MainEnv))]
        for naturalharmony in range(2,32):
            envelope=self.envelopes(self.lengthfunc(1,Octave),naturalharmony,self.decayexponent)
            pos=0
            for i in envelope:
                val=envelope[pos]*sin(pos*naturalharmony*Freq*pi*2/44100)
                out[pos]+=val
                pos+=1
        return out

def display(mylists):
    for mylist in mylists:
        plt.plot(mylist)
    plt.show()

Space=[0]*2000


def savesound(l,name="default.wav"):
    import wave
    from struct import pack
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

def normalize(l,size=2**15-1):
    mag=0
    for i in l:
        val=abs(i)
        if val>mag:
            mag=val
    factor=size/mag
    return [int(i*factor) for i in l]

MyPluck=Pluck()
sounds=[MyPluck.makepluck(i) for i in range(19*2,19*5+1)]
PluckSeries=[]
for i in range(len(sounds)):
    PluckSeries+=normalize(sounds[i])
    PluckSeries+=Space
savesound(PluckSeries,"plucks.wav")
    
