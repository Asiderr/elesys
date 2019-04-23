#!/usr/bin/env python
import plots_moje

c = plots_moje.Plots()
c.reciving_data('Norbert.csv')
c.plot_armature_current()
c.plot_armature_voltage()
c.plot_exciting_current()
