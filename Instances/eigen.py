import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import os
import sys

cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import catalyst
reload(catalyst)

cat_eigen = catalyst.Catalyst()

Da = 1.

guess = np.arange(0, 24., 0.01)

def get_lambda_error(guess, *args):
    Da = args[0]
    error = 1 - guess / Da * np.tan(guess)
    return error

solution = get_lambda_error(guess, Da)

def solve_lambda(Da):
    lambda_i = fsolve(
        get_lambda_error, x0=cat_eigen.get_lambda(Da=Da), args=(Da)
        )
    return lambda_i

lambda_i = solve_lambda(Da)
ydata = np.zeros(lambda_i.size)

print 'lambda_i =', lambda_i

# Plot configuration
FONTSIZE = 15
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

plt.close()

fig1 = plt.figure()
fig1.subplots_adjust(bottom=0.15)
fig1.subplots_adjust(left=0.15)
plt.plot(guess, solution, label='Da =' + str(Da))
plt.plot(guess, np.absolute(solution), label='absolute')
plt.plot(lambda_i, ydata, label='solver', marker='s', linestyle='',
         color='black')
# plt.xlim(0, 14)
plt.ylim(-20, 20)
plt.grid()
plt.xlabel(r'$\lambda$')
plt.ylabel(r'$1 - \frac{\lambda_n}{Da} \tan \lambda_n$') 
plt.title('Eigenvalues\nDa='+str(Da))
# plt.legend(loc='best')

plt.show()

plt.savefig('../Plots/eigen.pdf')
plt.savefig('../Plots/eigen.png')

