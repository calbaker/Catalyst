import matplotlib.pyplot as plt
import scipy as sp

data1.A_arr = 5.e16
data1.T_a = 26900.
data1.set_eta()

# Plot configuration
FONTSIZE = 14
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

fig = plt.figure()
plt.plot(data1.T_array, data1.eta_model[0,:], label='model', marker='*')
plt.plot(data1.T_array, data1.eta_exp, label='experiment', marker='x')
plt.grid()
plt.legend(loc='best')
plt.xlabel('Temperature (C)')
plt.ylabel('HC Conversion Efficiency')
plt.title("""Conversion Efficiency v. Temperature for Experimental and
Modeled Data""")
plt.savefig('Plots/graphical fit.pdf')
plt.savefig('Plots/graphical fit.png')

LEVELS = np.linspace(0., 0.009, 10)
fig2 = plt.figure()
A_arr2d, T_a2d = np.meshgrid(data1.A_arr_i, data1.T_a_j)
FCS = plt.contourf(A_arr2d, T_a2d, data1.S_r_ij.T, LEVELS)
CB = mpl.colorbar(FCS, orientation='vertical', format='%0.2e')
plt.xlabel('Preexponential (1/s)')
plt.ylabel('Activation Temperature (K)')
plt.title('Sum of Residuals Squared')
plt.savefig('Plots/S_r map.pdf')
plt.savefig('Plots/S_r map.png')

plt.show()


