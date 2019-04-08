#!/usr/bin/env python

import pandas as pd
import scipy.optimize as opt
import numpy as np


class Data:
    def reciving_data(self, name):
        # przekładnie lemow
        coef_stator_cur = 23.81
        coef_stator_voltage = 325.71
        coef_rotor_current = 494.4/5
        coef_tachometer = 59.8
        data = pd.read_csv(name, encoding='utf-8')
        # umieszczenie danych w listach
        self.current_stator = [x*coef_stator_cur for x in data['Ch 00`V'].tolist()]
        self.current_rotor = [x*coef_rotor_current for x in data['Ch 01`V'].tolist()]
        tachometer_volt = [x*coef_tachometer for x in data['Ch 02`V'].tolist()]
        min_tach = min(tachometer_volt)
        max_tach = max(tachometer_volt)
        self.tachometer = [(x-min_tach)*950/max_tach for x in tachometer_volt]
        self.voltage_stator = [x*coef_stator_voltage for x in data['Ch 03`V'].tolist()]
        self.time = data['t`s'].tolist()
        self.freq = [(950-x)*50/950 for x in self.tachometer]
