"""Module for plotting results of first term model."""

import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import multi_term 
reload(multi_term)

cat4 = multi_term.Catalyst()

cat4.x_array = np.linspace(0., 100., 100)
cat4.y_array = np.linspace(-1., 1., 100)
cat4.A_arr = 5576796142069.6602
cat4.T_a = 15325.877039480061
cat4.set_eta()
Pe = 500.
Da = 1.
cat4.set_Yxy(Pe,Da)
Da_range = sp.linspace(0, 5., 100)
lambda_i = cat4.get_lambda(Da_range)

# Plot configuration
FONTSIZE = 30
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE - 5
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

fig_eigen = plt.figure()
plt.plot(Da_range, lambda_i[3,:], label='4th')
plt.plot(Da_range, lambda_i[2,:], label='3rd')
plt.plot(Da_range, lambda_i[1,:], label='2nd')
plt.plot(Da_range, lambda_i[0,:], label='1st')
plt.xlabel('Da')
plt.ylabel(r'$\lambda_1$')
plt.xlim(0,5)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.17)
#plt.title('Four Eigenvalue Spline Fit')
plt.grid()
plt.legend(loc='best')
plt.savefig('Plots/4eigen_fit.pdf')
plt.savefig('Plots/4eigen_fit.png')

fig_species = plt.figure()
x_2d, y_2d = np.meshgrid(cat4.x_array, cat4.y_array)
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.2, 0.1)
FCS = plt.contourf(x_2d, y_2d, cat4.Yxy.T) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
# plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
#           '\nDa=' + str(cat4.Da) + ' Pe=' + str(cat4.Pe))  
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.savefig('Plots/4species Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.pdf') 
plt.savefig('Plots/4species Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.png')  

fig_eta = plt.figure()
Pe_2d = cat4.Pe_array.T
dummy, Da_2d = np.meshgrid(cat4.Pe_array[:,0], cat4.Da_array)
TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.05, 0.05)
FCS = plt.contourf(Pe_2d, Da_2d, cat4.eta.T) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
plt.grid()
plt.xlabel('Pe')
plt.ylabel('Da')
# plt.title('Species Conversion Efficiency')
plt.savefig('Plots/eta.pdf')
plt.savefig('Plots/eta.png')

plt.show()


