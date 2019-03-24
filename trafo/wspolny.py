#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import csv


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
                self.plot1.append([float(temp[0]), float(temp[1])*(496.52/5)])
                self.plot2.append([float(temp[2]), float(temp[3])*(496.52/5)])
                self.plot3.append([float(temp[4]), float(temp[5])*(71.47)])
                self.plot4.append([float(temp[6]), float(temp[7])*(71.47)])


class Plots(Data):
    def plot(self):
        x = []
        y = []
        y_vol = []
        for samples in self.plot2:
            x.append(samples[0])
            y.append(samples[1])
        for samples in self.plot4:
            y_vol.append(samples[1])
        y = y[700:3200].copy()
        x = x[700:3200].copy()
        y_vol = y_vol[700:3200].copy()
        fig, ax = plt.subplots()
        par1 = ax.twinx()
        plt.grid(True)

        line1, = ax.plot(x, y, label="i(t)")
        line2, = par1.plot(x, y_vol, "r", label="u(t)")
        ax.set_xlabel("t [s]")
        ax.set_ylabel("I [A]")
        par1.set_ylabel("U [V]")
        lines = [line1, line2]
        ax.legend(lines, [l.get_label() for l in lines])
        # wyznaczanie maksymalnej wartości prądu udarowego
        ymax = min(y)
        xpos = y.index(ymax)
        xmax = x[xpos]
        ax.set_ylim(-350, 350)
        # rysowanie kres|
        ax.annotate(
                     '',
                     xy=(xmax, ymax),
                     xytext=(xmax-((abs(x[0])+abs(x[len(x)-1]))/12), ymax),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        xcenter = xmax-(abs(x[0])+abs(x[len(x)-1]))/22.5
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$I_{udar}$' + '= '+str(round(abs(ymax), 3))+'A',
                xy=(xcenter, ymax+(250/40)),
                ha='center',
                va='center'
                )
        par1.annotate(
                     '',
                     xy=(-0.145299, 320+2),
                     xytext=(-0.1293, 320+2),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='|-|, widthB=0.4,widthA=0.4',
                                    ),
                     horizontalalignment='right'
                    )
        xcenter = -0.145299 + (0.145299-0.1293)/2
        fi = 360-(0.145299-0.1293)/0.02*360
        par1.annotate(
            r"$\phi_{pocz} $"+"="+str(round(fi, 3))+r"$^\circ$",
            xy=(xcenter, 320+10),
            ha='center',
            va='center'
            )
        x_tp = -0.14561
        x_tk = 0.0008
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
        plt.show()


c = Plots()
c.reciving_data()
c.plot()
