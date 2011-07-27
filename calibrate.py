"""Module for plotting results of first term model."""

import scipy as sp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import xlrd
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import experimental_data as expdata
reload(expdata)

data1 = expdata.Data()
data1.Vdot = 250.
source = '250sccm 10nm PtPd variedT.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data_worksheet = xlrd.open_workbook(filename=source).sheet_by_index(0)
    
# Import conversion data from worksheet and store as scipy arrays

data1.T_raw = sp.array(data_worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data1.T_array = data1.T_raw[0::3]
data1.HCout_raw = sp.array(data_worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data1.HCout = sp.array([data1.HCout_raw[0::3],
                        data1.HCout_raw[1::3],
                        data1.HCout_raw[2::3]]).T
data1.HCin_raw = sp.array(data_worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data1.HCin = sp.array([data1.HCin_raw[0::3],
                        data1.HCin_raw[1::3],
                        data1.HCin_raw[2::3]]).T
   
data1.Vdot_array = sp.array([data1.Vdot])
data1.set_eta()
data1.p0 = sp.array([5.e12, 15.e3])
data1.set_params()
data1.set_eta_dim()


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
plt.plot(data1.T_array, data1.eta_mean, ' sk', label='Experiment')  

plt.plot(data1.T_array, data1.eta_dim.T, '-b', label='Model')

plt.legend(loc='best')
plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('HC Conversion Efficiency')
plt.title('HC Conversion v. Temperature')
fig.savefig('Plots/eta v temp.pdf')
fig.savefig('Plots/eta v temp.png')

plt.show()

