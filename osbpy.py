from random import randint
import os
import pylab as plt
import math
import numpy as np
from scipy.io import wavfile

obj = {}
layers = ["Background","Fail","Pass","Foreground"]
origins = ["TopLeft","TopCentre","TopRight","CentreLeft","Centre","CentreRight","BottomLeft","BottomCentre","BottomRight"]

def stat(path,layer,origin,posX,posY):
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
    if valid:
        return "Sprite,%s,%s,%s,%s,%s" % (layer, origin, path, posX, posY)
    else:
        return errors

def anim(path,layer,origin,posX,posY,framecount,framerate,loop):
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
        if not isinstance(framecount, int) or not isinstance(framerate, int):
            errors += "Invalid Frame count or Frame rate! "
            valid = False
        if loop not in ["LoopForever","LoopOnce"]:
            errors += "Invalid Type! "
            valid = False    
        if valid:
            return "Animation,%s,%s,%s,%s,%s,%s,%s,%s" % (layer, origin, path, posX, posY, framecount, framerate, loop)
        else: 
            return errors

def fade(easing,startTime,endTime,startFade,endFade,loop = False):
    valid = True
    errors = ""
    if easing not in range(35):
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
            return "\n  F,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startFade, endFade)
        return "\n F,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startFade, endFade)
    else:
        return "\n" + errors

def move(easing,startTime,endTime,startmoveX,startmoveY,endmoveX,endmoveY,loop = False):
    valid = True
    errors = ""
    if easing not in range(35):
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
            return "\n  M,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, startmoveY, endmoveX, endmoveY)    
        return "\n M,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, startmoveY, endmoveX, endmoveY)
    else:
        return "\n" + errors

def moveX(easing,startTime,endTime,startmoveX,endmoveX,loop = False):
    valid = True
    errors = ""
    if easing not in range(35):
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
            return "\n  MX,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, endmoveX)
        return "\n MX,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, endmoveX)
    else:
        return "\n" + errors

def moveY(easing,startTime,endTime,startmoveY,endmoveY,loop = False):
    valid = True
    errors = ""
    if easing not in range(35):
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
            return "\n  MY,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveY, endmoveY)
        return "\n MY,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveY, endmoveY)
    else:
        return "\n" + errors

def scale(easing,startTime,endTime,startScale,endScale,loop = False):
    valid = True
    errors = ""
    if easing not in range(35):
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
            return "\n  S,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startScale, endScale)
        return "\n S,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startScale, endScale)
    else:
        return "\n" + errors

def vecscale(easing,startTime,endTime,startscaleX,startscaleY,endscaleX,endscaleY,loop = False):
    valid = True
    errors = ""
    if easing not in range(35):
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
            return "\n  V,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startscaleX, startscaleY, endscaleX, endscaleY)
        return "\n V,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startscaleX, startscaleY, endscaleX, endscaleY)
    else:
        return "\n" + errors

def rotate(easing,startTime,endTime,startRotate,endRotate,loop = False):
    valid = True
    errors = ""
    if easing not in range(35):
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
            return "\n  R,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startRotate, endRotate)
        return "\n R,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startRotate, endRotate)
    else:
        return "\n" + errors

def color(easing,startTime,endTime,startR,startG,startB,endR,endG,endB,loop = False):
    valid = True
    errors = ""
    if easing not in range(35):
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
            return "\n  C,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startR, startG, startB, endR, endG, endB)
        return "\n C,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startR, startG, startB, endR, endG, endB)
    else:
        return "\n" + errors

def para(easing,startTime,endTime,parameter):
    valid = True
    errors = ""
    if easing not in range(35):
        errors += "Invalid Easing! "
        valid = False
    if not isinstance(startTime, int) or not isinstance(endTime, int) or endTime < startTime:
        errors += "Invalid Time! "
        valid = False
    if parameter not in ["H", "V", "A"]:
        errors += "Invalid Parameter!"
        valid = False
    if valid:
        return "\n P,%s,%s,%s,%s" % (easing, startTime, endTime, parameter)
    else:
        return "\n" + errors

def loop(startTime,loopCount):
    valid = True
    errors = ""
    if not isinstance(startTime, int) or not isinstance(loopCount, int):
        errors += "Invalid Time or Loop count! "
        valid = False
    if valid:
        return "\n L,%s,%s" % (startTime, loopCount)
    else:
        return "\n" + errors

def trigger(trigger, startTime,loopCount):
    valid = True
    errors = ""
    if type(trigger) is not str:
        errors += "Invalid Trigger!"
        valid = False
    if not isinstance(startTime, int) or not isinstance(loopCount, int):
        errors += "Invalid Time or Loop count! "
        valid = False
    if valid:
        return "\n T,%s,%s,%s" % (trigger,startTime, loopCount)
    else:
        return "\n" + errors

def sinus(har, radius, sinheight):
    x1 = np.linspace(0, 6.1, har)
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

def spectrum(wav_file,mi,mx,har,start,end,gap,posX,posY,arrange,radius=30,sinheight=6.1):
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
        obj[n] = stat("bar.png","Foreground","BottomLeft",posX+position*gap+int(round(float(cirpos[n]))),posY+int(round(float(sinpos[n]))))
        position += 1
        obj[n] += rotate(0,start,start,math.ceil((1.5707+n*rotation)*1000)/1000,math.ceil((1.5707+n*rotation)*1000)/1000)
        obj[n] += fade(0,start,start+1000,0,1)
        obj[n] += fade(0,end-1000,end,1,0)
        for index,power in enumerate(spectrum[n]):
            power = ((power-minimum)/(maximum - minimum))*(mx-mi)+mi
            power = math.ceil(power*1000)/1000
            if power == lastval or int(round(t[index]*1000)) < start or int(round(t[index]*1000)) > end or index % 2 is not 0:
                lasttime = int(round(t[index]*1000))
                continue
            else:
                obj[n] += vecscale(0,lasttime,int(round(t[index]*1000)),1,lastval,1,power)
                lastval = power
                lasttime = int(round(t[index]*1000))
        n += 1

def end(osbfile):
    if os.path.isfile(osbfile):
        os.remove(osbfile)
    with open(osbfile, "a") as text:
        for k,v in obj.items():
            text.write("%s\n" % v)