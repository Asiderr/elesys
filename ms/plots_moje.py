#!/usr/bin/env python
import data_analysis
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import numpy as np


class Plots(data_analysis.Data):
    def plot_armature_current(self):
        # wczytanie odpowiednich zakresów danych
        y_current_armature = self.current_armature[1000:3000].copy()
        x_time = self.time[1000:3000].copy()
        # przeliczenie czasu do 0
        time_const = x_time[0]
        x_time = [x-time_const for x in x_time]

        # określenie stałej czasowej wykresu
        sample_list = [[x_time[i], y] for i, y in enumerate(y_current_armature)]
        self.determination_of_local_max(sample_list)
        self.regresion(self.plus_local_max, 6)
        coefficent_plus_start = self.result
        x_exp_plus_start = np.arange(self.plus_local_max[0][0], self.plus_local_max[1][0], 0.001)
        y_exp_plus_start = np.array([coefficent_plus_start[0]*math.exp(coefficent_plus_start[1]*i)+coefficent_plus_start[2]-3 for i in x_exp_plus_start])
        self.regresion(self.plus_local_max[1:], 1000)
        coefficent_plus_end = self.result
        x_exp_plus_end = np.arange(self.plus_local_max[1][0], (-1/coefficent_plus_end[1])*9, 0.001)
        y_exp_plus_end = np.array([coefficent_plus_end[0]*math.exp(coefficent_plus_end[1]*i)+coefficent_plus_end[2] for i in x_exp_plus_end])
        x_exp_plus = np.append(x_exp_plus_start, x_exp_plus_end)
        y_exp_plus = np.append(y_exp_plus_start, y_exp_plus_end)
        self.regresion(self.minus_local_max[1:], 1000)
        coefficent_minus = self.result
        x_exp_minus = np.arange(self.minus_local_max[1][0], (-1/coefficent_minus[1])*7, 0.001)
        y_exp_minus = np.array([coefficent_minus[0]*math.exp(coefficent_minus[1]*i)+coefficent_minus[2] for i in x_exp_minus])
        self.coef = coefficent_minus[1]
        
        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_current_armature, label=r"$I_{a}(t)$")
        line2, = ax.plot(
            x_exp_minus,
            y_exp_minus,
            label="y(t) = " + str(round(coefficent_minus[0], 2)) +
            " *e" + r'$^{%.2f *t}$' % (round(coefficent_minus[1], 2))
            )
        line3, = ax.plot(
            x_exp_plus,
            y_exp_plus,
            label="y(t) = " + str(round(coefficent_plus_end[0], 2)) +
            " *e" + r'$^{%.2f *t}$' % (round(coefficent_plus_end[1], 2))
            )
        ax.set_title('Prąd Twornika')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("I [A]")
        lines = [line1, line2, line3]
        ax.legend(lines, [l.get_label() for l in lines])
        
        # wyznaczanie maksymalnej wartości prądu maksymalnego
        max_check = [abs(x) for x in y_current_armature]
        ymax = max(max_check)
        # sprawdzenie po której stronie zera jest największa wartość
        try:
            xpos = y_current_armature.index(ymax)
        except:
            ymax = -ymax
            xpos = y_current_armature.index(ymax)
        xmax = x_time[xpos]
        ax.set_ylim(-100, 150)
        # rysowanie kres|
        ax.annotate(
                     '',
                     xy=(xmax, ymax),
                     # jeśli jest zadługa kreska - zmiana mianownik w xytext
                     xytext=(xmax-((abs(x_time[0])+abs(x_time[len(x_time)-1]))/13), ymax),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś - zmiana mianownika def plot(self):
        xcenter = xmax-(abs(x_time[0])+abs(x_time[len(x_time)-1]))/30
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$I_{a}$' + '= '+str(round(abs(ymax), 1))+'A',
                xy=(xcenter-0.005, ymax+5),
                ha='center',
                va='center'
                )
        
        # wyznaczenie stabilnej wartości prądu
        ymax = -coefficent_minus[2]+0.1
        xmax = 0.3529
        ax.annotate(
                     '',
                     xy=(xmax, ymax+1),
                     # jeśli jest zadługa kreska - zmiana mianownik w xytext
                     xytext=(xmax+((abs(x_time[0])+abs(x_time[len(x_time)-1]))/10), ymax+1),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś - zmiana mianownika def plot(self):
        xcenter = xmax+(abs(x_time[0])+abs(x_time[len(x_time)-1]))/30
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$I_{ustalone}$' + '= '+str(round(abs(ymax), 2))+'A',
                xy=(xcenter+0.005, ymax+5),
                ha='center',
                va='center'
                )

        # określenie czasu początkowego
        x_tp = 0.0603
        x_tk = x_tp + -1/coefficent_minus[1]*4
        x_cen = x_tp + (x_tk-x_tp)/2
        y_t = -80
        ax.annotate(
                     '',
                     xy=(x_tp, y_t),
                     xytext=(x_tk, y_t),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='|-|, widthB=0.4,widthA=0.4',
                                    ),
                     horizontalalignment='right'
                    )
        ax.annotate(
                r"$t_{rozruchu} $"+"="+str(round((-1/coefficent_minus[1]*4), 3))+'s',
                xy=(x_cen, y_t+10),
                ha='center',
                va='center'
                      )
        plt.show()

    def plot_armature_voltage(self):
        # wczytanie odpowiednich zakresów danych
        y_armature_voltage = self.voltage_armature[1000:3000].copy()
        x_time = self.time[1000:3000].copy()
        # przeliczenie czasu do 0
        time_const = x_time[0]
        x_time = [x-time_const for x in x_time]

        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_armature_voltage, label="U(t)", color='maroon')
        ax.set_title('Napięcie Twornika')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("U [V]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])
        # wyznaczanie maksymalnej wartości prądu maksymalnego
        max_check = [abs(x) for x in y_armature_voltage]
        ymax = max(max_check)
        # sprawdzenie po której stronie zera jest największa wartość
        try:
            xpos = y_armature_voltage.index(ymax)
        except:
            ymax = -ymax
            xpos = y_armature_voltage.index(ymax)
        xmax = x_time[xpos]
        ax.set_ylim(-350, 350)
        # rysowanie kres|
        ax.annotate(
                     '',
                     xy=(xmax, ymax),
                     # jeśli jest zadługa kreska - zmiana mianownik w xytext
                     xytext=(xmax-((abs(x_time[0])+abs(x_time[len(x_time)-1]))/13), ymax),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś - zmiana mianownika def plot(self):
        xcenter = xmax-(abs(x_time[0])+abs(x_time[len(x_time)-1]))/30
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$U_{a}$' + '= '+str(round(abs(ymax), 1))+'V',
                xy=(xcenter-0.005, ymax+15),
                ha='center',
                va='center'
                )
        
        # wyznaczenie stabilnej wartości prądu
        ymax = 55
        xmax = 0.3529
        ax.annotate(
                     '',
                     xy=(xmax, ymax+1),
                     # jeśli jest zadługa kreska - zmiana mianownik w xytext
                     xytext=(xmax+((abs(x_time[0])+abs(x_time[len(x_time)-1]))/10), ymax+1),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś - zmiana mianownika def plot(self):
        xcenter = xmax+(abs(x_time[0])+abs(x_time[len(x_time)-1]))/30
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$U_{ustalone}$' + '= '+str(round(abs(ymax), 2))+'V',
                xy=(xcenter+0.005, ymax+15),
                ha='center',
                va='center'
                )

        # określenie czasu początkowego
        x_tp = 0.0603
        x_tk = x_tp + -1/self.coef*4
        x_cen = x_tp + (x_tk-x_tp)/2
        y_t = -170
        ax.annotate(
                     '',
                     xy=(x_tp, y_t),
                     xytext=(x_tk, y_t),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='|-|, widthB=0.4,widthA=0.4',
                                    ),
                     horizontalalignment='right'
                    )
        ax.annotate(
                r"$t_{rozruchu} $"+"="+str(round((-1/self.coef*4), 3))+'s',
                xy=(x_cen, y_t+10),
                ha='center',
                va='center'
                      )
        plt.show()

    def plot_exciting_current(self):
        # wczytanie odpowiednich zakresów danych
        y_exciting_current = self.current_exciting[1000:3000].copy()
        x_time = self.time[1000:3000].copy()
        # przeliczenie czasu do 0
        time_const = x_time[0]
        x_time = [x-time_const for x in x_time]

        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_exciting_current, label="I(t)", color='darkslategrey')
        ax.set_title('Prąd wzbudzenia')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("I [A]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])
        # wyznaczanie maksymalnej wartości prądu maksymalnego
        max_check = [abs(x) for x in y_exciting_current]
        ymax = max(max_check)
        # sprawdzenie po której stronie zera jest największa wartość
        try:
            xpos = y_exciting_current.index(ymax)
        except:
            ymax = -ymax
            xpos = y_exciting_current.index(ymax)
        xmax = x_time[xpos]
        ax.set_ylim(-25, 75)
        # rysowanie kres|
        ax.annotate(
                     '',
                     xy=(xmax, ymax),
                     # jeśli jest zadługa kreska - zmiana mianownik w xytext
                     xytext=(xmax-((abs(x_time[0])+abs(x_time[len(x_time)-1]))/13), ymax),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś - zmiana mianownika def plot(self):
        xcenter = xmax-(abs(x_time[0])+abs(x_time[len(x_time)-1]))/30
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$I_{f}$' + '= '+str(round(abs(ymax), 2))+'A',
                xy=(xcenter-0.005, ymax+2),
                ha='center',
                va='center'
                )
        
        # wyznaczenie stabilnej wartości prądu
        ymax = 8
        xmax = 0.4
        ax.annotate(
                     '',
                     xy=(xmax, ymax+1),
                     # jeśli jest zadługa kreska - zmiana mianownik w xytext
                     xytext=(xmax+((abs(x_time[0])+abs(x_time[len(x_time)-1]))/10), ymax+1),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś - zmiana mianownika def plot(self):
        xcenter = xmax+(abs(x_time[0])+abs(x_time[len(x_time)-1]))/30
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$I_{ustalone}$' + '= '+str(round(abs(ymax), 2))+'A',
                xy=(xcenter+0.005, ymax+3),
                ha='center',
                va='center'
                )

        plt.show()
