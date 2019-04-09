#!/usr/bin/env python
import data_analysis
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


class Plots(data_analysis.Data):
    def plot_stator_current(self):
        # wczytanie odpowiednich zakresów danych
        y_current_stator = self.current_stator[200:2500].copy()
        x_time = self.time[200:2500].copy()
        time_const = x_time[0]
        x_time = [x-time_const for x in x_time]

        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_current_stator, label="i(t)")
        ax.set_title('Prąd Stojana')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("I [A]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])
        # wyznaczanie maksymalnej wartości prądu maksymalnego
        max_check = [abs(x) for x in y_current_stator]
        ymax = max(max_check)
        try:
            xpos = y_current_stator.index(ymax)
        except:
            ymax = -ymax
            xpos = y_current_stator.index(ymax)
        xmax = x_time[xpos]
        ax.set_ylim(-150, 150)
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
                r'$I_{stojana}$' + '= '+str(round(abs(ymax), 1))+'A',
                xy=(xcenter-0.005, ymax+3),
                ha='center',
                va='center'
                )

        # określenie czasu początkowego
        x_tp = 0.131 - time_const
        x_tk = 0.489 - time_const
        x_cen = x_tp + (x_tk-x_tp)/2
        y_t = 100
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
                r"$t_{rozruchu} $"+"="+str(round((x_tk-x_tp), 3))+'s',
                xy=(x_cen, y_t+10),
                ha='center',
                va='center'
                      )
        plt.show()

    def plot_stator_voltage(self):
        y_voltage_stator = self.voltage_stator[200:2500].copy()
        x_time = self.time[200:2500].copy()
        time_const = x_time[0]
        x_time = [x-time_const for x in x_time]

        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_voltage_stator, label="U(t)", color='maroon')
        ax.set_title('Napięcie Stojana')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("U [V]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])
        plt.show()

    def plot_rotor_current(self):
        y_current_rotor = self.current_rotor[200:2500].copy()
        x_time = self.time[200:2500].copy()
        time_const = x_time[0]
        x_time = [x-time_const for x in x_time]

        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_current_rotor, label="i(t)", color="g")
        ax.set_title('Prąd Wirnika')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("I [A]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])

        # wyznaczanie maksymalnej wartości prądu maksymalnego
        max_check = [abs(x) for x in y_current_rotor]
        ymax = max(max_check)
        try:
            xpos = y_current_rotor.index(ymax)
        except:
            ymax = -ymax
            xpos = y_current_rotor.index(ymax)
        xpos = y_current_rotor.index(ymax)
        xmax = x_time[xpos]
        # ax.set_ylim(-150, 150)
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
                r'$I_{wirnika}$' + '= '+str(round(abs(ymax), 1))+'A',
                xy=(xcenter-0.005, ymax+6),
                ha='center',
                va='center'
                )
        plt.show()

    def plot_RPM(self):
        y_tachometer = self.tachometer[200:2500].copy()
        x_time = self.time[200:2500].copy()
        time_const = x_time[0]
        x_time = [x-time_const for x in x_time]

        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_tachometer, label="n(t)", color="cadetblue")
        ax.set_title('Prędkość wirnika')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("n [obr/min]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])
        # określenie czasu początkowego
        x_tp = 0.141 - time_const
        x_tk = 0.499 - time_const
        x_cen = x_tp + (x_tk-x_tp)/2
        y_t = 1000
        ax.set_ylim(-10, 1050)

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
                r"$t_{rozruchu} $"+"="+str(round((x_tk-x_tp), 3))+'s',
                xy=(x_cen, y_t+20),
                ha='center',
                va='center'
                      )
        plt.show()

    def plot_freq_rotor_cur(self):
        x_time = self.time[200:2500].copy()
        y_freq = self.freq[200:2500].copy()
        time_const = x_time[0]
        x_time = [x-time_const for x in x_time]

        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_freq, label="f(t)", color='mediumslateblue')
        ax.set_title('Częstotliwość prądu wirnika')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("f [Hz]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])
        plt.show()

    def plot_wybieg(self):
        # wczytanie odpowiednich zakresów danych
        self.reciving_data("wybieg.csv")
        x_time = self.time[72000:].copy()
        y_tachometer = self.tachometer[72000:].copy()
        time_const = x_time[0]
        x_time = [x-time_const for x in x_time]
        
        fig, ax = plt.subplots()
        plt.grid(True)
        line1, = ax.plot(x_time, y_tachometer, label="n(t)", color="cadetblue")
        ax.set_title('Prędkość wirnika')
        ax.set_xlabel("t [s]")
        ax.set_ylabel("n [obr/min]")
        lines = [line1, ]
        ax.legend(lines, [l.get_label() for l in lines])
        x_tp = 6.76
        x_tk = 32.25
        x_cen = x_tp + (x_tk-x_tp)/2
        y_t = 1000
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
                r"$t_{wybiegu} $"+"="+str(round((x_tk-x_tp), 3))+'s',
                xy=(x_cen, y_t+30),
                ha='center',
                va='center'
                      )
        plt.show()
