import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import first_term as ft

# For Da = 1,
lambda_i = np.array([0.86, 3.43, 6.44, 9.53])
terms = np.size(lambda_i)
A_i = ( 2. * np.sin(lambda_i) / (lambda_i + np.sin(lambda_i) *
                                 np.cos(lambda_i)) ) 
Pe = 50. 

def get_Y(x_, y_, A_i, lambda_i, Pe):
    Y = ( sp.sum(A_i * np.exp(-4. * lambda_i**2. / Pe * x_) *
    np.cos(lambda_i * y_)) ) 
    return Y

x_ = np.linspace(0., 200., 50)
y_ = np.linspace(-1., 1., 100)
Y = np.zeros([np.size(x_), np.size(y_)])

for i in sp.arange(sp.size(x_)):
    for j in sp.arange(sp.size(y_)):
        Y[i,j] = get_Y(x_[i], y_[j], A_i, lambda_i, Pe)

# Plot configuration
FONTSIZE = 30
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

x_2d, y_2d = np.meshgrid(x_, y_)
TICKS = sp.arange(0,1.2,0.2)
LEVELS = sp.arange(0, 1.1, 0.05)
fig_eta = plt.figure()
FCS = plt.contourf(x_2d, y_2d, Y.T, levels=LEVELS)  
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS)
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
plt.ylim(-1,1)
#plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$') 
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('Plots/'+ str(terms) + 'term species.pdf')
plt.savefig('Plots/'+ str(terms) + 'term species.png')

cat1 = ft.One_Term_Catalyst()

cat1.x_array = np.linspace(0., 200., 50)
cat1.y_array = np.linspace(-1., 1, 100)
cat1.Pe = 50.
cat1.set_Yxy_()

fig_species = plt.figure()
x_2d, y_2d = np.meshgrid(cat1.x_array, cat1.y_array)
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.2, 0.1)
FCS = plt.contourf(x_2d, y_2d, cat1.Yxy_.T) 
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f')
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
# plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
#           '\nDa=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe))  
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.pdf') 
plt.savefig('Plots/species Da=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe)
            + '.png')  

plt.show()
