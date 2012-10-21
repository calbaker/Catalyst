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
cat_opt.T = 400. + 273.15
cat_opt.set_TempPres_dependents(cat_opt.T)

height = cat_opt.height
length = cat_opt.length
Vdot = 500.e-6 / 60. 

height_array = np.linspace(0.1, 5., 25) * height
length_array = (length * height) / height_array
Vdot_array = Vdot * height_array / height

cat_opt.Vdot = Vdot

U = np.zeros(height_array.size)
DeltaP = np.zeros(height_array.size)
Wdot = np.zeros(height_array.size)

eta = np.zeros(height_array.size)
eta_per_p = np.zeros(height_array.size)
eta_per_Wdot = np.zeros(height_array.size)

for i in range(height_array.size):
    cat_opt.height = height_array[i]
    cat_opt.Vdot = Vdot_array[i]
    cat_opt.x_ = cat_opt.length / cat_opt.height

    cat_opt.get_eta()

    U[i] = cat_opt.U
    Re_h = U[i] * cat_opt.height / cat_opt.air.nu
    f = 24. / Re_h

    perimeter = 2. * (cat_opt.height + cat_opt.width)
    area = cat_opt.height * cat_opt.width
    DeltaP[i] = (
        0.5 * f * perimeter * cat_opt.length / area * cat_opt.air.rho
        * cat_opt.U ** 2.
        )
    Wdot[i] = (
        DeltaP[i] * cat_opt.Vdot / (cat_opt.length * cat_opt.height)
        )

    eta[i] = cat_opt.eta
    eta_per_p[i] = eta[i] / DeltaP[i]
    eta_per_Wdot[i] = eta[i] / Wdot[i]

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

plt.figure('eta per p')
plt.plot(height_array * 1e3, eta_per_p)
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\frac{\eta}{\Delta P}$ (%/Pa)'
    )
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_p.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_p.pdf')

plt.figure('eta per w')
plt.plot(height_array * 1e3, eta_per_Wdot)
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\frac{\eta}{\dot{W}}$ (%/W)'
    )
plt.grid()
# plt.legend(loc="best")
plt.subplots_adjust(left=0.17)
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_Wdot.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_Wdot.pdf')

plt.figure('eta')
plt.plot(height_array * 1e3, eta)
plt.xlabel('Channel Height (mm)')
plt.ylabel('Conversion Efficiency (%)')
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta.pdf')

plt.figure('delta p')
plt.plot(height_array * 1e3, DeltaP)
plt.xlabel('Channel Height (mm)')
plt.ylabel(r'$\Delta P$ (Pa)')
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/deltaP.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'deltaP.pdf')

plt.show()
