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
cat_opt.T = 400. + 273.15  # temperature (K)
cat_opt.set_TempPres_dependents(cat_opt.T)

height = cat_opt.height
length = cat_opt.length
thickness = 550.e-6  # wafer thickness (m)
Vdot = 500.e-6 / 60. # volume flow rate (m/s)

height_array = np.linspace(0.25, 10., 25) * height
# distance (m) between plate centerlines

length_array = length * (height_array / height)
# lengths (m) for const. catalyst area 

# length_array = np.ones(height_array.size) * length
# lengths (m) for const. length

# length_array = length * height / height_array
# lengths (m) for const. volume

h_gap = height_array - thickness
# height (m) of actual gap

Vdot_array = (height - thickness) / h_gap * Vdot

cat_opt.Vdot = Vdot

DeltaP = np.zeros(height_array.size)
eta = np.zeros(height_array.size)

cat_opt.get_eta()
U = cat_opt.U


for i in range(height_array.size):
    cat_opt.height = h_gap[i]
    cat_opt.length = length_array[i]
    cat_opt.Vdot = Vdot_array[i]
    cat_opt.x_ = cat_opt.length / cat_opt.height

    cat_opt.get_eta()

    U = cat_opt.U
    Re_h = U * cat_opt.height / cat_opt.air.nu
    f = 24. / Re_h

    perimeter = 2. * (cat_opt.height + cat_opt.width)
    area = cat_opt.height * cat_opt.width
    DeltaP[i] = (
        0.5 * f * perimeter * cat_opt.length / area * cat_opt.air.rho
        * cat_opt.U ** 2.
        )
    eta[i] = cat_opt.eta

Wdot = DeltaP * Vdot
eta_per_p = eta / DeltaP
eta_per_Wdot = eta / Wdot
eta_per_cat = eta * height_array / length_array
eta_per_vol = eta * length_array / length * (length * height)

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

# eta per vol
plt.figure('eta per vol')
plt.plot(h_gap * 1e3, eta_per_vol)
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\frac{\eta}{volume}$'
    )
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_vol.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_vol.pdf')

# eta per DeltaP
plt.figure('eta per DeltaP')
plt.plot(h_gap * 1e3, eta_per_p)
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\frac{\eta}{???}$'
    )
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_p.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_p.pdf')

# eta per Wdot
plt.figure('eta per Wdot')
plt.plot(h_gap * 1e3, eta_per_Wdot)
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\frac{\eta}{\dot{W}}$'
    )
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_p.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_p.pdf')

# eta per cat
plt.figure('eta per cat')
plt.plot(h_gap * 1e3, eta_per_cat)
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\frac{\eta}{A}$ (%/m$^2$)'
    )
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_cat.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_cat.pdf')

# eta
plt.figure('eta')
plt.plot(h_gap * 1e3, eta)
plt.xlabel('Channel Height (mm)')
plt.ylabel('Conversion Efficiency (%)')
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta.pdf')

plt.show()
