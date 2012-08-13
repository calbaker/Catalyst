"""Generates plot of hydrocarbon conversion efficiency versus temperature comparing
performance of catalyst with control experiment.  This plot is used in paper.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import catalyst 
reload(catalyst)

plt.close('all')

A_arr = 1.129e7
T_a = 6822.

cat = catalyst.Catalyst()
cat.source = '../data/750sccm 10nmPtPd VariedT rep2.xls'
cat.A_arr = A_arr
cat.T_a = T_a
cat.Vdot = 750. * 1.e-6 / 60.
cat.Vdot_array = np.array([cat.Vdot])

cat.import_data()

cat.set_eta_ij()

cat_empty = catalyst.Catalyst()
# cat_empty.source = 'alumina_holder_only.xls' # this data needs to be
# cleared with Hall and Ezekoye
cat_empty.source = '../data/1000sccm empty tube rep2.xls'
cat_empty.A_arr = A_arr
cat_empty.T_a = T_a
cat_empty.Vdot = 1000. * 1.e-6 / 60. 
cat_empty.Vdot_array = np.array([cat_empty.Vdot])

cat_empty.import_data()

cat_empty.set_eta_ij()

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE 
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

plt.figure()

plt.plot(cat.T_exp, cat.eta_exp * 100., 'sr', linestyle='',
         label='750sccm exp')
plt.plot(cat.T_array, cat.eta_ij.T * 100., '-r',
         label='750sccm model')

plt.plot(cat_empty.T_exp, cat_empty.eta_exp * 100., 'om', linestyle='',
         label='1000sccm control')

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
plt.ylim(ymax=40)
plt.xlim(xmax=700)
# plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig('../Plots/high_temp_bad.pdf')
plt.savefig('../Plots/high_temp_bad.png')

plt.show()
