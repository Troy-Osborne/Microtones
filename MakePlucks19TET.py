from math import sin,pi,cos,log
from matplotlib import pyplot as plt
from random import random
FrameRate=44100

def HarmonicEnv(length,harmonicnumber,lengthdecay,volumedecay):
    attacktime=480#frames
    releasetime=min(int(length*FrameRate-attacktime),int((length/lengthdecay**(harmonicnumber-1))*FrameRate-attacktime))
    #convert length into seconds divide by harmonic number and subtract attack
    factor=volumedecay**(harmonicnumber-1)
    return [(frame/attacktime)/factor for frame in range(attacktime)]+[(1-frame/releasetime)/factor for frame in range(releasetime)]

class Pluck:
    def __init__(self,fundamentalwave=sin,overtones=64,lengthfunc=lambda length,octave:(4*length)/(octave+4),envelopes=lambda length,harmonicnumber,lengthdecay,volumedecay:HarmonicEnv(length,harmonicnumber,lengthdecay,volumedecay),lengthdecay=2,volumedecay=1.6,overtonecount=8,fundamentalvoices=16,detunecents=8):
        self.overtones=overtones
        self.envelopes=envelopes
        self.lengthfunc=lengthfunc
        self.lengthdecay=lengthdecay
        self.volumedecay=volumedecay
        self.fundamentalvoices=fundamentalvoices
        self.detunecents=detunecents
        self.overtonecount=overtonecount
        self.fundamentalwave=fundamentalwave
    def makepluck(self,notenum,TonesPerOctave=19,Tuning=437.36,cents=0):
        offset=(4*TonesPerOctave+1)
        Freq=Tuning*2**((notenum+cents/100-offset)/TonesPerOctave)
        Octave=(notenum+cents/100-offset)/TonesPerOctave
        MainEnv=self.envelopes(self.lengthfunc(1,Octave),1,self.lengthdecay,self.volumedecay)
        out=[MainEnv[i]*self.fundamentalwave(i*Freq*pi*2/44100)/self.fundamentalvoices for i in range(len(MainEnv))]#Add Primary Fundemental completely in tune
        for voice in range(1,self.fundamentalvoices): ## add additiona fundemental voices with random detuning within parameters
            detunecents=self.detunecents*(1-random()*2)#how many cents will be detuned
            VoiceFreq=2**(log(Freq/Tuning,2)+(detunecents/1200))*Tuning #turn the frequency into an octave number and apply the detune then turn back to a frequency
            for i in range(len(MainEnv)):
                out[i]=MainEnv[i]*self.fundamentalwave(i*VoiceFreq*pi*2/44100)/self.fundamentalvoices #write in the desired wave in the detuned frequency
        for naturalharmony in range(2,self.overtonecount+1):#add the desired natural harmonics starting at 2 since the first harmonic is the fundamental
                                                            #add 1 to the end of the range, since the natural harmonics start at 1 whereas python is 0-indexed
            envelope=self.envelopes(self.lengthfunc(1,Octave),naturalharmony,self.lengthdecay,self.volumedecay)
            pos=0
            for i in envelope:
                val=envelope[pos]*self.fundamentalwave(pos*naturalharmony*Freq*pi*2/44100)
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

def InstrumentToNotes(Generator,outname,Start=38,End=96):
    sounds=[Generator(i) for i in range(Start,End)]
    PluckSeries=[]
    for i in range(len(sounds)):
        PluckSeries+=normalize(sounds[i])
        PluckSeries+=Space
    savesound(PluckSeries,outname)

#Test Pluck
#MyPluck=Pluck(lengthdecay=1.8,volumedecay=2.5,overtonecount=32,detunecents=20,fundamentalvoices=16,lengthfunc=lambda length,octave:(6*length)/(octave+6))
#InstrumentToNotes(MyPluck.makepluck,"LDecay1.8 VDecay2.5 32Overtones 16voices detune20.wav")

#Bass Pluck
#BassPluck=Pluck(lengthdecay=1.4,volumedecay=3,overtonecount=8,fundamentalvoices=1)
#InstrumentToNotes(BassPluck.makepluck,"NewBassPlucks.wav",Start=19,End=77)
