#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import csv
import scipy.optimize as opt
import math


class Data:
    def reciving_data(self):
        self.plot1 = []
        self.plot2 = []
        self.plot3 = []
        self.plot4 = []
        plots_together = []
        with open('1_wspolny.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                temp = [sample for sample in row if sample is not '']
                # plot 1,2 - prąd
                # plot 3,4 - napięcie
                self.plot1.append([float(temp[0]) + 0.15, float(temp[1])*(496.52/5)])
                self.plot2.append([float(temp[2]) + 0.15, float(temp[3])*(496.52/5)])
                self.plot3.append([float(temp[4]) + 0.15, float(temp[5])*(71.47)])
                self.plot4.append([float(temp[6]) + 0.15, float(temp[7])*(71.47)])

    def determination_of_local_max(self, sample_list):
        self.local_max = []
        first_local = True
        for number, sample in enumerate(sample_list):
            if number is 0:
                max_val = sample[1]
                max_val_x = sample[0]
            else:
                sample_before = sample_list[number-1]
                abs_sample_val = abs(sample[1])
                # sprawdzenie maksimum
                if abs_sample_val > abs(sample_before[1]) and abs_sample_val > abs(max_val):
                    max_val = abs_sample_val
                    max_val_x = sample[0]
                    if sample[1] < 0:
                        max_val = -1 * abs_sample_val
                # sprawdzenie kolejnego przedziału i przypisanie maximum/minimum
                # (te 7 będą do zmiany przy następnych labkach)
                if abs_sample_val < 7 and abs(sample_before[1]) > 7:
                    if first_local:
                        self.local_max.append([max_val_x, max_val])
                        max_val = 0
                        first_local = False
                    else:
                        # 0.018 okres przebiegu
                        if sample[0] - self.local_max[-1][0] > 0.019:
                            self.local_max.append([max_val_x, max_val])
                            max_val = 0

    def expot(self, x, a, b, c):
            return a * np.exp(b * x) + c

    def regresion(self):
        x = []
        y = []
        for i in self.local_max:
            x.append(i[0])
            y.append(i[1])
        x_np = np.array(x[0:4])
        y_np = np.array(y[0:4])
        popt, pcov = opt.curve_fit(self.expot, x_np, y_np)
        self.result = popt
        # self.result = opt.curve_fit(lambda t,a,b: (a*np.exp(b*t)), x_np, y_np, p0=(1, 5))


class Plots(Data):
    def plot(self):
        x = []
        y = []
        y_vol = []
        # plot 2 prad
        for samples in self.plot2:
            x.append(samples[0])
            y.append(samples[1])
        # plot 4 napiecie
        for samples in self.plot4:
            y_vol.append(samples[1])
        y = y[700:3200].copy()
        x = x[700:3200].copy()
        y_vol = y_vol[700:3200].copy()
        # obwiednia wykresu
        self.determination_of_local_max(self.plot2[700:3200])
        self.regresion()
        coefficent = self.result
        x_exp = np.arange(self.local_max[0][0], (-1/coefficent[2])*4, 0.001)
        y_exp = []
        for i in x_exp:
            y_exp.append(coefficent[0]*math.exp(coefficent[1]*i)+coefficent[2])
        y_exp = np.array(y_exp)
        # rysowanie wykresów
        fig, ax = plt.subplots()
        par1 = ax.twinx()
        plt.grid(True)
        line1, = ax.plot(x, y, label="i(t)")
        line3, = ax.plot(
            x_exp,
            y_exp,
            label="y(t) = " + str(round(coefficent[0], 2)) +
            " *e" + r'$^{%.2f *t}$' % (round(coefficent[1], 2))
            )
        line2, = par1.plot(x, y_vol, "r", label="u(t)")
        ax.set_xlabel("t [s]")
        ax.set_ylabel("I [A]")
        par1.set_ylabel("U [V]")
        lines = [line1, line2, line3]
        ax.legend(lines, [l.get_label() for l in lines])
        # wyznaczanie maksymalnej wartości prądu udarowego
        ymax = min(y)
        xpos = y.index(ymax)
        xmax = x[xpos]
        ax.set_ylim(-350, 350)
        ax.set_xlim(-0.01, 0.225)
        # rysowanie kres|
        ax.annotate(
                     '',
                     xy=(xmax, ymax),
                     # jeśli jest zadługa kreska - zmiana mianownika w xytext
                     xytext=(xmax-((abs(x[0])+abs(x[len(x)-1]))/13), ymax),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś zmiana mianownika
        xcenter = xmax-(abs(x[0])+abs(x[len(x)-1]))/22
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$I_{udar}$' + '= '+str(round(abs(ymax), 3))+'A',
                xy=(xcenter, ymax+(250/40)),
                ha='center',
                va='center'
                )
        # Kreska w stylu |-|
        par1.annotate(
                     '',
                     xy=(-0.145299 + 0.15, 320+2),
                     xytext=(-0.1293 + 0.15, 320+2),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='|-|, widthB=0.4,widthA=0.4',
                                    ),
                     horizontalalignment='right'
                    )
        # 0.15 - przesunięcie danych do zera
        # faza napięcia w chwili załączenia
        xcenter = -0.145299 + 0.15 + (0.145299 - 0.1293)/2
        fi = 360 - (0.145299 - 0.1293)/0.02*360
        par1.annotate(
            r"$\phi_{pocz} $"+"="+str(round(fi, 3))+r"$^\circ$",
            xy=(xcenter, 320+10),
            ha='center',
            va='center'
            )
        # określenie czasu początkowego
        x_tp = -0.14561 + 0.15
        x_tk = (-1/coefficent[2])*4
        x_cen = x_tp + (x_tk-x_tp)/2
        y_t = - 320
        par1.set_ylim(-350, 350)
        par1.annotate(
                     '',
                     xy=(x_tp, y_t),
                     xytext=(x_tk, y_t),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='|-|, widthB=0.4,widthA=0.4',
                                    ),
                     horizontalalignment='right'
                    )
        par1.annotate(
                r"$t_{nieustalone} $"+"="+str(round((x_tk-x_tp), 3))+'s',
                xy=(x_cen, y_t-10),
                ha='center',
                va='center'
                      )
        # stała czasowa
        par1.annotate(
                     '',
                     xy=(self.local_max[0][0], -200),
                     xytext=((self.local_max[0][0]-1/coefficent[2]), -200),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='|-|, widthB=0.4,widthA=0.4',
                                    ),
                     horizontalalignment='right'
                    )
        tcen = self.local_max[0][0] + (-1/coefficent[2])/2
        par1.annotate(
                r"$T_{0} $"+"="+str(round((-1/coefficent[2]), 3))+'s',
                xy=(tcen, -200+6),
                ha='center',
                va='center'
                      )

        plt.show()


c = Plots()
c.reciving_data()
c.plot()
