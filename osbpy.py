from random import randint
import os
import pylab as plt
import math
import numpy as np
from scipy.io import wavfile

layers = ["Background","Fail","Pass","Foreground"]
origins = ["TopLeft","TopCentre","TopRight","CentreLeft","Centre","CentreRight","BottomLeft","BottomCentre","BottomRight"]
spect = []

def sinus(har, radius, sinheight):
    x1 = np.linspace(0, sinheight, har)
    y1 = np.sin(x1)
    sinus = plt.plot(x1, y1, 'bo')
    ysinus = sinus[0].get_ydata()*radius
    return ysinus

def gencircle(r, n):
    for i in range(len(r)):
        for j in range(n[i]):
            yield r[i], j*(2 * np.pi / n[i])

def circle(har, radius):
    circle = []
    xcircle = {}
    ycircle = {}
    for r, t in gencircle([2*radius], [har]):
        circle += plt.plot(r * np.cos(t), r * np.sin(t), 'bo')
    for index, val in enumerate(circle):
        xcircle[index] = val.get_xdata()
        ycircle[index] = val.get_ydata()
    return ycircle, xcircle

def check_easing(es):
    if es not in range(35):
        return True
    else:
        return False

class osbject:
    obj = []
    def __init__(self, path, layer, origin, posX, posY, framecount=None, framerate=None, loop=None):
        osbject.obj.append(self)
        valid = True
        errors = ""
        if type(path) is not str:
            errors += "Invalid Path! "
            valid = False
        if layer not in layers:
            errors += "Invalid Layer! "
            valid = False
        if origin not in origins:
            errors += "Invalid Origin! "
            valid = False
        if not isinstance(posX, int) or not isinstance(posY, int):
            errors += "Invalid Position! "
            valid = False
        if framecount is not None and framerate is not None and loop is not None:
            if not isinstance(framecount, int) or not isinstance(framerate, int):
                errors += "Invalid Frame count or Frame rate! "
                valid = False
            if loop not in ["LoopForever","LoopOnce"]:
                errors += "Invalid Type! "
                valid = False
            if valid:
                self.props = "Animation,%s,%s,%s,%s,%s,%s,%s,%s" % (layer, origin, path, posX, posY, framecount, framerate, loop)
            else:
                self.props = errors
        else:
            if valid:
                self.props = "Sprite,%s,%s,%s,%s,%s" % (layer, origin, path, posX, posY)
            else:
                self.props = errors

    def fade(self, easing,startTime,endTime,startFade,endFade,loop = False):
        valid = True
        errors = ""
        if check_easing(easing):
            errors += "Invalid Easing! "
            valid = False
        if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
            errors += "Invalid Time! "
            valid = False
        if not (isinstance(startFade, int) or isinstance(startFade, float)) or not (isinstance(endFade, int) or isinstance(endFade, float)):
            errors += "Invalid Fade! "
            valid = False
        if valid:
            if loop:
                self.props += "\n  F,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startFade, endFade)
            else:
                self.props += "\n F,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startFade, endFade)
        else:
            self.props += "\n" + errors

    def move(self, easing,startTime,endTime,startmoveX,startmoveY,endmoveX,endmoveY,loop = False):
        valid = True
        errors = ""
        if check_easing(easing):
            errors += "Invalid Easing! "
            valid = False
        if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
            errors += "Invalid Time! "
            valid = False
        if not isinstance(startmoveX, int) or not isinstance(startmoveY, int) or not isinstance(endmoveX, int) or not isinstance(endmoveY, int):
            errors += "Invalid Move! "
            valid = False
        if valid:
            if loop:
                self.props += "\n  M,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, startmoveY, endmoveX, endmoveY)
            else:
                self.props += "\n M,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, startmoveY, endmoveX, endmoveY)
        else:
            self.props += "\n" + errors

    def moveX(self, easing,startTime,endTime,startmoveX,endmoveX,loop = False):
        valid = True
        errors = ""
        if check_easing(easing):
            errors += "Invalid Easing! "
            valid = False
        if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
            errors += "Invalid Time! "
            valid = False
        if not isinstance(startmoveX, int) or not isinstance(endmoveX, int):
            errors += "Invalid Move! "
            valid = False
        if valid:
            if loop:
                self.props += "\n  MX,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, endmoveX)
            else:
                self.props += "\n MX,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, endmoveX)
        else:
            self.props += "\n" + errors

    def moveY(self, easing,startTime,endTime,startmoveY,endmoveY,loop = False):
        valid = True
        errors = ""
        if check_easing(easing):
            errors += "Invalid Easing! "
            valid = False
        if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
            errors += "Invalid Time! "
            valid = False
        if not isinstance(startmoveY, int) or not isinstance(endmoveY, int):
            errors += "Invalid Move! "
            valid = False
        if valid:
            if loop:
                self.props += "\n  MY,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveY, endmoveY)
            else:
                self.props += "\n MY,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveY, endmoveY)
        else:
            self.props += "\n" + errors

    def scale(self, easing,startTime,endTime,startScale,endScale,loop = False):
        valid = True
        errors = ""
        if check_easing(easing):
            errors += "Invalid Easing! "
            valid = False
        if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
            errors += "Invalid Time! "
            valid = False
        if not (isinstance(startScale, int) or isinstance(startScale, float)) or not (isinstance(endScale, int) or isinstance(endScale, float)):
            errors += "Invalid Scale! "
            valid = False
        if valid:
            if loop:
                self.props += "\n  S,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startScale, endScale)
            else:
                self.props += "\n S,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startScale, endScale)
        else:
            self.props += "\n" + errors

    def vecscale(self, easing,startTime,endTime,startscaleX,startscaleY,endscaleX,endscaleY,loop = False):
        valid = True
        errors = ""
        if check_easing(easing):
            errors += "Invalid Easing! "
            valid = False
        if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
            errors += "Invalid Time! "
            valid = False
        if not (isinstance(startscaleX, int) or isinstance(startscaleX, float)) or not (isinstance(endscaleX, int) or isinstance(endscaleX, float)) or not (isinstance(startscaleY, int) or isinstance(startscaleY, float)) or not (isinstance(endscaleY, int) or isinstance(endscaleY, float)):
            errors += "Invalid Scale! "
            valid = False
        if valid:
            if loop:
                self.props += "\n  V,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startscaleX, startscaleY, endscaleX, endscaleY)
            else:
                self.props += "\n V,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startscaleX, startscaleY, endscaleX, endscaleY)
        else:
            self.props += "\n" + errors

    def rotate(self, easing,startTime,endTime,startRotate,endRotate,loop = False):
        valid = True
        errors = ""
        if check_easing(easing):
            errors += "Invalid Easing! "
            valid = False
        if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
            errors += "Invalid Time! "
            valid = False
        if not (isinstance(startRotate, int) or isinstance(startRotate, float)) or not (isinstance(endRotate, int) or isinstance(endRotate, float)):
            errors += "Invalid Rotate! "
            valid = False
        if valid:
            if loop:
                self.props += "\n  R,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startRotate, endRotate)
            else:
                self.props += "\n R,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startRotate, endRotate)
        else:
            self.props += "\n" + errors

    def color(self, easing,startTime,endTime,startR,startG,startB,endR,endG,endB,loop = False):
        valid = True
        errors = ""
        if check_easing(easing):
            errors += "Invalid Easing! "
            valid = False
        if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
            errors += "Invalid Time! "
            valid = False
        if not isinstance(startR, int) or not isinstance(startG, int) or not isinstance(startB, int) or not isinstance(endR, int) or not isinstance(endG, int) or not isinstance(endB, int):
            errors += "Invalid Move! "
            valid = False
        if valid:
            if loop:
                self.props += "\n  C,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startR, startG, startB, endR, endG, endB)
            else:
                self.props += "\n C,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startR, startG, startB, endR, endG, endB)
        else:
            self.props += "\n" + errors

    def para(self, easing,startTime,endTime,parameter):
        valid = True
        errors = ""
        if check_easing(easing):
            errors += "Invalid Easing! "
            valid = False
        if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
            errors += "Invalid Time! "
            valid = False
        if parameter not in ["H", "V", "A"]:
            errors += "Invalid Parameter!"
            valid = False
        if valid:
            self.props += "\n P,%s,%s,%s,%s" % (easing, startTime, endTime, parameter)
        else:
            self.props += "\n" + errors

    def loop(self, startTime,loopCount):
        valid = True
        errors = ""
        if not isinstance(startTime, int) or not isinstance(loopCount, int):
            errors += "Invalid Time or Loop count! "
            valid = False
        if valid:
            self.props += "\n L,%s,%s" % (startTime, loopCount)
        else:
            self.props += "\n" + errors

    def trigger(self, trigger, startTime,loopCount):
        valid = True
        errors = ""
        if type(trigger) is not str:
            errors += "Invalid Trigger!"
            valid = False
        if not isinstance(startTime, int) or not isinstance(loopCount, int):
            errors += "Invalid Time or Loop count! "
            valid = False
        if valid:
            self.props += "\n T,%s,%s,%s" % (trigger,startTime, loopCount)
        else:
            self.props += "\n" + errors

    @classmethod
    def end(cl,osbfile):
        if os.path.isfile(osbfile):
            os.remove(osbfile)
        with open(osbfile, "a") as text:
            for val in cl.obj:
                text.write("%s\n" % val.props)

def spectrum(wav_file,mi,mx,har,start,end,posX,posY,layer,origin,gap=0,arrange="",radius=30,sinheight=6.1):
    frame_rate, snd = wavfile.read(wav_file)
    sound_info = snd[:,0]
    spectrum, freqs, t, im = plt.specgram(sound_info,NFFT=1024,Fs=frame_rate,noverlap=5,mode='magnitude')
    n = 0
    rotation = 6.2831
    sinpos = {}
    cirpos = {}
    if arrange is "sinus":
        sinpos = sinus(har,radius,sinheight)
        for i in range(har):
            cirpos[i] = 0
    elif arrange is "circle":
        gap = 0
        sinpos, cirpos = circle(har,radius)
        rotation /= har
    else:
        for i in range(har):
            sinpos[i] = 0
        for i in range(har):
            cirpos[i] = 0
    maximum = plt.amax(spectrum)
    minimum = plt.amin(spectrum)
    position = 0
    while n < har:
        lastval = ((spectrum[n][0]-minimum)/(maximum - minimum))*(mx-mi)+mi
        lastval = math.ceil(lastval*1000)/1000
        lasttime = int(round(t[0]*1000))
        spect.append(osbject("bar.png",layer,origin,posX+position*gap+int(round(float(cirpos[n]))),posY+int(round(float(sinpos[n])))))
        position += 1
        if arrange is "circle":
            spect[n].rotate(0,start,start,math.ceil((1.5707+n*rotation)*1000)/1000,math.ceil((1.5707+n*rotation)*1000)/1000)
        for index,power in enumerate(spectrum[n]):
            power = ((power-minimum)/(maximum - minimum))*(mx-mi)+mi
            power = math.ceil(power*1000)/1000
            if power == lastval or int(round(t[index]*1000)) < start or int(round(t[index]*1000)) > end or index % 2 is not 0:
                lasttime = int(round(t[index]*1000))
                continue
            else:
                spect[n].vecscale(0,lasttime,int(round(t[index]*1000)),1,lastval,1,power)
                lastval = power
                lasttime = int(round(t[index]*1000))
        n += 1
