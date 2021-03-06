#!/usr/bin/env python
import data_analysis
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import numpy as np
import csv


class Plots(data_analysis.Data):
    def plot_armature_current(self):
        # wczytanie odpowiednich zakresów danych
        y_current_armature = self.current_armature[500:3500].copy()
        x_time = self.time[500:3500].copy()

        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_current_armature, label=r"$I_{a}(t)$")
        ax.set_title('Prąd Twornika')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("I [A]")
        lines = [line1]
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
        # rysowanie kres|
        ax.annotate(
                     '',
                     xy=(xmax, ymax),
                     # jeśli jest zadługa kreska - zmiana mianownik w xytext
                     xytext=(xmax-((abs(x_time[0])+abs(x_time[len(x_time)-1]))/18), ymax),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś - zmiana mianownika def plot(self):
        xcenter = xmax-(abs(x_time[0])+abs(x_time[len(x_time)-1]))/7.5
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$I_{a}$' + '= '+str(round(abs(ymax), 1))+'A',
                xy=(xcenter+0.2, ymax+10),
                ha='center',
                va='center'
                )
        plt.show()

    def plot_armature_voltage(self):
        # wczytanie odpowiednich zakresów danych
        y_armature_voltage = self.voltage_armature[:1250].copy()
        x_time = self.time[:1250].copy()
        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_armature_voltage, label="U(t)", color='maroon')
        ax.set_title('Napięcie pomiędzy systemem, a generatorem')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("U [V]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])

        # wyznaczanie maksymalnej wartości prądu maksymalnego
        max_check = [abs(x) for x in y_armature_voltage[971:]]
        ymax = max(max_check)
        # sprawdzenie po której stronie zera jest największa wartość
        try:
            xpos = y_armature_voltage.index(ymax)
        except:
            ymax = -ymax
            xpos = y_armature_voltage.index(ymax)
        xmax = x_time[xpos]
        # rysowanie kres|
        ax.annotate(
                     '',
                     xy=(xmax, ymax),
                     # jeśli jest zadługa kreska - zmiana mianownik w xytext
                     xytext=(xmax-((abs(x_time[0])+abs(x_time[len(x_time)-1]))/15), ymax),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś - zmiana mianownika def plot(self):
        xcenter = xmax-(abs(x_time[0])+abs(x_time[len(x_time)-1]))/27
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$U_{zał}$' + '= '+str(round(abs(ymax), 1))+'V',
                xy=(xcenter, ymax+20),
                ha='center',
                va='center'
                )   

        plt.show()

    def plot_exciting_current(self):
        # wczytanie odpowiednich zakresów danych
        y_exciting_current = self.current_exciting[500:3500].copy()
        x_time = self.time[500:3500].copy()

        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_exciting_current, label="I(t)", color='darkslategrey')
        ax.set_title('Prąd wzbudzenia')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("I [A]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])

        # wyznaczanie maksymalnej wartości prądu maksymalnego
        ymax = max(y_exciting_current)
        xmax = x_time[y_exciting_current.index(ymax)]
        max_index = y_exciting_current.index(ymax)
        # rysowanie kres|
        ax.annotate(
                     '',
                     xy=(xmax, ymax),
                     # jeśli jest zadługa kreska - zmiana mianownik w xytext
                     xytext=(xmax-((abs(x_time[0])+abs(x_time[len(x_time)-1]))/20), ymax),
                     arrowprops=dict(
                                        facecolor='black',
                                        arrowstyle='-',

                                    ),
                     horizontalalignment='right'
                    )
        # jeśli tekst wysuwa się za oś - zmiana mianownika def plot(self):
        xcenter = xmax-(abs(x_time[0])+abs(x_time[len(x_time)-1]))/35
        # dodawanie tekstu nad kreską
        ax.annotate(
                r'$I_{f}$' + '= '+str(round(abs(ymax), 2))+'A',
                xy=(xcenter, ymax+0.2),
                ha='center',
                va='center'
                )
        plt.ylim(bottom=-5.7)
        # określenie czasu rozruchu
        x_tp = 0.52
        x_tk = x_tp + (1.62-0.52)/12
        x_cen = x_tp + (x_tk-x_tp)/2
        y_t = -5
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
                r"$T_{oscylacji} $"+"= "+str(round((1.62/12), 2))+' s',
                xy=(x_cen, y_t-0.5),
                ha='center',
                va='center'
                      )

        plt.show()
