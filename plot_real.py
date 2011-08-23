"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as plt
import xlrd
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

from first_term import *
import experimental_data as expdata
reload(expdata)

plt.close('all')

data1 = expdata.Data()
data1.Vdot = 250. * 1.e-6 / 60.
data1.source = '250sccm 10nm PtPd variedT.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data1.worksheet = xlrd.open_workbook(filename=data1.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data1.T_raw = sp.array(data1.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data1.T_exp = data1.T_raw[0::3]
data1.HCout_raw = sp.array(data1.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data1.HCout = sp.array([data1.HCout_raw[0::3],
                        data1.HCout_raw[1::3],
                        data1.HCout_raw[2::3]]).T
data1.HCin_raw = sp.array(data1.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data1.HCin = sp.array([data1.HCin_raw[0::3],
                        data1.HCin_raw[1::3],
                        data1.HCin_raw[2::3]]).T
data1.T_array = sp.arange(305., 655., 5.)
data1.Vdot_array = sp.array([data1.Vdot])
data1.set_eta()
data1.eta_mean = data1.eta_mean[:-3]
data1.T_exp = data1.T_exp[:-3]
data1.set_params()
data1.set_eta_dim()

data2 = expdata.Data()
data2.Vdot = 750. * 1.e-6 / 60.
data2.source = '750sccm 10nm PtPd variedT.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data2.worksheet = xlrd.open_workbook(filename=data2.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data2.T_raw = sp.array(data2.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data2.T_exp = data2.T_raw[0::3]
data2.HCout_raw = sp.array(data2.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data2.HCout = sp.array([data2.HCout_raw[0::3],
                        data2.HCout_raw[1::3],
                        data2.HCout_raw[2::3]]).T
data2.HCin_raw = sp.array(data2.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data2.HCin = sp.array([data2.HCin_raw[0::3],
                        data2.HCin_raw[1::3],
                        data2.HCin_raw[2::3]]).T
data2.T_array = sp.arange(305., 655., 5.)
data2.Vdot_array = sp.array([data2.Vdot])
data2.set_eta()
data2.set_eta_dim()

data3 = expdata.Data()
data3.Vdot = 1000. * 1.e-6 / 60.
data3.source = '1000sccm 10nm PtPd variedT.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data3.worksheet = xlrd.open_workbook(filename=data3.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data3.T_raw = sp.array(data3.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data3.T_exp = data3.T_raw[0::3]
data3.HCout_raw = sp.array(data3.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data3.HCout = sp.array([data3.HCout_raw[0::3],
                        data3.HCout_raw[1::3],
                        data3.HCout_raw[2::3]]).T
data3.HCin_raw = sp.array(data3.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data3.HCin = sp.array([data3.HCin_raw[0::3],
                        data3.HCin_raw[1::3],
                        data3.HCin_raw[2::3]]).T
data3.T_array = sp.arange(305., 655., 5.)
data3.Vdot_array = sp.array([data3.Vdot])
data3.set_eta()
data3.set_eta_dim()

# Plot configuration
FONTSIZE = 14
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

plt.figure()
plt.plot(data1.T_exp, data1.eta_mean, 'sk', label='250sccm exp')
plt.plot(data1.T_array, data1.eta_dim.T, '-k', label='250sccm model')

plt.plot(data2.T_exp, data2.eta_mean, 'sr', linestyle='', label='750sccm exp')
plt.plot(data2.T_array, data2.eta_dim.T, '-r', label='750sccm model')

plt.plot(data3.T_exp, data3.eta_mean, 'sb', linestyle='', label='1000sccm exp')
plt.plot(data3.T_array, data3.eta_dim.T, '-b', label='1000sccm model')

plt.xlabel('Temperature (C)')
plt.ylabel('Conversion Efficiency (%)')
plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig('Plots/model and exp.pdf')
plt.savefig('Plots/model and exp.png')

plt.show()
