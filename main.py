import numpy as np
import scipy as scipy
from matplotlib import pyplot as plt
from scipy import signal

DURATION = 300


def draw_plot(x, y, name, w, h):
    fig, ax = plt.subplots()
    ax.set_title(name)
    fig = plt.figure(figsize=(w / 100, h / 100))
    plt.plot(x, y)
    return fig


def draw_rect_plot(x, y, name, w, h):
    fig, ax = plt.subplots()
    ax.set_title(name)
    ax.set_facecolor('seashell')
    fig = plt.figure(figsize=(w / 100, h / 100))
    plt.bar(x, y)
    return fig


def analyze(HF_sum):
    if HF_sum > 1200 or HF_sum < 700:
        return 'Замечено отклонение от нормы по HF мощности'
    else:
        return 'Спектральная мощность HF соответствует норме'


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
        x = np.linspace(1, N, N, endpoint=False)
        freq = N / (sum(y) / 1000)
        xf, yf = scipy.signal.welch(y, detrend='constant', scaling='spectrum', fs=freq)
        VLF_end = int(0.04 / (max(xf) / N))
        LF_end = int(0.15 / (max(xf) / N))
        HF_end = int(0.4 / (max(xf) / N))
        print(sum(yf[LF_end:HF_end]))
        draw_plot(sorted(x), y, str(i) + ' график')
        draw_plot(sorted(xf), np.abs(yf), 'Частотный спектр сигнала ' + str(i) + '-ого графика')
