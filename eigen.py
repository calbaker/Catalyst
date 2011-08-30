import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

Da = 1.  

def get_solution(Da):
    lambda_guess = np.arange(0, 10., 0.0001)
    solution = 1 - lambda_guess / Da * np.tan(lambda_guess)
    return solution,lambda_guess

def plot_solution(Da):
    solution,lambda_guess = get_solution(Da)

    # Plot configuration
    FONTSIZE = 20
    plt.rcParams['axes.labelsize'] = FONTSIZE
    plt.rcParams['axes.titlesize'] = FONTSIZE
    plt.rcParams['legend.fontsize'] = FONTSIZE
    plt.rcParams['xtick.labelsize'] = FONTSIZE
    plt.rcParams['ytick.labelsize'] = FONTSIZE
    plt.rcParams['lines.linewidth'] = 1.5
    plt.rcParams['lines.markersize'] = 10

    fig1 = plt.figure()
    fig1.subplots_adjust(bottom=0.12)
    fig1.subplots_adjust(left=0.17)
    plt.plot(lambda_guess, solution, label='Da =' + str(Da))
    plt.plot(lambda_guess, sp.absolute(solution), label='absolute')
    # plt.xlim(0, 2)
    plt.ylim(-100, 100)
    plt.grid()
    plt.xlabel(r'$\lambda$')
    plt.ylabel(r'$1 - \frac{\lambda}{Da} \lambda$') 
    # plt.title('Eigenvalues\nDa='+str(Da))
    plt.legend(loc='best')

    plt.savefig('Plots/eigen.pdf')
    plt.savefig('Plots/eigen.png')

    plt.show()
