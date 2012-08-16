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

Vdot = 500.e-6 / 60.
T_array = np.linspace(200, 500, 25) + 273.15

cat_num_test = catalyst.Catalyst()
cat_num_test.terms = 10
terms = cat_num_test.terms
cat_num_test.Vdot = Vdot
cat_num_test.T_array = T_array

print "solving numerical model"
cat_num_test.y_array = np.linspace(0, 1, 100)
cat_num_test.set_eta_ij_num()

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

plt.plot(T_array - 273.15, cat_num_test.eta_ij_num[0, :] * 100., '--k',
    label='numerical')

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
# plt.ylim(ymax=37)
# plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig('../Plots/Fo convergence' + str(Vdot * 60e6) + '.pdf')
plt.savefig('../Plots/Fo convergence' + str(Vdot * 60e6) + '.png')

plt.show()
