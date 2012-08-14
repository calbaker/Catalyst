"""Module for plotting results of first term model with experimental
data and fitting capability."""

import matplotlib.pyplot as plt
import os
import sys

cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import catalyst 
reload(catalyst)

data250 = catalyst.Catalyst()
data250.source = (
    '../data/250sccm 10nmPtPd VariedT rep2.xls'
    )
data250.import_data()
data250.Vdot = 250. * 1.e-6 / 60.
A_arr = 10.e6
T_a = 7.2e3
data250.A_arr = A_arr
data250.T_a = T_a
data250.set_fit_params()

data500 = catalyst.Catalyst()
data500.source = (
    '../data/500sccm 10nmPtPd VariedT rep2.xls'
    )
data500.import_data()
data500.T_a = data250.T_a
data500.A_arr = data250.A_arr
data500.Vdot = 500. * 1.e-6 / 60.
data500.set_eta_ij()

data750 = catalyst.Catalyst()
data750.source = (
    '../data/750sccm 10nmPtPd VariedT rep2.xls'
    )
data750.import_data()
data750.T_a = data250.T_a
data750.A_arr = data250.A_arr
data750.Vdot = 750. * 1.e-6 / 60.
data750.set_eta_ij()

data1000 = catalyst.Catalyst()
data1000.source = (
    '../data/1000sccm 10nmPtPd VariedT rep2.xls'
    )
data1000.import_data()
data1000.T_a = data250.T_a
data1000.A_arr = data250.A_arr
data1000.Vdot = 1000. * 1.e-6 / 60.
data1000.set_eta_ij()

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE 
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

plt.close()

plt.figure()

plt.plot(data250.T_exp, data250.eta_exp * 100., 'sr', linestyle='',
         label='250sccm exp')
plt.plot(data250.T_array, data250.eta_ij.T * 100., '-r',
         label='250sccm model')

plt.plot(data500.T_exp, data500.eta_exp * 100., 'og', linestyle='',
         label='500sccm exp')
plt.plot(data500.T_array, data500.eta_ij.T * 100., '-g',
         label='500sccm model')

plt.plot(data750.T_exp, data750.eta_exp * 100., 'v', linestyle='',
         label='750sccm exp')
plt.plot(data750.T_array, data750.eta_ij.T * 100., '-b',
         label='750sccm model')

plt.plot(data1000.T_exp, data1000.eta_exp * 100., '*m', linestyle='',
         label='1000sccm exp')
plt.plot(data1000.T_array, data1000.eta_ij.T * 100., '-m',
         label='1000sccm model')

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
plt.ylim(ymax=37)
# plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig('../Plots/4model and exp.pdf')
plt.savefig('../Plots/4model and exp.png')

plt.show()
