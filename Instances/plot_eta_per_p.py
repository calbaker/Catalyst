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

cat_opt = catalyst.Catalyst()
cat_opt.terms = 4
cat_opt.Vdot = 500e-6 / 60.
cat_opt.T = 400. + 273.15

terms = np.arange(1, cat_opt.terms)

eta_ij = np.zeros([T_array.size, cat_opt.terms])

for i in range(terms.size):
    print "solving for", terms[i], "terms"
    cat_opt.terms = terms[i]
    cat_opt.set_eta_ij()
    eta_ij[:, i] = cat_opt.eta_ij

print "solving numerical model"
cat_opt.y_array = np.linspace(0, 1, 100)
cat_opt.set_eta_ij_num()


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

for i in range(terms.size):
    if i % 2 == 0:
        LABEL = str(terms[i]) + ' terms'
    else:
        LABEL = None
    plt.plot(T_array - 273.15, eta_ij[:, i] * 100., label=LABEL)
plt.plot(T_array - 273.15, cat_opt.eta_ij_num[0, :] * 100., '--k',
    label='numerical')

np.savetxt('../output/plot_eta_v_terms/eta_ij', eta_ij)
np.savetxt('../output/plot_eta_v_terms/eta_ij_num', cat_opt.eta_ij_num)
np.savetxt('../output/plot_eta_v_terms/T_array', T_array)

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
# plt.ylim(ymax=37)
# plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig(
    '../Plots/plot_eta_v_terms/Fo convergence' + str(Vdot * 60e6) + '.pdf')
plt.savefig(
    '../Plots/plot_eta_v_terms/Fo convergence' + str(Vdot * 60e6) + '.png')

paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'

plt.savefig(paper_dir + 'Fo_convergence.pdf')

plt.show()
