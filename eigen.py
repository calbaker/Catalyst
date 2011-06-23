import numpy as np
import scipy as sp
import matplotlib.pyplot as mpl

lambda_guess = np.arange(0,10., 0.005)
Da = 0.3

def get_solution(lambda_guess, Da):
    solution = 1 - lambda_guess / Da * np.tan(lambda_guess)
    return solution

solution = get_solution(lambda_guess, Da)

# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

fig1 = mpl.figure()
fig1.subplots_adjust(bottom=0.12)
mpl.plot(lambda_guess, solution)
#mpl.xlim(0, 2)
mpl.ylim(-10, 10)
mpl.grid()
mpl.xlabel(r'$\lambda$')
mpl.title('Eigenvalues\nDa='+str(Da))
mpl.savefig('Plots/eigen.pdf')
mpl.savefig('Plots/eigen.png')

mpl.show()
