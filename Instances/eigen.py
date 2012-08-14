import numpy as np

import matplotlib.pyplot as plt

Da = 0.25

lambda_guess = np.arange(0, 14., 0.001)

def get_solution(Da):
    solution = 1 - lambda_guess / Da * np.tan(lambda_guess)
    return solution, lambda_guess

solution, lambda_guess = get_solution(Da)

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
plt.plot(lambda_guess, solution, label='Da =' + str(Da))
# plt.plot(lambda_guess, np.absolute(solution), label='absolute')
plt.xlim(0, 14)
plt.ylim(-20, 20)
plt.grid()
plt.xlabel(r'$\lambda$')
plt.ylabel(r'$1 - \frac{\lambda_n}{Da} \tan \lambda_n$') 
plt.title('Eigenvalues\nDa='+str(Da))
# plt.legend(loc='best')

plt.show()

plt.savefig('../Plots/eigen.pdf')
plt.savefig('../Plots/eigen.png')

