"""Script for showing splines and the data they are supposed to
fit.""" 

import matplotlib.pyplot as plt
import os
import sys
import numpy as np

cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import catalyst 
reload(catalyst)

spltest = catalyst.Catalyst()

Da_array = np.linspace(0.001, 1., 100)
lambda_array = np.zeros(
    [Da_array.size, spltest.lambda_and_Da.shape[1] - 1]
    )
print lambda_array.shape

for i in range(Da_array.size):
    Da = Da_array[i]
    lambda_array[i, :] = spltest.get_lambda(Da=Da)

# Plot configuration
FONTSIZE = 20
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

plt.close()

COLOR = ['red', 'green', 'blue', 'black']

for i in range(lambda_array.shape[1]):
    plt.plot(Da_array, lambda_array[:, i], color=COLOR[i % 4])
    plt.plot(
        spltest.lambda_and_Da[:,0], spltest.lambda_and_Da[:, i + 1],
    marker='x', linestyle='', color=COLOR[i % 4]
        ) 

plt.xlabel('Da')
plt.ylabel(r'$\lambda_i$')
plt.xlim(0, Da_array.max())
plt.grid()

plt.savefig('../Plots/splines.pdf')
plt.savefig('../Plots/splines.png')

plt.show()
