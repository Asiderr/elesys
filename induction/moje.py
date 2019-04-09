#!/usr/bin/env python
import plots_moje

c = plots_moje.Plots()
c.reciving_data('moje_dane.csv')
c.plot_stator_current()
c.plot_freq_rotor_cur()
c.plot_RPM()
c.plot_stator_voltage()
c.plot_rotor_current()
c.plot_wybieg()