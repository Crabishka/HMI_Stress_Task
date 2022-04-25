import numpy as np
import scipy as scipy
from matplotlib import pyplot as plt
from numpy.fft import rfft, rfftfreq
from scipy import signal

SAMPLE_RATE = 200


def draw_plot(x, y, name):
    fig, ax = plt.subplots()
    ax.set_title(name)
    plt.plot(x, y)
    plt.show()


def read_from_file(path):
    f = open(path, 'r')
    y = []
    line = f.readline()
    while line != '':
        if line.startswith(';'):
            line = f.readline()
            continue
        else:
            y.append(int(line.split()[0]))
        line = f.readline()
    f.close()
    return y


if __name__ == '__main__':
    for i in range(1, 4):
        path = 'input/стресс' + str(i) + '.rr'
        y = np.array(read_from_file(path))
        N = len(y)
        x = np.linspace(1, N, N,  endpoint=False)
        xf, yf = scipy.signal.welch(y, detrend='constant', scaling='spectrum')
        draw_plot(sorted(x), y, str(i) + ' график')
        draw_plot(sorted(xf), np.abs(yf), 'Частотный спектр сигнала ' + str(i) + '-ого графика')
