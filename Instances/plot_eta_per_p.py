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

height0 = cat_opt.height
length0 = cat_opt.length
thickness = 550.e-6  # wafer thickness (m)
Vdot0 = 500.e-6 / 60. # volume flow rate (m^3/s)

height = np.linspace(0.25, 1.5, 50) * height0
# distance (m) between plate centerlines

length = length0 * (height / height0)
# lengths (m) for const. catalyst area 

# length_array = np.ones(height_array.size) * length
# lengths (m) for const. length

# length_array = length * height / height_array
# lengths (m) for const. volume

h_gap = height - thickness
# height (m) of actual gap
h_gap0 = height0 - thickness

volume = length * height

Vdot = Vdot0 * h_gap0 / height0 * (height / h_gap)
# from previous commit: 
# Vdot_array = (height - thickness) / h_gap * Vdot

DeltaP = np.zeros(height.size)
Da = np.zeros(height.size)
Pe = np.zeros(height.size)
thiele = np.zeros(height.size)
eta = np.zeros(height.size)
U = np.zeros(height.size)

for i in range(height.size):
    cat_opt.height = h_gap[i]
    cat_opt.length = length[i]
    cat_opt.Vdot = Vdot[i]
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
    Da[i] = cat_opt.Da
    Pe[i] = cat_opt.Pe
    thiele[i] = cat_opt.thiele
    eta[i] = cat_opt.eta

Wdot = DeltaP * Vdot
eta_per_p = eta / DeltaP
eta_per_Wdot = eta / Wdot
eta_per_cat = eta * height / length
eta_per_vol = eta / volume

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
plt.plot(h_gap * 1e3, eta_per_vol, '-k')
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\eta$ / V (m$^{-3}$)'
    )
plt.grid()
# plt.legend(loc="best")
# plt.savefig(
#     '../Plots/plot_eta_per_p/eta_per_vol.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_vol.pdf')

plt.show()
plt.close()

FONTSIZE = 30
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

plt.figure('eta per vol big font')
plt.plot(h_gap * 1e3, eta_per_vol, '-k')
plt.xticks(rotation=45)
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\eta$ / V (m$^{-3}$)'
    )
plt.grid()
# plt.legend(loc="best")
plt.subplots_adjust(bottom=0.2, left=0.2)
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_vol.pdf')

# # dimless number
# plt.figure('thiele, Da, and Pe')
# plt.plot(
#     h_gap * 1e3, Da * 1e3, label=r'Da x 10$^3$'
#     )
# plt.plot(
#     h_gap * 1e3, Pe, label='Pe'
#     )
# plt.xlabel('Channel Height (mm)')
# plt.grid()
# plt.legend(loc="best")
# plt.savefig(
#     '../Plots/plot_eta_per_p/dimless.pdf')
# paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
# plt.savefig(paper_dir + 'dimless.pdf')

# # eta per DeltaP
# plt.figure('eta per DeltaP')
# plt.plot(h_gap * 1e3, eta_per_p)
# plt.xlabel('Channel Height (mm)')
# plt.ylabel(
#     r'$\frac{\eta}{???}$'
#     )
# plt.grid()
# # plt.legend(loc="best")
# plt.savefig(
#     '../Plots/plot_eta_per_p/eta_per_p.pdf')
# paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
# plt.savefig(paper_dir + 'eta_per_p.pdf')

# # eta per Wdot
# plt.figure('eta per Wdot')
# plt.plot(h_gap * 1e3, eta_per_Wdot)
# plt.xlabel('Channel Height (mm)')
# plt.ylabel(
#     r'$\frac{\eta}{\dot{W}}$'
#     )
# plt.grid()
# # plt.legend(loc="best")
# plt.savefig(
#     '../Plots/plot_eta_per_p/eta_per_p.pdf')
# paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
# plt.savefig(paper_dir + 'eta_per_p.pdf')

# # eta per cat
# plt.figure('eta per cat')
# plt.plot(h_gap * 1e3, eta_per_cat)
# plt.xlabel('Channel Height (mm)')
# plt.ylabel(
#     r'$\frac{\eta}{A}$ (%/m$^2$)'
#     )
# plt.grid()
# # plt.legend(loc="best")
# plt.savefig(
#     '../Plots/plot_eta_per_p/eta_per_cat.pdf')
# paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
# plt.savefig(paper_dir + 'eta_per_cat.pdf')

# eta
plt.figure('eta')
plt.plot(h_gap * 1e3, eta)
plt.xlabel('Channel Height (mm)')
plt.ylabel('Conversion Efficiency (%)')
plt.xticks(rotation=45)
plt.grid()
# plt.legend(loc="best")
plt.subplots_adjust(bottom=0.2, left=0.2)
plt.savefig(
    '../Plots/plot_eta_per_p/eta.pdf')
# paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
# plt.savefig(paper_dir + 'eta.pdf')

plt.show()
