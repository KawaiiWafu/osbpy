import itertools
import math
import os
from string import ascii_lowercase
from string import ascii_uppercase
import numpy as np
import pylab as plt
from scipy.io import wavfile


def sine(har, radius, height):
    x1 = np.linspace(0, height, har)
    y1 = np.sin(x1)
    sine_plot = plt.plot(x1, y1, 'bo')
    result = sine_plot[0].get_ydata() * radius
    return result


def generate_circle(r, n):
    for i in range(len(r)):
        for j in range(n[i]):
            yield r[i], j * (2 * np.pi / n[i])


def circle(har, radius):
    result = []
    circle_x = {}
    circle_y = {}
    for r, t in generate_circle([2 * radius], [har]):
        result += plt.plot(r * np.cos(t), r * np.sin(t), 'bo')
    for index, val in enumerate(result):
        circle_x[index] = val.get_xdata()
        circle_y[index] = val.get_ydata()
    return circle_y, circle_x


def variable_name():
    size = 1
    while True:
        for varName in itertools.product(ascii_lowercase + ascii_uppercase, repeat=size):
            yield "".join(varName)
        size += 1


def check_path(path):
    if type(path) is not str:
        print("{val} is an invalid path.".format(val=path))
        return False
    return True


def check_layer(layer):
    if layer not in ("Background", "Fail", "Pass", "Foreground"):
        print("{val} is an invalid layer. Valid: Background, Fail, Pass, Foreground".format(val=layer))
        return False
    return True


def check_origin(origin):
    if origin not in (
            "TopLeft", "TopCentre", "TopRight",
            "CentreLeft", "Centre", "CentreRight",
            "BottomLeft", "BottomCentre", "BottomRight"
    ):
        print("{val} is an invalid origin. Valid: TopLeft, TopCentre, TopRight, CentreLeft, Centre, CentreRight,"
              "BottomLeft, BottomCentre, BottomRight".format(val=origin))
        return False
    return True


def check_int(integer):
    if not isinstance(integer, int):
        print("{val} is not an integer.".format(val=integer))
        return False
    return True


def check_easing(easing):
    if easing not in range(35):
        print("{val} is an invalid easing. Valid: Integers 0 - 34".format(val=easing))
        return False
    return True


def check_loop(loop):
    if loop not in ("LoopForever", "LoopOnce"):
        print("{val} is an invalid loop type. Valid: LoopForever, LoopOnce".format(val=loop))
        return False
    return True


def check_dec(dec):
    if not (isinstance(dec, int) or isinstance(dec, float)):
        print("{val} is not a decimal or an integer.".format(val=dec))
        return False
    return True


def check_time(start, end):
    if not isinstance(start, int):
        print("Time {val} is not an integer.".format(val=start))
        return False
    if not isinstance(end, int):
        print("Time {val} is not an integer.".format(val=end))
        return False
    if end < start:
        print("End time {val1} is greater than start time {val2}.".format(val1=end, val2=start))
        return False
    return True


def check_colours(args):
    for color in args:
        if color not in range(256):
            print("{val} is an invalid color. Valid: 0 - 255".format(val=color))
            return False
    return True


def check_parameter(parameter):
    if parameter not in ('H', 'V', 'A'):
        print("{val} is an invalid Parameter. Valid: H, V, A".format(val=parameter))
        return False
    return True


def check_trigger(trigger):
    if trigger not in ("Failing", "Passing") and not trigger.startswith("HitSound"):
        print("{val} is an invalid Trigger. Valid: Failing, Passing, HitSound...".format(val=trigger))
        return False
    return True


class Osbject:
    obj_background = []
    obj_fail = []
    obj_pass = []
    obj_foreground = []
    obj_link = {"Background": obj_background,
                "Fail": obj_fail,
                "Pass": obj_pass,
                "Foreground": obj_foreground}
    minim = []
    minim_duplicate = [",0,1",
                       ",1,0",
                       ",0,0",
                       ",1,1"]
    minim_threshold = 0
    minim_time_collision = False

    def __init__(self, path, layer, origin, posx, posy, frame_count=None, frame_rate=None, loop=None):
        Osbject.obj_link[layer].append(self)
        self.props = []
        valid = check_path(path) and check_layer(layer) and check_origin(origin) and check_int(posx) and check_int(posy)

        if frame_count is not None and frame_rate is not None and loop is not None:
            tag = "Animation"
            valid = valid and check_int(frame_count) and check_int(frame_rate) and check_loop(loop)
            if valid:
                self.add((tag, layer, origin, path, posx, posy, frame_count, frame_rate, loop))
        else:
            tag = "Sprite"
            if valid:
                self.add((tag, layer, origin, path, posx, posy))

        if valid:
            self.minimize(",".join((tag, layer, origin)) + ",", True)
            if Osbject.minim_threshold != 0:
                self.minimize("," + ",".join(map(str, (posx, posy))))
            self.minimize(path, True)

    def add(self, args):
        self.props.append(",".join(map(str, args)))

    def fade(self, easing, start, end, start_fade, end_fade, loop=False):
        valid = check_easing(easing) and check_time(start, end) and check_dec(start_fade) and check_dec(end_fade)
        if start == end:
            end = ""
        if valid:
            if loop:
                tag = "\n  F"
            else:
                tag = "\n F"

            if start_fade == end_fade:
                self.add((tag, easing, start, end, start_fade))
            else:
                self.add((tag, easing, start, end, start_fade, end_fade))
                if Osbject.minim_threshold != 0:
                    self.minimize("," + ",".join(map(str, (start_fade, end_fade))))
                    self.minimize("," + str(end_fade))

            self.minimize(",".join(map(str, (tag.lstrip("\n"), easing))), True)
            if Osbject.minim_threshold != 0:
                if Osbject.minim_time_collision:
                    self.minimize("," + ",".join(map(str, (start, end))))
                    self.minimize("," + str(start))
                    self.minimize("," + str(end))
                self.minimize("," + str(start_fade))

    def move(self, easing, start, end, start_movex, start_movey, end_movex, end_movey, loop=False):
        valid = check_int(start_movex) and check_int(start_movey) and check_int(end_movex) and check_int(end_movey)
        valid = valid and check_easing(easing) and check_time(start, end)
        if start == end:
            end = ""
        if valid:
            if loop:
                tag = "\n  M"
            else:
                tag = "\n M"

            if start_movex == end_movex and start_movey == end_movey:
                self.add((tag, easing, start, end, start_movex, start_movey))
            else:
                self.add((tag, easing, start, end, start_movex, start_movey, end_movex, end_movey))
                if Osbject.minim_threshold != 0:
                    self.minimize("," + ",".join(map(str, (end_movex, end_movey))))
                    self.minimize("," + str(end_movex))
                    self.minimize("," + str(end_movey))

            self.minimize(",".join(map(str, (tag.lstrip("\n"), easing))), True)
            if Osbject.minim_threshold != 0:
                if Osbject.minim_time_collision:
                    self.minimize("," + ",".join(map(str, (start, end))))
                    self.minimize("," + str(start))
                    self.minimize("," + str(end))
                self.minimize("," + ",".join(map(str, (start_movex, start_movey))))
                self.minimize("," + str(start_movex))
                self.minimize("," + str(start_movey))

    def movex(self, easing, start, end, start_movex, end_movex, loop=False, swap=False):
        valid = check_easing(easing) and check_time(start, end) and check_int(start_movex) and check_int(end_movex)
        if start == end:
            end = ""
        if valid:
            if loop:
                if swap:
                    tag = "\n  MY"
                else:
                    tag = "\n  MX"
            else:
                if swap:
                    tag = "\n MY"
                else:
                    tag = "\n MX"

            if start_movex == end_movex:
                self.add((tag, easing, start, end, start_movex))
            else:
                self.add((tag, easing, start, end, start_movex, end_movex))
                if Osbject.minim_threshold != 0:
                    self.minimize("," + ",".join(map(str, (start_movex, end_movex))))
                    self.minimize("," + str(end_movex))

            self.minimize(",".join(map(str, (tag.lstrip("\n"), easing))), True)
            if Osbject.minim_threshold != 0:
                if Osbject.minim_time_collision:
                    self.minimize("," + str(start))
                    self.minimize("," + str(end))
                    self.minimize("," + ",".join(map(str, (start, end))))
                self.minimize("," + str(start_movex))

    def movey(self, easing, start, end, start_movey, end_movey, loop=False):
        self.movex(easing, start, end, start_movey, end_movey, loop, True)

    def scale(self, easing, start, end, start_scale, end_scale, loop=False):
        valid = check_easing(easing) and check_time(start, end) and check_dec(start_scale) and check_dec(end_scale)
        if start == end:
            end = ""
        if valid:
            if loop:
                tag = "\n  S"
            else:
                tag = "\n S"

            if start_scale == end_scale:
                self.add((tag, easing, start, end, start_scale))
            else:
                self.add((tag, easing, start, end, start_scale, end_scale))
                if Osbject.minim_threshold != 0:
                    self.minimize("," + ",".join(map(str, (start_scale, end_scale))))
                    self.minimize("," + str(end_scale))

            self.minimize(",".join(map(str, (tag.lstrip("\n"), easing))), True)
            if Osbject.minim_threshold != 0:
                if Osbject.minim_time_collision:
                    self.minimize("," + ",".join(map(str, (start, end))))
                    self.minimize("," + str(start))
                    self.minimize("," + str(end))
                self.minimize("," + str(start_scale))

    def vecscale(self, easing, start, end, start_scalex, start_scaley, end_scalex, end_scaley, loop=False):
        valid = check_dec(start_scalex) and check_dec(start_scaley) and check_dec(end_scalex) and check_dec(end_scaley)
        valid = valid and check_easing(easing) and check_time(start, end)
        if start == end:
            end = ""
        if valid:
            if loop:
                tag = "\n  V"
            else:
                tag = "\n V"

            if start_scalex == end_scalex and start_scaley == end_scaley:
                self.add((tag, easing, start, end, start_scalex, start_scaley))
            else:
                self.add((tag, easing, start, end, start_scalex, start_scaley, end_scalex, end_scaley))
                if Osbject.minim_threshold != 0:
                    self.minimize("," + ",".join(map(str, (end_scalex, end_scaley))))
                    self.minimize("," + str(end_scalex))
                    self.minimize("," + str(end_scaley))

            self.minimize(",".join(map(str, (tag.lstrip("\n"), easing))), True)
            if Osbject.minim_threshold != 0:
                self.minimize("," + ",".join(map(str, (start_scalex, start_scaley))))
                self.minimize("," + str(start_scalex))
                self.minimize("," + str(start_scaley))
                if Osbject.minim_time_collision:
                    self.minimize("," + ",".join(map(str, (start, end))))
                    self.minimize("," + str(start))
                    self.minimize("," + str(end))

    def rotate(self, easing, start, end, start_rotate, end_rotate, loop=False):
        valid = check_easing(easing) and check_time(start, end) and check_dec(start_rotate) and check_dec(end_rotate)
        if start == end:
            end = ""
        if valid:
            if loop:
                tag = "\n  R"
            else:
                tag = "\n R"

            if start_rotate == end_rotate:
                self.add((tag, easing, start, end, start_rotate))
            else:
                self.add((tag, easing, start, end, start_rotate, end_rotate))
                if Osbject.minim_threshold != 0:
                    self.minimize("," + ",".join(map(str, (start_rotate, end_rotate))))
                    self.minimize("," + str(end_rotate))

            self.minimize(",".join(map(str, (tag.lstrip("\n"), easing))), True)
            if Osbject.minim_threshold != 0:
                self.minimize("," + str(start_rotate))
                if Osbject.minim_time_collision:
                    self.minimize("," + ",".join((str(start), str(end))))
                    self.minimize("," + str(start))
                    self.minimize("," + str(end))

    def colour(self, easing, start, end, r, g, b, end_r, end_g, end_b, loop=False):
        valid = check_easing(easing) and check_time(start, end)
        valid = valid and check_colours((r, g, b, end_r, end_g, end_b))
        if start == end:
            end = ""
        if valid:
            if loop:
                tag = "\n  C"
            else:
                tag = "\n C"

            if r == end_r and g == end_g and b == end_b:
                self.add((tag, easing, start, end, r, g, b))
            else:
                self.add((tag, easing, start, end, r, g, b, end_r, end_g, end_b))
                if Osbject.minim_threshold != 0:
                    self.minimize("," + ",".join(map(str, (end_r, end_g, end_b))))

            self.minimize(",".join(map(str, (tag.lstrip("\n"), easing))), True)
            if Osbject.minim_threshold != 0:
                if Osbject.minim_time_collision:
                    self.minimize("," + ",".join(map(str, (start, end))))
                    self.minimize("," + str(start))
                    self.minimize("," + str(end))
                self.minimize("," + ",".join(map(str, (r, g, b))))

    def para(self, easing, start, end, parameter):
        valid = check_easing(easing) and check_time(start, end) and check_parameter(parameter)
        if start == end:
            end = ""
        if valid:
            tag = "\n P"
            self.add((tag, easing, start, end, parameter))
            self.minimize(",".join(map(str, (tag.lstrip("\n"), easing))), True)
            if Osbject.minim_threshold != 0 and Osbject.minim_time_collision:
                self.minimize("," + ",".join(map(str, (start, end))))
                self.minimize("," + str(start))
                self.minimize("," + str(end))
            self.minimize(tag.lstrip("\n") + ",", True)

    def loop(self, start, loop_count):
        valid = check_int(start) and check_int(loop_count)
        if valid:
            tag = "\n L"
            self.add((tag, start, loop_count))
            if Osbject.minim_threshold != 0 and Osbject.minim_time_collision:
                self.minimize(",".join(map(str, (tag.lstrip("\n"), start))))
                self.minimize("," + ",".join(map(str, (start, loop_count))))
                self.minimize("," + str(start))
                self.minimize("," + str(loop_count))
            self.minimize(tag.lstrip("\n") + ",", True)

    def trigger(self, trigger, start, loop_count):
        valid = check_trigger(trigger) and check_int(start) and check_int(loop_count)
        if valid:
            tag = "\n T"
            self.add((tag, trigger, start, loop_count))
            self.minimize(",".join(map(str, (tag.lstrip("\n"), trigger))), True)
            if Osbject.minim_threshold != 0 and Osbject.minim_time_collision:
                self.minimize("," + ",".join(map(str, (start, loop_count))))
                self.minimize("," + str(start))
                self.minimize("," + str(loop_count))
            self.minimize(tag.lstrip("\n") + ",", True)

    @staticmethod
    def minimize(variable, force=False):
        if len(variable) >= Osbject.minim_threshold or force:
            if variable not in Osbject.minim:
                Osbject.minim.append(variable)
            elif variable not in Osbject.minim_duplicate:
                Osbject.minim_duplicate.append(variable)

    @classmethod
    def end(cls, osb_file):
        if os.path.isfile(osb_file):
            os.remove(osb_file)
        with open(osb_file, "a") as text:
            text.write("[Events]\n//Background and Video events\n//Storyboard Layer 0 (Background)\n")
            for val in cls.obj_background:
                text.write("%s\n" % "".join(val.props))
            text.write("//Storyboard Layer 1 (Fail)\n")
            for val in cls.obj_fail:
                text.write("%s\n" % "".join(val.props))
            text.write("//Storyboard Layer 2 (Pass)\n")
            for val in cls.obj_pass:
                text.write("%s\n" % "".join(val.props))
            text.write("//Storyboard Layer 3 (Foreground)\n")
            for val in cls.obj_foreground:
                text.write("%s\n" % "".join(val.props))
            text.write("//Storyboard Sound Samples\n")

    @classmethod
    def end_minimize(cls, osb_file):
        if os.path.isfile(osb_file):
            os.remove(osb_file)
        cls.end(osb_file + ".bkp")
        short_names = []
        c = 1
        cls.minim_duplicate.sort(key=len, reverse=True)
        for i in itertools.islice(variable_name(), len(cls.minim_duplicate)):
            short_names.append(i)
        short_names.reverse()
        minim_dict = dict(zip(cls.minim_duplicate, short_names))
        with open(osb_file + ".bkp") as backup_text:
            temporary_text = backup_text.read()
            with open(osb_file, "a") as text:
                text.write("[Variables]\n")
                for key, val in minim_dict.items():
                    text.write("$%s=%s\n" % (val, key))
                    temporary_text = temporary_text.replace(key, "".join(["$", val]))
                    print("%s/%s" % (c, len(minim_dict)))
                    c += 1
                text.write(temporary_text)

    @classmethod
    def set_minimize_threshold(cls, threshold):
        cls.minim_threshold = threshold

    @classmethod
    def set_minimize_time(cls, value):
        cls.minim_time_collision = value

    @classmethod
    def minimize_force(cls, variable):
        cls.minim_duplicate.append(variable)


def spectrum(
        wav_file, bar_file, mi, mx, har, start, end, posx, posy,
        layer, origin, gap=0, arrange="", radius=30, sine_height=6.1
):
    result = []
    frame_rate, snd = wavfile.read(wav_file)
    sound_info = snd[:, 0]
    specgram, frequencies, t, im = plt.specgram(sound_info, NFFT=1024, Fs=frame_rate, noverlap=5, mode='magnitude')
    n = 0
    rotation = 6.2831
    sine_pos = {}
    circle_pos = {}
    if arrange is "sine":
        sine_pos = sine(har, radius, sine_height)
        for i in range(har):
            circle_pos[i] = 0
    elif arrange is "circle":
        gap = 0
        sine_pos, circle_pos = circle(har, radius)
        rotation /= har
    else:
        for i in range(har):
            sine_pos[i] = 0
        for i in range(har):
            circle_pos[i] = 0
    maximum = plt.amax(specgram)
    minimum = plt.amin(specgram)
    position = 0
    while n < har:
        last_value = ((specgram[n][0] - minimum) / (maximum - minimum)) * (mx - mi) + mi
        last_value = math.ceil(last_value * 1000) / 1000
        last_time = int(round(t[0] * 1000))
        result.append(Osbject(
            bar_file, layer, origin, posx + position * gap + int(round(float(circle_pos[n]))),
            posy + int(round(float(sine_pos[n]))))
        )
        position += 1
        if arrange is "circle":
            result[n].rotate(
                0, start, start, math.ceil((1.5707 + n * rotation) * 1000) / 1000,
                math.ceil((1.5707 + n * rotation) * 1000) / 1000
            )
        for index, power in enumerate(specgram[n]):
            power = ((power - minimum) / (maximum - minimum)) * (mx - mi) + mi
            power = math.ceil(power * 1000) / 1000
            if power == last_value or int(round(t[index] * 1000)) < start or int(
                    round(t[index] * 1000)) > end or index % 2 is not 0:
                last_time = int(round(t[index] * 1000))
                continue
            else:
                result[n].vecscale(0, last_time, int(round(t[index] * 1000)), 1, last_value, 1, power)
                last_value = power
                last_time = int(round(t[index] * 1000))
        n += 1
    return result
