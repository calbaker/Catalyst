"""Module for plotting results of first term model with experimental
data and fitting capability."""

import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from scipy.optimize import fsolve

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
length_array = length * (height_array / height)
Vdot_array = Vdot * height_array / height

cat_opt.Vdot = Vdot

DeltaP = np.zeros(height_array.size)
eta = np.zeros(height_array.size)

cat_opt.get_eta()
U = cat_opt.U

def get_DeltaP(length, *args):
    height = args[0]
    Re_h = U * height / cat_opt.air.nu
    f = 24. / Re_h

    perimeter = 2. * (height + cat_opt.width)
    area = height * cat_opt.width
    DeltaP = (
        0.5 * f * perimeter * length / area * cat_opt.air.rho *
        cat_opt.U ** 2.
        )
    return DeltaP

DeltaP0 = get_DeltaP(length, height)

def get_error(length, *args):
    height = args[0]
    DeltaP = get_DeltaP(length, height)
    error = DeltaP - DeltaP0
    return error

for i in range(height_array.size):
    height = height_array[i]
    # length_array[i] = (
    #     fsolve(get_error, x0=length_array[i], args=(height))
    #     )
    cat_opt.height = height_array[i]
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

Wdot = DeltaP * Vdot_array * height / height_array
eta_per_p = eta / DeltaP
eta_per_Wdot = eta / Wdot
eta_per_cat = eta * height_array / length_array
eta_per_cat_p = (
    eta * (height_array / length_array) / (DeltaP * 1e-3)
    )

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

# eta per cat_p
plt.figure('eta per cat_p')
plt.plot(height_array * 1e3, eta_per_cat_p)
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\frac{\eta}{cat p}$'
    )
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_cat_p.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_cat_p.pdf')

# eta per cat
plt.figure('eta per cat')
plt.plot(height_array * 1e3, eta_per_cat)
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
plt.plot(height_array * 1e3, eta)
plt.xlabel('Channel Height (mm)')
plt.ylabel('Conversion Efficiency (%)')
plt.grid()
# plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta.pdf')

plt.show()
