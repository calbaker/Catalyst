"""Module for plotting results of first term model with experimental
data and fitting capability."""

import matplotlib.pyplot as plt
import os
import sys
import numpy as np

cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import catalyst 
reload(catalyst)

T_model = np.linspace(250, 450, 50) + 273.15

print "running data250"

data250 = catalyst.Catalyst()
data250.source = (
    '../data/250sccm 10nmPtPd VariedT rep2.xls'
    )
data250.import_data()
data250.Vdot = 250. * 1.e-6 / 60.
data250.set_fit_params()
data250.T_model = T_model
data250.set_eta_ij()
A_arr = data250.A_arr
T_a = data250.T_a

np.savetxt('../output/calibrate/data250.T_exp', data250.T_exp)
np.savetxt('../output/calibrate/data250.T_array', data250.T_array)
np.savetxt('../output/calibrate/data250.eta_ij', data250.eta_ij)
np.savetxt('../output/calibrate/data250.eta_exp', data250.eta_exp)

print "running data500"

data500 = catalyst.Catalyst()
data500.source = (
    '../data/500sccm 10nmPtPd VariedT rep2.xls'
    )
data500.import_data()
data500.T_model = T_model
data500.T_a = data250.T_a
data500.A_arr = data250.A_arr
data500.Vdot = 500. * 1.e-6 / 60.
data500.set_eta_ij()

np.savetxt('../output/calibrate/data500.T_exp', data500.T_exp)
np.savetxt('../output/calibrate/data500.T_array', data500.T_array)
np.savetxt('../output/calibrate/data500.eta_ij', data500.eta_ij)
np.savetxt('../output/calibrate/data500.eta_exp', data500.eta_exp)

print "running data750"

data750 = catalyst.Catalyst()
data750.source = (
    '../data/750sccm 10nmPtPd VariedT rep2.xls'
    )
data750.import_data()
data750.T_model = T_model
data750.T_a = data250.T_a
data750.A_arr = data250.A_arr
data750.Vdot = 750. * 1.e-6 / 60.
data750.set_eta_ij()

np.savetxt('../output/calibrate/data750.T_exp', data750.T_exp)
np.savetxt('../output/calibrate/data750.T_array', data750.T_array)
np.savetxt('../output/calibrate/data750.eta_ij', data750.eta_ij)
np.savetxt('../output/calibrate/data750.eta_exp', data250.eta_exp)

print "running data1000"

data1000 = catalyst.Catalyst()
data1000.source = (
    '../data/1000sccm 10nmPtPd VariedT rep2.xls'
    )
data1000.import_data()
data1000.T_model = T_model
data1000.T_a = data250.T_a
data1000.A_arr = data250.A_arr
data1000.Vdot = 1000. * 1.e-6 / 60.
data1000.set_eta_ij()

np.savetxt('../output/calibrate/data1000.T_exp', data1000.T_exp)
np.savetxt('../output/calibrate/data1000.T_array', data1000.T_array)
np.savetxt('../output/calibrate/data1000.eta_ij', data1000.eta_ij)
np.savetxt('../output/calibrate/data1000.eta_exp', data1000.eta_exp)

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

fig1 = plt.figure()

plt.plot(data250.T_exp - 273.15, data250.eta_exp * 100., 'sr', linestyle='',
         label='250sccm exp')
plt.plot(data250.T_array - 273.15, data250.eta_ij.T * 100., '-r',
         label='250sccm model')

plt.plot(data500.T_exp - 273.15, data500.eta_exp * 100., 'og', linestyle='',
         label='500sccm exp')
plt.plot(data500.T_array - 273.15, data500.eta_ij.T * 100., '-g',
         label='500sccm model')

plt.plot(data750.T_exp - 273.15, data750.eta_exp * 100., 'v', linestyle='',
         label='750sccm exp')
plt.plot(data750.T_array - 273.15, data750.eta_ij.T * 100., '-b',
         label='750sccm model')

plt.plot(data1000.T_exp - 273.15, data1000.eta_exp * 100., '*m', linestyle='',
         label='1000sccm exp')
plt.plot(data1000.T_array - 273.15, data1000.eta_ij.T * 100., '-m',
         label='1000sccm model')

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
plt.ylim(ymax=45)
# plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()

fig1.savefig('../Plots/calibrate/4model and exp.pdf')
fig1.savefig('../Plots/calibrate/4model and exp.png')

plt.show()

