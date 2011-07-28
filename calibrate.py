"""Module for plotting results of first term model."""

import scipy as sp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import xlrd
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import experimental_data as expdata
reload(expdata)

cal_data = expdata.Data()

cal_data.Vdot = 250. * 1.e-6 / 60.
source = '250sccm 10nm PtPd variedT.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data_worksheet = xlrd.open_workbook(filename=source).sheet_by_index(0)
    
# Import conversion data from worksheet and store as scipy arrays

cal_data.T_raw = sp.array(data_worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
cal_data.T_exp = cal_data.T_raw[0::3]
cal_data.HCout_raw = sp.array(data_worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
cal_data.HCout = sp.array([cal_data.HCout_raw[0::3],
                        cal_data.HCout_raw[1::3],
                        cal_data.HCout_raw[2::3]]).T
cal_data.HCin_raw = sp.array(data_worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
cal_data.HCin = sp.array([cal_data.HCin_raw[0::3],
                        cal_data.HCin_raw[1::3],
                        cal_data.HCin_raw[2::3]]).T
cal_data.HCin = cal_data.HCin[1:-2]
cal_data.HCout = cal_data.HCout[1:-2]
cal_data.T_exp = cal_data.T_exp[1:-2]
   
cal_data.Vdot_array = sp.array([cal_data.Vdot])
cal_data.set_eta()
cal_data.p0 = sp.array([5.e12, 13.e3])
cal_data.set_params()
cal_data.T_array = sp.arange(325., 655., 5.)
cal_data.set_eta_dim()


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
plt.plot(cal_data.T_exp, cal_data.eta_mean, ' sk', label='Experiment')  
plt.plot(cal_data.T_array, cal_data.eta_dim.T, '-b', label='Model')
plt.xlim(350, 575)
plt.legend(loc='best')
plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('HC Conversion Efficiency')
plt.title('HC Conversion v. Temperature')
fig.savefig('Plots/calibrate.pdf')
fig.savefig('Plots/calibrate.png')

plt.show()

