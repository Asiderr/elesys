#!/usr/bin/env python

import pandas as pd
import scipy.optimize as opt
import numpy as np


class Data:
    def reciving_data(self, name):
        # przekładnie lemow
        coef_armature_current = 494.4/5
        coef_exciting_current = 30.3
        coef_armature_voltage = 179.33
        data = pd.read_csv(name, encoding='utf-8')
        # umieszczenie danych w listach
        self.current_armature = [x*coef_armature_current for x in data['Ch 02`V'].tolist()]
        self.current_exciting = [x*coef_exciting_current for x in data['Ch 01`V'].tolist()]
        self.voltage_armature = [x*coef_armature_voltage for x in data['Ch 00`V'].tolist()]
        self.time = data['t`s'].tolist()

    def plus_n_minus(self, sample_list):
        self.plus = []
        self.minus = []
        for sample in sample_list:
            if sample[1] > 0:
                self.plus.append(sample)
                self.minus.append([sample[0], 0])
            else:
                self.plus.append([sample[0], 0])
                self.minus.append(sample)
    
    def check_local_maxes(self, sample_list):
        self.local_max = []
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
                if abs_sample_val < 1 and abs(sample_before[1]) > 1:
                    self.local_max.append([max_val_x, max_val])
                    max_val = 0

    def determination_of_local_max(self, sample_list):
        self.plus_n_minus(sample_list)
        self.check_local_maxes(self.minus)
        self.minus_local_max = self.local_max.copy()
        self.check_local_maxes(self.plus)
        self.plus_local_max = self.local_max.copy()        
    
    def expot(self, x, a, b, c):
            return a * np.exp(b * x) + c

    def regresion(self, local_max, max_range):
        x = []
        y = []
        for i in local_max:
            x.append(i[0])
            y.append(i[1])
        x_np = np.array(x[:max_range])
        y_np = np.array(y[:max_range])
        popt, pcov = opt.curve_fit(self.expot, x_np, y_np)
        self.result = popt
        # druga wersja wyznaczania krzywej expotencjalnej
        # self.result = opt.curve_fit(lambda t,a,b: (a*np.exp(b*t)), x_np, y_np, p0=(1, 5))
