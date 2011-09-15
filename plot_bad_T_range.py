"""Module for plotting results of first term model with experimental
data and fitting capability."""

import scipy as sp
import matplotlib.pyplot as plt
import xlrd
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import multi_term
reload(multi_term)

plt.close('all')

data250 = multi_term.Catalyst()
data250.Vdot = 250. * 1.e-6 / 60.
data250.source = '250sccm 10nmPtPd VariedT rep2.xls'
A_arr = 10.e6
T_a = 7.2e3
data250.A_arr = A_arr
data250.T_a = T_a
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data250.worksheet = xlrd.open_workbook(filename=data250.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data250.T_raw = sp.array(data250.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data250.T_exp = data250.T_raw
data250.HCout_raw = sp.array(data250.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data250.HCin_raw = sp.array(data250.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data250.eta_exp = (data250.HCin_raw - data250.HCout_raw) / data250.HCin_raw
data250.Vdot_array = sp.array([data250.Vdot])
data250.p0 = sp.array([A_arr, T_a])
data250.set_eta()

data_empty = multi_term.Catalyst()
data_empty.source = '1000sccm empty tube.xls'
data_empty.A_arr = A_arr
data_empty.T_a = T_a
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data_empty.worksheet = xlrd.open_workbook(filename=data_empty.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data_empty.T_raw = sp.array(data_empty.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data_empty.T_exp = data_empty.T_raw
data_empty.HCout_raw = sp.array(data_empty.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data_empty.HCin_raw = sp.array(data_empty.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data_empty.eta_exp = (data_empty.HCin_raw - data_empty.HCout_raw) / data_empty.HCin_raw


# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE 
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

plt.figure()

plt.plot(data250.T_exp, data250.eta_exp * 100., 'sr', linestyle='',
         label='250sccm exp')
plt.plot(data250.T_array, data250.eta.T * 100., '-r',
         label='250sccm model')

plt.plot(data_empty.T_exp, data_empty.eta_exp * 100., 'sm', linestyle='',
         label='1000sccm empty tube')

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
#plt.ylim(ymax=30)
# plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig('Plots/high_temp_bad.pdf')
plt.savefig('Plots/high_temp_bad.png')

plt.show()
