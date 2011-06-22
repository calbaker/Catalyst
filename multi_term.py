import numpy as np
import scipy as sp
import matplotlib.pyplot as mpl

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

x_ = np.arange(0., 52., 2.)
y_ = np.arange(-1., 1.001, 0.001)
Y = np.zeros([np.size(x_), np.size(y_)])

for i in sp.arange(sp.size(x_)):
    for j in sp.arange(sp.size(y_)):
        Y[i,j] = get_Y(x_[i], y_[j], A_i, lambda_i, Pe)

# Plot configuration
FONTSIZE = 20
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

x_2d, y_2d = np.meshgrid(x_, y_)
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0, 1.1, 0.05)
fig_eta = mpl.figure()
FCS = mpl.contourf(x_2d, y_2d, Y.T, LEVELS) 
CB = mpl.colorbar(FCS, orientation='horizontal')
mpl.grid()
mpl.xlabel(r'$\tilde{x}$')
mpl.ylabel(r'$\tilde{y}$')
mpl.ylim(-1,1)
mpl.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$') 
mpl.ylim(-1, 1)
mpl.savefig('Plots/'+ str(terms) + 'term species.pdf')
mpl.savefig('Plots/'+ str(terms) + 'term species.png')

