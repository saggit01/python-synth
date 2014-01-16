#!/usr/bin/python
import math, numpy, pyaudio, itertools
from scipy import interpolate
from operator import itemgetter
from random import *
from pylab import *
import sys
import time
import Config

Rate = 44100


class Note:
    NOTES = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']

    def __init__(self, note, octave=4):
        self.octave = octave
        if isinstance(note, int):
            self.index = note
            self.note = Note.NOTES[note]
        elif isinstance(note, str):
            self.note = note.strip().lower()
            self.index = Note.NOTES.index(self.note)

    def transpose(self, halfsteps):
        octave_delta, note = divmod(self.index + halfsteps, 12)
        return Note(note, self.octave + octave_delta)

    def frequency(self):
        base_frequency = 16.35159783128741 * 2.0 ** (float(self.index) / 12.0)
        return base_frequency * (2.0 ** self.octave)

    def __float__(self):
        return self.frequency()


class Scale:
    def __init__(self, root, intervals):
        self.root = Note(root.index, 0)
        self.intervals = intervals

    def get(self, index):
        intervals = self.intervals
        if index < 0:
            index = abs(index)
            intervals = reversed(self.intervals)
        intervals = itertools.cycle(self.intervals)
        note = self.root
        for i in range(index):
            note = note.transpose(next(intervals))
        return note

    def index(self, note):
        intervals = itertools.cycle(self.intervals)
        index = 0
        x = self.root
        while x.octave != note.octave or x.note != note.note:
            x = x.transpose(next(intervals))
            index += 1
        return index

    def transpose(self, note, interval):
        return self.get(self.index(note) + interval)


class Synth:
    def __init__(self, overtones, vol):
        self.keys = Config.Keys()
        self.vals = Config.Vals()
        self.vol = vol
        self.overtones = overtones

    def sin_wave(self, frequency, length, rate):
        #self.keys[1] = 0.5
        length = int(length * rate)
        factor = float(frequency) * (math.pi * 2) / rate
        return numpy.sin(numpy.arange(length) * factor)

    def Harmonics(self, freq, length):
        waves = self.sin_wave(freq, length, Rate) * self.vol[0]
        for i in range(1, self.overtones):
            waves = waves + self.sin_wave(freq * (i + 1), length, Rate) * self.vol[i]
        print("Done")
        return waves

    def Shape(self, data, kind='slinear'):
        interp = interpolate.interp1d(self.keys, self.vals, kind=kind)
        factor = 1.0 / len(data)
        Shape = interp(numpy.arange(len(data)) * factor)
        return data * Shape

    def MakeChunk(self, note, length):
        chunk = self.Harmonics(note.frequency(), length)
        return self.Shape(chunk)


class Player():
    def __init__(self, overtones, vol):
        self.root = Note('A', 1)
        self.Synth = Synth(overtones, vol)
        self.scale = Scale(self.root, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    def Play(self, strpath):
        myfile = open(strpath)
        filelines = myfile.readlines()
        lines = len(filelines)
        chunks = []
        p = pyaudio.PyAudio()
        for i in range(0, lines):
            index = int(filelines[i][:2])
            length = float(filelines[i][2:])
            chunks.append(self.Synth.MakeChunk(self.scale.get(index), length))
            chunk = numpy.concatenate(chunks) * 0.25
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
        stream.write(chunk.astype(numpy.float32).tostring())
        stream.close()
        p.terminate()

    def showWaveform(self):
        length = 0.2
        wave = self.Synth.Harmonics(self.scale.get(20).frequency(), length)
        plot(numpy.arange(int(length * 44100)), wave, 'r')
        print("vbrwtbwrb")
        show()
