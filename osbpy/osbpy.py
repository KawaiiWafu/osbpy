import os
import pylab as plt
import math
import numpy as np
from scipy.io import wavfile


def sinus(har, radius, sinheight):
    x1 = np.linspace(0, sinheight, har)
    y1 = np.sin(x1)
    sinus = plt.plot(x1, y1, 'bo')
    ysinus = sinus[0].get_ydata() * radius
    return ysinus


def gencircle(r, n):
    for i in range(len(r)):
        for j in range(n[i]):
            yield r[i], j * (2 * np.pi / n[i])


def circle(har, radius):
    circle = []
    xcircle = {}
    ycircle = {}
    for r, t in gencircle([2 * radius], [har]):
        circle += plt.plot(r * np.cos(t), r * np.sin(t), 'bo')
    for index, val in enumerate(circle):
        xcircle[index] = val.get_xdata()
        ycircle[index] = val.get_ydata()
    return ycircle, xcircle


# Lazy
def error_check(errors, path=None, layer=None, origin=None, posX=None, posY=None, posX2=None, posY2=None, easing=None, framecount=None, framerate=None, loop=None, startTime=None, endTime=None, startFade=None, endFade=None, startFade2=None, endFade2=None):
    valid = True
    if path is not None:
        if type(path) is not str:
            errors.append("Invalid Path! ")
            valid = False
    if layer is not None:
        if layer not in ["Background","Fail","Pass","Foreground"]:
            errors.append("Invalid Layer! ")
            valid = False
    if origin is not None:
        if origin not in ["TopLeft","TopCentre","TopRight","CentreLeft","Centre","CentreRight","BottomLeft","BottomCentre","BottomRight"]:
            errors.append("Invalid Origin! ")
            valid = False
    if posX is not None:
        if not isinstance(posX, int):
            errors.append("Invalid Position! ")
            valid = False
    if posY is not None:
        if not isinstance(posY, int):
            errors.append("Invalid Position! ")
            valid = False
    if posX2 is not None:
        if not isinstance(posX2, int):
            errors.append("Invalid Position! ")
            valid = False
    if posY2 is not None:
        if not isinstance(posY2, int):
            errors.append("Invalid Position! ")
            valid = False
    if easing is not None:
        if easing not in range(35):
            errors.append("Invalid Easing.")
            valid = False
    if framecount is not None:
        if not isinstance(framecount, int):
            errors.append("Invalid Frame count! ")
            valid = False
    if framerate is not None:
        if not isinstance(framerate, int):
            errors.append("Invalid Frame rate! ")
            valid = False
    if loop is not None:
        if loop not in ["LoopForever", "LoopOnce"]:
            errors.append("Invalid Type! ")
            valid = False
    if startTime is not None:
        if not isinstance(startTime, int):
            errors.append("Invalid Time! ")
            valid = False
    if endTime is not None:
        if not isinstance(endTime, int) or endTime < startTime:
            errors.append("Invalid Time! ")
            valid = False
    if startFade is not None:
        if not (isinstance(startFade, int) or isinstance(startFade, float)):
            errors.append("Invalid Fade/Scale! ")
            valid = False
    if endFade is not None:
        if not (isinstance(endFade, int) or isinstance(endFade, float)):
            errors.append("Invalid Fade/Scale! ")
            valid = False
    if startFade2 is not None:
        if not (isinstance(startFade2, int) or isinstance(startFade2, float)):
            errors.append("Invalid Scale! ")
            valid = False
    if endFade2 is not None:
        if not (isinstance(endFade2, int) or isinstance(endFade2, float)):
            errors.append("Invalid Scale! ")
            valid = False
    return valid


class osbject:
    obj_background = []
    obj_fail = []
    obj_pass = []
    obj_foreground = []
    obj_link = {"Background" : obj_background, "Fail" : obj_fail, "Pass" : obj_pass, "Foreground" : obj_foreground}
    def __init__(self, path, layer, origin, posX, posY, framecount=None, framerate=None, loop=None):
        osbject.obj_link[layer].append(self)
        self.props = []
        errors = []
        valid = error_check(errors, path=path, layer=layer, origin=origin, posX=posX, posY=posY, framecount=framecount, framerate=framerate, loop=loop)
        if framecount is not None and framerate is not None and loop is not None:
            if valid:
                self.props.append("Animation,%s,%s,%s,%s,%s,%s,%s,%s" % (layer, origin, path, posX, posY, framecount, framerate, loop))
            else:
                self.props.append("".join(errors))
        else:
            if valid:
                self.props.append("Sprite,%s,%s,%s,%s,%s" % (layer, origin, path, posX, posY))
            else:
                self.props.append("".join(errors))


    def fade(self, easing, startTime, endTime, startFade, endFade, loop=False):
        errors = []
        valid = error_check(errors, easing=easing, startTime=startTime, endTime=endTime, startFade=startFade, endFade=endFade)
        if startTime == endTime:
            endTime = ""
        if valid:
            if loop:
                if startFade == endFade:
                    self.props.append("\n  F,%s,%s,%s,%s" % (easing, startTime, endTime, startFade))
                else:
                    self.props.append("\n  F,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startFade, endFade))
            else:
                if startFade == endFade:
                    self.props.append("\n F,%s,%s,%s,%s" % (easing, startTime, endTime, startFade))
                else:
                    self.props.append("\n F,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startFade, endFade))
        else:
            self.props.append("\n" + "".join(errors))


    def move(self, easing, startTime, endTime, startmoveX, startmoveY, endmoveX, endmoveY, loop=False):
        errors = []
        valid = error_check(errors, posX=startmoveX, posY=startmoveY, posX2=endmoveX, posY2=endmoveY, easing=easing, startTime=startTime, endTime=endTime)
        if startTime == endTime:
            endTime = ""
        if valid:
            if loop:
                if startmoveX == endmoveX and startmoveY == endmoveY:
                    self.props.append("\n  M,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, startmoveY))
                else:
                    self.props.append("\n  M,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, startmoveY, endmoveX, endmoveY))
            else:
                if startmoveX == endmoveX and startmoveY == endmoveY:
                    self.props.append("\n M,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, startmoveY))
                else:
                    self.props.append("\n M,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, startmoveY, endmoveX, endmoveY))
        else:
            self.props.append("\n" + "".join(errors))


    def moveX(self, easing, startTime, endTime, startmoveX, endmoveX, loop = False):
        errors = []
        valid = error_check(errors, posX=startmoveX, posY=endmoveX, easing=easing, startTime=startTime, endTime=endTime)
        if startTime == endTime:
            endTime = ""
        if valid:
            if loop:
                if startmoveX == endmoveX:
                    self.props.append("\n  MX,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX))
                else:
                    self.props.append("\n  MX,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, endmoveX))
            else:
                if startmoveX == endmoveX:
                    self.props.append("\n MX,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX))
                else:
                    self.props.append("\n MX,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveX, endmoveX))
        else:
            self.props.append("\n" + "".join(errors))


    def moveY(self, easing, startTime, endTime, startmoveY, endmoveY, loop = False):
        errors = []
        valid = error_check(errors, posX=startmoveY, posY=endmoveY, easing=easing, startTime=startTime, endTime=endTime)
        if startTime == endTime:
            endTime = ""
        if valid:
            if loop:
                if startmoveY == endmoveY:
                    self.props.append("\n  MY,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveY))
                else:
                    self.props.append("\n  MY,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveY, endmoveY))
            else:
                if startmoveY == endmoveY:
                    self.props.append("\n MY,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveY))
                else:
                    self.props.append("\n MY,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startmoveY, endmoveY))
        else:
            self.props.append("\n" + "".join(errors))


    def scale(self, easing, startTime, endTime, startScale, endScale, loop = False):
        errors = []
        valid = error_check(errors, startFade=startScale, endFade=endScale, easing=easing, startTime=startTime, endTime=endTime)
        if startTime == endTime:
            endTime = ""
        if valid:
            if loop:
                if startScale == endScale:
                    self.props.append("\n  S,%s,%s,%s,%s" % (easing, startTime, endTime, startScale))
                else:
                    self.props.append("\n  S,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startScale, endScale))
            else:
                if startScale == endScale:
                    self.props.append("\n S,%s,%s,%s,%s" % (easing, startTime, endTime, startScale))
                else:
                    self.props.append("\n S,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startScale, endScale))
        else:
            self.props.append("\n" + "".join(errors))


    def vecscale(self, easing, startTime, endTime, startscaleX, startscaleY, endscaleX, endscaleY, loop = False):
        errors = []
        valid = error_check(errors, startFade=startscaleX, endFade=startscaleY, startFade2=endscaleX, endFade2=endscaleY, easing=easing, startTime=startTime, endTime=endTime)
        if startTime == endTime:
            endTime = ""
        if valid:
            if loop:
                if startscaleX == endscaleX and startscaleY == endscaleY:
                    self.props.append("\n  V,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startscaleX, startscaleY))
                else:
                    self.props.append("\n  V,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startscaleX, startscaleY, endscaleX, endscaleY))
            else:
                if startscaleX == endscaleX and startscaleY == endscaleY:
                    self.props.append("\n V,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startscaleX, startscaleY))
                else:
                    self.props.append("\n V,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startscaleX, startscaleY, endscaleX, endscaleY))
        else:
            self.props.append("\n" + "".join(errors))


    def rotate(self, easing, startTime, endTime, startRotate, endRotate, loop = False):
        errors = []
        valid = error_check(errors, easing=easing, startTime=startTime, endTime=endTime, startFade=startRotate, endFade=endRotate)
        if startTime == endTime:
            endTime = ""
        if valid:
            if loop:
                if startRotate == endRotate:
                    self.props.append("\n  R,%s,%s,%s,%s" % (easing, startTime, endTime, startRotate))
                else:
                    self.props.append("\n  R,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startRotate, endRotate))
            else:
                if startRotate == endRotate:
                    self.props.append("\n R,%s,%s,%s,%s" % (easing, startTime, endTime, startRotate))
                else:
                    self.props.append("\n R,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startRotate, endRotate))
        else:
            self.props.append("\n" + "".join(errors))


    def colour(self, easing, startTime, endTime, startR, startG, startB, endR, endG, endB, loop = False):
        errors = []
        valid = error_check(errors, easing=easing, startTime=startTime, endTime=endTime)
        if startTime == endTime:
            endTime = ""
        if startR is not None:
            if startR not in range(256):
                errors.append("Invalid Colour!")
        if startG is not None:
            if startG not in range(256):
                errors.append("Invalid Colour!")
        if startB is not None:
            if startB not in range(256):
                errors.append("Invalid Colour!")
        if endR is not None:
            if endR not in range(256):
                errors.append("Invalid Colour!")
        if endG is not None:
            if endG not in range(256):
                errors.append("Invalid Colour!")
        if endB is not None:
            if endB not in range(256):
                errors.append("Invalid Colour!")
        if valid:
            if loop:
                if startR == endR and startG == endG and startB == endB:
                    self.props.append("\n  C,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startR, startG, startB))
                else:
                    self.props.append("\n  C,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startR, startG, startB, endR, endG, endB))
            else:
                if startR == endR and startG == endG and startB == endB:
                    self.props.append("\n C,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startR, startG, startB))
                else:
                    self.props.append("\n C,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (easing, startTime, endTime, startR, startG, startB, endR, endG, endB))
        else:
            self.props.append("\n" + "".join(errors))


    def para(self, easing, startTime, endTime, parameter):
        errors = []
        valid = error_check(errors, easing=easing, startTime=startTime, endTime=endTime)
        if startTime == endTime:
            endTime = ""
        if parameter not in ["H", "V", "A"]:
            errors.append("Invalid Parameter!")
            valid = False
        if valid:
            self.props.append("\n P,%s,%s,%s,%s" % (easing, startTime, endTime, parameter))
        else:
            self.props.append("\n" + "".join(errors))


    def loop(self, startTime, loopCount):
        valid = True
        errors = []
        if not isinstance(startTime, int) or not isinstance(loopCount, int):
            errors.append("Invalid Time or Loop count! ")
            valid = False
        if valid:
            self.props.append("\n L,%s,%s" % (startTime, loopCount))
        else:
            self.props.append("\n" + "".join(errors))


    def trigger(self, trigger, startTime, loopCount):
        errors = []
        valid = error_check(errors, path=trigger, startTime=startTime, posX=loopCount)
        if valid:
            self.props.append("\n T,%s,%s,%s" % (trigger, startTime, loopCount))
        else:
            self.props.append("\n" + "".join(errors))

    @classmethod
    def end(cl, osbfile):
        if os.path.isfile(osbfile):
            os.remove(osbfile)
        with open(osbfile, "a") as text:
            text.write("[Events]\n//Background and Video events\n//Storyboard Layer 0 (Background)\n")
            for val in cl.obj_background:
                text.write("%s\n" % "".join(val.props))
            text.write("//Storyboard Layer 1 (Fail)\n")
            for val in cl.obj_fail:
                text.write("%s\n" % "".join(val.props))
            text.write("//Storyboard Layer 2 (Pass)\n")
            for val in cl.obj_pass:
                text.write("%s\n" % "".join(val.props))
            text.write("//Storyboard Layer 3 (Foreground)\n")
            for val in cl.obj_foreground:
                text.write("%s\n" % "".join(val.props))
            text.write("//Storyboard Sound Samples\n")


def spectrum(wav_file, mi, mx, har, start, end, posX, posY, layer, origin, gap=0, arrange="", radius=30, sinheight=6.1):
    spect = []
    frame_rate, snd = wavfile.read(wav_file)
    sound_info = snd[:,0]
    spectrum, freqs, t, im = plt.specgram(sound_info, NFFT=1024, Fs=frame_rate, noverlap=5, mode='magnitude')
    n = 0
    rotation = 6.2831
    sinpos = {}
    cirpos = {}
    if arrange is "sinus":
        sinpos = sinus(har, radius, sinheight)
        for i in range(har):
            cirpos[i] = 0
    elif arrange is "circle":
        gap = 0
        sinpos, cirpos = circle(har, radius)
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
        lastval = ((spectrum[n][0] - minimum) / (maximum - minimum)) * (mx - mi) + mi
        lastval = math.ceil(lastval * 1000) / 1000
        lasttime = int(round(t[0] * 1000))
        spect.append(osbject("bar.png", layer, origin, posX + position * gap + int(round(float(cirpos[n]))), posY + int(round(float(sinpos[n])))))
        position += 1
        if arrange is "circle":
            spect[n].rotate(0, start, start, math.ceil((1.5707 + n * rotation) * 1000) / 1000, math.ceil((1.5707 + n * rotation) * 1000) / 1000)
        for index, power in enumerate(spectrum[n]):
            power = ((power - minimum) / (maximum - minimum)) * (mx - mi) + mi
            power = math.ceil(power * 1000) / 1000
            if power == lastval or int(round(t[index] * 1000)) < start or int(round(t[index] * 1000)) > end or index % 2 is not 0:
                lasttime = int(round(t[index] * 1000))
                continue
            else:
                spect[n].vecscale(0, lasttime, int(round(t[index] * 1000)), 1, lastval, 1, power)
                lastval = power
                lasttime = int(round(t[index] * 1000))
        n += 1
    return spect
