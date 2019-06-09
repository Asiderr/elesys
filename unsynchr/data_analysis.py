#!/usr/bin/env python

import pandas as pd
import scipy.optimize as opt
import numpy as np
from math import pi


class Data:
    def reciving_data(self, name):
        # przekładnie lemow
        coef_armature_current = 495.38
        coef_exciting_current = 21.74
        coef_armature_voltage = 156.16
        data = pd.read_csv(name, encoding='utf-8')
        # umieszczenie danych w listach
        self.current_armature = [x*coef_armature_current for x in data['Ch 02`V'].tolist()]
        self.current_exciting = [x*coef_exciting_current for x in data['Ch 01`V'].tolist()]
        self.voltage_armature = [x*coef_armature_voltage for x in data['Ch 00`V'].tolist()]
        self.time = data['t`s'].tolist()
