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

A_arr = 10.e6
T_a = 7.2e3

data = multi_term.Catalyst()
data.Vdot = 750. * 1.e-6 / 60.
# data.source = 'alumina_holder_only.xls' # this data needs to be
# cleared with Hall and Ezekoye
data.source = '750sccm 10nmPtPd VariedT rep2.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data.worksheet = xlrd.open_workbook(filename=data.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data.T_raw = sp.array(data.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data.T_exp = data.T_raw
data.HCout_raw = sp.array(data.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data.HCin_raw = sp.array(data.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data.eta_exp = (data.HCin_raw - data.HCout_raw) / data.HCin_raw
data.Vdot_array = sp.array([data.Vdot])
data.set_eta()

data_empty = multi_term.Catalyst()
# data_empty.source = 'alumina_holder_only.xls' # this data needs to be
# cleared with Hall and Ezekoye
data_empty.source = '1000sccm empty tube rep2.xls'
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

plt.plot(data.T_exp, data.eta_exp * 100., 'sr', linestyle='',
         label='750sccm exp')
plt.plot(data.T_array, data.eta.T * 100., '-r',
         label='750sccm model')

plt.plot(data_empty.T_exp, data_empty.eta_exp * 100., 'sm', linestyle='',
         label='1000sccm control')

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
plt.ylim(ymax=40)
plt.xlim(xmax=700)
# plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig('Plots/high_temp_bad.pdf')
plt.savefig('Plots/high_temp_bad.png')

plt.show()
