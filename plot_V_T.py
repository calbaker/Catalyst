"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

from first_term import *

mpl.close('all')

cat2 = One_Term_Catalyst()

cat2.T_array = sp.arange(200., 800., 20.)
cat2.set_Da()
cat2.set_Pe()
cat2.set_eta_dimensional()
Vdot2d, T2d = np.meshgrid(cat2.Vdot, cat2.T_array)
Vdot2d = Vdot2d * 60. * 1.e6
# converts back to sccm for plotting

# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

fig_eta_real = mpl.figure()
TICKS = sp.arange(0,1.1,0.1)
LEVELS = sp.arange(0.0, 1.05, 0.05)
FCS = mpl.contourf(Vdot2d, T2d, cat2.eta_ij.T, LEVELS)
CB = mpl.colorbar(FCS, orientation='horizontal')
mpl.grid()
mpl.xlabel(r'$\dot{V}$ (sccm)')
mpl.ylabel('T (C)')
mpl.title(
    'Conversion Efficiency v.\nFlow Rate and Temperature') 
mpl.savefig('Plots/eta v V and T.pdf')
mpl.savefig('Plots/eta v V and T.png')

mpl.show()
