"""Module for plotting results of first term model with experimental
data and fitting capability."""

import scipy as sp
import matplotlib.pyplot as plt
import xlrd
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

from first_term import *
import experimental_data as expdata
reload(expdata)

plt.close('all')

data250 = expdata.Data()
data250.Vdot = 250. * 1.e-6 / 60.
data250.source = '250sccm 10nmPtPd VariedT aug.xls'
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
data250.eta_mean = (data250.HCin_raw - data250.HCout_raw) / data250.HCin_raw
data250.T_array = sp.linspace(250., 650., 100)
data250.Vdot_array = sp.array([data250.Vdot])
data250.p0 = sp.array([1e7, 5e3])
data250.set_params()
data250.set_eta_dim()

data750 = expdata.Data()
data750.T_a = data250.T_a
data750.A_arr = data250.A_arr
data750.Vdot = 750. * 1.e-6 / 60.
data750.source = '750sccm 10nmPtPd VariedT aug.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data750.worksheet = xlrd.open_workbook(filename=data750.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data750.T_raw = sp.array(data750.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data750.T_exp = data750.T_raw
data750.HCout_raw = sp.array(data750.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data750.HCin_raw = sp.array(data750.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data750.eta_mean = (data750.HCin_raw - data750.HCout_raw) / data750.HCin_raw
data750.T_array = sp.linspace(250., 650., 100)
data750.Vdot_array = sp.array([data750.Vdot])
data750.set_eta_dim()


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
plt.plot(data250.T_exp, data250.eta_mean * 100., 'sr', linestyle='',
         label='250sccm exp')
plt.plot(data250.T_array, data250.eta_dim.T * 100., '-r',
         label='250sccm model')

plt.plot(data750.T_exp, data750.eta_mean * 100., 'sb', linestyle='',
         label='750sccm exp')
plt.plot(data750.T_array, data750.eta_dim.T * 100., '-b',
         label='750sccm model')

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
plt.xlim(xmax=450)
plt.ylim(ymax=40)
#plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig('Plots/model and exp.pdf')
plt.savefig('Plots/model and exp.png')

plt.show()
