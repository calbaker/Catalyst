"""Module for plotting results of first term model with experimental
data and fitting capability."""

import numpy as np
import matplotlib.pyplot as plt
import xlrd
import os


import experimental_data as expdata
reload(expdata)

plt.close('all')

data250 = expdata.ExpDataMulti()
data250.Vdot = 250. * 1.e-6 / 60.
data250.source = '../Conversion Data/250sccm 10nmPtPd VariedT rep2.xls'
A_arr = 10.e6
T_a = 7.2e3
data250.A_arr = A_arr
data250.T_a = T_a
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data250.worksheet = xlrd.open_workbook(filename=data250.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data250.T_raw = np.array(data250.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data250.T_exp = data250.T_raw
data250.HCout_raw = np.array(data250.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data250.HCin_raw = np.array(data250.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data250.eta_exp = (data250.HCin_raw - data250.HCout_raw) / data250.HCin_raw
data250.Vdot_array = np.array([data250.Vdot])
data250.p0 = np.array([A_arr, T_a])
data250.set_params()
data250.set_eta()

data500 = expdata.ExpDataMulti()
data500.T_a = data250.T_a
data500.A_arr = data250.A_arr
data500.Vdot = 500. * 1.e-6 / 60.
data500.source = '../Conversion Data/500sccm 10nmPtPd VariedT rep2.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data500.worksheet = xlrd.open_workbook(filename=data500.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data500.T_raw = np.array(data500.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data500.T_exp = data500.T_raw
data500.HCout_raw = np.array(data500.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data500.HCin_raw = np.array(data500.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data500.eta_exp = (data500.HCin_raw - data500.HCout_raw) / data500.HCin_raw
data500.Vdot_array = np.array([data500.Vdot])
data500.set_eta()

data750 = expdata.ExpDataMulti()
data750.T_a = data250.T_a
data750.A_arr = data250.A_arr
data750.Vdot = 750. * 1.e-6 / 60.
data750.source = '../Conversion Data/750sccm 10nmPtPd VariedT rep2.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data750.worksheet = xlrd.open_workbook(filename=data750.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data750.T_raw = np.array(data750.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data750.T_exp = data750.T_raw
data750.HCout_raw = np.array(data750.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data750.HCin_raw = np.array(data750.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data750.eta_exp = (data750.HCin_raw - data750.HCout_raw) / data750.HCin_raw
data750.Vdot_array = np.array([data750.Vdot])
data750.set_eta()

data1000 = expdata.ExpDataMulti()
data1000.T_a = data250.T_a
data1000.A_arr = data250.A_arr
data1000.Vdot = 1000. * 1.e-6 / 60.
data1000.source = '../Conversion Data/1000sccm 10nmPtPd VariedT rep2.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data1000.worksheet = xlrd.open_workbook(filename=data1000.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data1000.T_raw = np.array(data1000.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data1000.T_exp = data1000.T_raw
data1000.HCout_raw = np.array(data1000.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data1000.HCin_raw = np.array(data1000.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data1000.eta_exp = (data1000.HCin_raw - data1000.HCout_raw) / data1000.HCin_raw
data1000.Vdot_array = np.array([data1000.Vdot])
data1000.set_eta()

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

plt.plot(data500.T_exp, data500.eta_exp * 100., 'og', linestyle='',
         label='500sccm exp')
plt.plot(data500.T_array, data500.eta.T * 100., '-g',
         label='500sccm model')

plt.plot(data750.T_exp, data750.eta_exp * 100., 'v', linestyle='',
         label='750sccm exp')
plt.plot(data750.T_array, data750.eta.T * 100., '-b',
         label='750sccm model')

plt.plot(data1000.T_exp, data1000.eta_exp * 100., '*m', linestyle='',
         label='1000sccm exp')
plt.plot(data1000.T_array, data1000.eta.T * 100., '-m',
         label='1000sccm model')

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
plt.ylim(ymax=37)
# plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig('Plots/4model and exp.pdf')
plt.savefig('Plots/4model and exp.png')

plt.show()
