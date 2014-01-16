def Keys():
    return [0.0, 0.005, 0.25, 0.9, 1.0]


def Vals():
    return [0.0, 1.0, 0.5, 0.1, 0.0]


def Harmonics(self, freq, length):
    a = self.sine(freq * 2.0, length, Rate)
    #b = sine(freq * 4.0, length, Rate)
    #c = sine(freq * 8.0, length, Rate)
    b = numpy.cos(2 * a * random() / 5.0)
    c = numpy.sin(2 * b + random() / 5.0)
    return (a * 10)
