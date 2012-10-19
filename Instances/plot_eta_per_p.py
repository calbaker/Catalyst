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
cat_opt.Vdot = 50000.e-6 / 60. 
cat_opt.T = 400. + 273.15
cat_opt.set_TempPres_dependents(cat_opt.T)

length = cat_opt.length
height = cat_opt.height
height_array = np.linspace(0.5, 10., 25) * 1.e-3
length_array = (length * height) / height_array

U = np.zeros(height_array.size)
DeltaP_c_L = np.zeros(height_array.size)
DeltaP_c_V = np.zeros(height_array.size)

eta_c_L = np.zeros(height_array.size)
eta_per_p_c_L = np.zeros(height_array.size)
eta_c_V = np.zeros(height_array.size)
eta_per_p_c_V = np.zeros(height_array.size)

for i in range(height_array.size):
    # Constant Length
    cat_opt.length = length
    cat_opt.height = height_array[i]
    cat_opt.x_ = cat_opt.length / cat_opt.height

    cat_opt.get_eta()
    print "\n\n\nConstant Length"
    print "Da =", cat_opt.Da
    print "A_i =", cat_opt.A_i
    print "lambda_i =", cat_opt.lambda_i

    U[i] = cat_opt.U
    Re_h = U[i] * height_array[i] / cat_opt.air.nu
    f = 24. / Re_h

    perimeter = 2. * (cat_opt.height + cat_opt.width)
    area = cat_opt.height * cat_opt.width

    DeltaP_c_L[i] = (
        0.5 * f * perimeter * cat_opt.length / area * cat_opt.air.rho
        * cat_opt.U ** 2. * 1e-3
        )

    eta_c_L[i] = cat_opt.eta
    eta_per_p_c_L[i] = eta_c_L[i] / DeltaP_c_L[i]

    # Constant Volume
    cat_opt.length = length_array[i]
    cat_opt.x_ = cat_opt.length / cat_opt.height

    cat_opt.get_eta()
    print "\nConstant Volume"
    print "Da =", cat_opt.Da
    print "A_i =", cat_opt.A_i
    print "lambda_i =", cat_opt.lambda_i

    perimeter = 2. * (cat_opt.height + cat_opt.width)
    area = cat_opt.height * cat_opt.width

    DeltaP_c_V[i] = (
        0.5 * f * perimeter * cat_opt.length / area * cat_opt.air.rho
        * cat_opt.U ** 2. * 1e-3
        )

    eta_c_V[i] = cat_opt.eta
    eta_per_p_c_V[i] = eta_c_V[i] / DeltaP_c_V[i]

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
plt.plot(height_array * 1e3, eta_per_p_c_L, label="Const. L")
plt.plot(height_array * 1e3, eta_per_p_c_V, label="Const. V")
plt.xlabel('Channel Height (mm)')
plt.ylabel(
    r'$\frac{\eta}{\Delta P}$ (%/kPa)'
    )
plt.grid()
plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_p.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_p.pdf')

plt.figure('eta per p v length')
plt.plot(length_array * 1e3, eta_per_p_c_V)
plt.xlabel('Channel Length (mm)')
plt.ylabel(
    r'$\frac{\eta}{\Delta P}$ (%/kPa)'
    )
plt.grid()
plt.savefig(
    '../Plots/plot_eta_per_p/eta_per_p_v_length.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta_per_p_v_length.pdf')

plt.figure('eta')
plt.plot(height_array * 1e3, eta_c_L, label="Const. L")
plt.plot(height_array * 1e3, eta_c_V, label="Const. V")
plt.xlabel('Channel Height (mm)')
plt.ylabel('Conversion Efficiency (%)')
plt.grid()
plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/eta.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'eta.pdf')

plt.figure('delta p')
plt.plot(height_array * 1e3, DeltaP_c_L, label="Const. L")
plt.plot(height_array * 1e3, DeltaP_c_V, label="Const. V")
plt.xlabel('Channel Height (mm)')
plt.ylabel(r'$\Delta P$ (kPa)')
plt.grid()
plt.legend(loc="best")
plt.savefig(
    '../Plots/plot_eta_per_p/deltaP.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'deltaP.pdf')

plt.show()
