import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import scipy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy.fft import rfft, rfftfreq

import main


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')


sg.theme('Dark Grey 13')

headers = ['тип', 'результат', 'норма']
data = [
    ['Мощность VLF', '-', '765±410'],
    ['Мощность LF', '-', '1170±416'],
    ['Мощность HF', '-', '975±203'],
    ['LF нормированная', '-', '50,6±9,4%'],
    ['HF нормированная', '-', '49,4±9,4%'],

]

layout = [
    [sg.Text('Введите файл RR-кривых', pad=(20, 5))],
    [sg.InputText(size=(100, 20), pad=(20, 5), key='-INPUT-'), sg.FileBrowse('Найти', pad=(20, 0)),
     sg.Button('Анализ', key='-SUBMIT-')],
    [
        sg.Canvas(size=(270, 20)),
        sg.Text('График Сигнала', pad=(20, 5)),
        sg.Canvas(size=(340, 20)),
        sg.Text('Диаграмма Плотности сигналов', pad=(20, 5)),
    ],

    [
        sg.Canvas(size=(650, 350), key='-CANVAS-GRAPH-', pad=(20, 5), background_color='white'),
        sg.Canvas(size=(350, 350), key='-CANVAS-DIAGRAM-', pad=(20, 5), background_color='white')
    ],

    [
        sg.Canvas(size=(270, 20)),
        sg.Text('График Спектра', pad=(20, 5)),
        sg.Canvas(size=(400, 20)),
        sg.Text('Результат', pad=(20, 5)),
    ],

    [
        sg.Canvas(size=(650, 350), key='-CANVAS-SPECTRUM-', pad=(20, 5), background_color='white'),

        sg.Table(auto_size_columns=True, values=data, headings=headers, key='-CANVAS-RESULT-', pad=(20, 5)),

    ],
    [
        sg.Text('Вывод', font='Helvetica 28', key='-CONCLUSION-')
    ]

]

window = sg.Window('Оценка стресс состояния', layout)

fig_graph = None
fig_diagram = None
fig_spectrum = None
fig_result = None
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-SUBMIT-':
        try:
            path = str(values['-INPUT-'])
            if not path.endswith('.rr'):
                sg.popup('Неверный формат файла или такого файла не существует')
                continue
            y = main.read_from_file(path)
            N = len(y)
            x = np.linspace(1, N, N, endpoint=False)
            canvas_elem = window['-CANVAS-GRAPH-'].TKCanvas
            if fig_graph is not None:
                delete_fig_agg(fig_graph)
            fig_graph = draw_figure(canvas_elem, main.draw_plot(x, y, 'График Сигнала', 650, 350))
            canvas_elem = window['-CANVAS-SPECTRUM-'].TKCanvas
            if fig_spectrum is not None:
                delete_fig_agg(fig_spectrum)
            freq = N / (sum(y) / 1000)
            xf, yf = scipy.signal.welch(y, detrend='constant', scaling='spectrum', fs=freq)
            fig_spectrum = draw_figure(canvas_elem, main.draw_plot(xf, yf, 'График Спектра', 650, 350))
        except Exception as e:
            sg.popup('Такого файла не существует')
        hist_x = ['VLF', 'LF', 'HF']
        VLF_end = int(0.04 / (max(xf) / len(xf)))
        LF_end = int(0.15 / (max(xf) / len(xf)))
        HF_end = int(0.4 / (max(xf) / len(xf)))
        hist_y = [sum(yf[0:VLF_end]), sum(yf[VLF_end:LF_end]), sum(yf[LF_end:HF_end])]
        canvas_elem = window['-CANVAS-DIAGRAM-'].TKCanvas
        if fig_diagram is not None:
            delete_fig_agg(fig_diagram)
        fig_diagram = draw_figure(canvas_elem, main.draw_rect_plot(hist_x, hist_y, 'Диаграмма мощности', 350, 350))
        canvas_elem = window['-CANVAS-RESULT-']
        values = canvas_elem.Values
        values[0][1] = round(hist_y[0])
        values[1][1] = round(hist_y[1])
        values[2][1] = round(hist_y[2])
        values[3][1] = round((hist_y[1]) / (hist_y[1] + hist_y[2]) * 100, 1)
        values[4][1] = round((hist_y[2]) / (hist_y[1] + hist_y[2]) * 100, 1)
        canvas_elem.update(values)
        canvas_elem = window['-CONCLUSION-']
        canvas_elem.update('Вывод : ' + main.analyze(hist_y[2]))

window.close()
