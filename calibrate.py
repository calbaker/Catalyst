"""Module for plotting results of first term model."""

import scipy as sp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import experimental_data as expdata
reload(expdata)

data1 = expdata.Data()
data1.source = 'Osman July 3'
data1.Vdot = 250. * 1.e-6 / 60. 
data1.T_array = sp.arange(350., 625., 25.)
data1.HCin = sp.array([[4900., 4950., 4940.], [4900., 4920., 4950.],
                       [5150., 5170., 5140.], [5760., 5450., 5560.],
                       [5550., 5560., 5580.], [4880., 4930., 4950.],
                       [4870., 4900., 4880.], [5140., 5150., 5140.],
                       [5050., 5040., 5050.], [4590., 4500., 4540.],
                       [4570., 4620., 4610.]])
data1.HCout = sp.array([[3910., 3895., 3890.], [3730., 3740., 3720.],
                        [3470., 3510., 3500.], [2890., 2700., 2740.],
                        [1855., 1924., 1935.], [1277., 1310., 1320.],
                        [0753., 0725., 0718.], [0400., 0381., 0377.],
                        [0239., 0220., 0225.], [0111., 0098., 0103.],
                        [0053., 0041., 0045.]])

# data1.T_array = data1.T_array[:-3]
# data1.HCin = data1.HCin[:-3]
# data1.HCout = data1.HCout[:-3]

data1.Vdot_array = sp.array([data1.Vdot])
data1.set_eta()
data1.p0 = sp.array([5.e12, 15.e3])
data1.set_params()

data2 = expdata.Data()
data2.source = 'Osman July 3'
data2.Vdot = 750. * 1.e-6 / 60. 
data2.T_array = sp.arange(350., 675., 25.)
data2.HCin = sp.array([[4540., 4550., 4560.],[4560., 4550., 4590.],
                      [4570., 4550., 4550.], [4540., 4550., 4560.],
                      [4560., 4540., 4540.], [4530., 4590., 4600.],
                      [4660., 4580., 4570.], [4530., 4540., 4540.],
                      [4570., 4560., 4560.], [4570., 4550., 4550.],
                      [4540., 4540., 4550.], [4540., 4540., 4530.],
                      [4530., 4540., 4530.]])

data2.HCout = sp.array([[4160., 4120., 4130.], [4000., 3970., 3990.],
                      [3770., 3730., 3720.], [3480., 3390., 3420.],
                      [3120., 3100., 3070.], [2430., 2450., 2460.],
                      [1993., 1905., 1890.], [1500., 1470., 1460.],
                      [1076., 1028., 1017.], [838., 789., 796.],
                      [591., 615., 604.], [402., 383., 389.], [156.,
                      148., 145.]])
data2.set_eta()
data2.T_array_unsliced = data2.T_array.copy()
data2.eta_unsliced = data2.eta_mean.copy()

# data2.T_array = data2.T_array[:-5]
# data2.HCin = data2.HCin[:-5]
# data2.HCout = data2.HCout[:-5]

data2.Vdot_array = sp.array([data2.Vdot])
data2.p0 = sp.array([5.e12, 15.e3])
data2.set_params()

data2.T_array = data2.T_array_unsliced
data2.eta_mean = data2.eta_unsliced

data1.A_arr = data2.A_arr
data1.T_a = data2.T_a

# Plot configuration
FONTSIZE = 14
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

fig = plt.figure()
plt.plot(data1.T_array, data1.eta_mean, ' sb', label='250sccm exp')  
plt.plot(data2.T_array, data2.eta_mean, ' sk', label='750sccm exp')   

data1.T_array = sp.arange(350., 655., 5.)
data1.set_eta_dim()
plt.plot(data1.T_array, data1.eta_dim.T, '-b', label='250sccm mod')

data2.T_array = sp.arange(350., 655., 5.)
data2.set_eta_dim()
plt.plot(data2.T_array, data2.eta_dim.T, '-k', label='750sccm mod')

plt.legend(loc='best')
plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('HC Conversion Efficiency')
plt.title('HC Conversion v. Temperature')
fig.savefig('Plots/eta v temp.pdf')
fig.savefig('Plots/eta v temp.png')

plt.show()

