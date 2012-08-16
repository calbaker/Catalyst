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

cat_terms = catalyst.Catalyst()
cat_terms.terms = 10
terms = cat_terms.terms
cat_terms.Vdot = Vdot
cat_terms.T_array = T_array

eta_ij = np.zeros([T_array.size, cat_terms.terms])

for i in range(terms):
    print "solving for", i + 1, "terms"
    cat_terms.terms = i + 1
    cat_terms.set_eta_ij()
    eta_ij[:, i] = cat_terms.eta_ij

print "solving numerical model"
cat_terms.y_array = np.linspace(0, 1, 100)
cat_terms.set_eta_ij_num()

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

for i in range(terms):
    if i % 2 == 0:
        LABEL = str(i + 1) + ' terms'
    else:
        LABEL = None
    plt.plot(T_array - 273.15, eta_ij[:, i] * 100., label=LABEL)
plt.plot(T_array - 273.15, cat_terms.eta_ij_num[0, :] * 100., '--k',
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
