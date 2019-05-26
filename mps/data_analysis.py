#!/usr/bin/env python

import pandas as pd
import scipy.optimize as opt
import numpy as np
from math import pi


class Data:
    def reciving_data(self, name):
        # przekładnie lemow
        coef_armature_current = 494.4/5
        coef_exciting_current = 5.78
        coef_armature_voltage = 71.7
        data = pd.read_csv(name, encoding='utf-8')
        # umieszczenie danych w listach
        self.current_armature = [-1*x*coef_armature_current for x in data['Ch 02`V'].tolist()]
        self.current_exciting = [-1*x*coef_exciting_current for x in data['Ch 01`V'].tolist()]
        self.voltage_armature = [-1*x*coef_armature_voltage for x in data['Ch 00`V'].tolist()]
        self.time = data['t`s'].tolist()
        self.data_calculations()

    def data_calculations(self):
        # wyliczenie momentu elektromagnetycznego i prądkości obrotowej
        rotation_induction = 1.57
        armature_resistance = 0.55
        self.tork = [
            rotation_induction*self.current_armature[i]*v
            for i, v in enumerate(self.current_exciting)
        ]
        self.velocity = [
            ((self.voltage_armature[i] - armature_resistance*self.current_armature[i]) /
             (rotation_induction*v))*30/pi
            for i, v in enumerate(self.current_exciting)
        ]

    def time_constatant_electrical(self, data):
        for i, v in enumerate(data):
            if i is 0:
                pass
            else:
                if v > 1 and data[i-1] < 1:
                    self.zero_time = self.time[i]

        self.max_time = data.index(max(data))

    def expot(self, x, a, b):
            return a*x + b

    def regresion(self, local_max):
        x = []
        y = []
        for i in local_max:
            x.append(i[0])
            y.append(i[1])
        x_np = np.array(x)
        y_np = np.array(y)
        popt, pcov = opt.curve_fit(self.expot, x_np, y_np)
        self.result = popt
        # druga wersja wyznaczania krzywej expotencjalnej
        # self.result = opt.curve_fit(lambda t,a,b: (a*np.exp(b*t)), x_np, y_np, p0=(1, 5))
