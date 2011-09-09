"""Module for plotting results of first term model with experimental
data and fitting capability."""

import scipy as sp
import matplotlib.pyplot as plt
import xlrd
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import first_term as ft
reload(ft)

plt.close('all')

data250 = ft.One_Term_Catalyst()
data250.Vdot = 250. * 1.e-6 / 60.
data250.source = '250sccm 10nmPtPd VariedT rep2.xls'
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
data250.T_array = sp.linspace(250., 650., 100)
data250.Vdot_array = sp.array([data250.Vdot])
data250.p0 = sp.array([1e7, 15e3])
data250.set_params()
data250.set_eta()

# data250osman = ft.One_Term_Catalyst()
# data250osman.T_a = data250.T_a
# data250osman.A_arr = data250.A_arr
# data250osman.Vdot = 250. * 1.e-6 / 60.
# data250osman.source = '250sccm 10nm PtPd variedT.xls'
# # Define the path to the .xls file(s) containing the conversion data.
# # import the worksheet as a sheet object
# data250osman.worksheet = xlrd.open_workbook(filename=data250osman.source).sheet_by_index(0)
# # Import conversion data from worksheet and store as scipy arrays
# data250osman.T_raw = sp.array(data250osman.worksheet.col_values(0, start_rowx=4, 
#                                                  end_rowx=None)) 
# data250osman.T_exp = data250osman.T_raw[0::3]
# data250osman.HCout_raw = sp.array(data250osman.worksheet.col_values(4, start_rowx=4, 
#                                                      end_rowx=None))
# data250osman.HCout = sp.array([data250osman.HCout_raw[0::3],
#                         data250osman.HCout_raw[1::3],
#                         data250osman.HCout_raw[2::3]]).T
# data250osman.HCin_raw = sp.array(data250osman.worksheet.col_values(8, start_rowx=4,
#                                                     end_rowx=None))
# data250osman.HCin = sp.array([data250osman.HCin_raw[0::3],
#                         data250osman.HCin_raw[1::3],
#                         data250osman.HCin_raw[2::3]]).T
# data250osman.set_eta()
# data250osman.T_array = sp.linspace(250., 650., 100)
# data250osman.Vdot_array = sp.array([data250osman.Vdot])
# data250osman.set_eta()

data250b = ft.One_Term_Catalyst()
data250b.Vdot = 250. * 1.e-6 / 60.
data250b.source = '250sccm 10nmPtPd VariedT rep3.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data250b.worksheet = xlrd.open_workbook(filename=data250b.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data250b.T_raw = sp.array(data250b.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data250b.T_exp = data250b.T_raw
data250b.HCout_raw = sp.array(data250b.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data250b.HCin_raw = sp.array(data250b.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data250b.eta_exp = (data250b.HCin_raw - data250b.HCout_raw) / data250b.HCin_raw

data500 = ft.One_Term_Catalyst()
data500.T_a = data250.T_a
data500.A_arr = data250.A_arr
data500.Vdot = 500. * 1.e-6 / 60.
data500.source = '500sccm 10nmPtPd VariedT rep2.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data500.worksheet = xlrd.open_workbook(filename=data500.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data500.T_raw = sp.array(data500.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data500.T_exp = data500.T_raw
data500.HCout_raw = sp.array(data500.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data500.HCin_raw = sp.array(data500.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data500.eta_exp = (data500.HCin_raw - data500.HCout_raw) / data500.HCin_raw
data500.T_array = sp.linspace(250., 650., 100)
data500.Vdot_array = sp.array([data500.Vdot])
data500.set_eta()

data500b = ft.One_Term_Catalyst()
data500b.source = '500sccm 10nmPtPd VariedT rep3.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data500b.worksheet = xlrd.open_workbook(filename=data500b.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data500b.T_raw = sp.array(data500b.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data500b.T_exp = data500b.T_raw
data500b.HCout_raw = sp.array(data500b.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data500b.HCin_raw = sp.array(data500b.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data500b.eta_exp = (data500b.HCin_raw - data500b.HCout_raw) / data500b.HCin_raw

data100 = ft.One_Term_Catalyst()
data100.T_a = data250.T_a
data100.A_arr = data250.A_arr
data100.Vdot = 100. * 1.e-6 / 60.
data100.source = '100sccm 10nmPtPd VariedT rep3.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data100.worksheet = xlrd.open_workbook(filename=data100.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data100.T_raw = sp.array(data100.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data100.T_exp = data100.T_raw
data100.HCout_raw = sp.array(data100.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data100.HCin_raw = sp.array(data100.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data100.eta_exp = (data100.HCin_raw - data100.HCout_raw) / data100.HCin_raw
data100.T_array = sp.linspace(250., 650., 100)
data100.Vdot_array = sp.array([data100.Vdot])
data100.set_eta()

data750 = ft.One_Term_Catalyst()
data750.T_a = data250.T_a
data750.A_arr = data250.A_arr
data750.Vdot = 750. * 1.e-6 / 60.
data750.source = '750sccm 10nmPtPd VariedT rep2.xls'
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
data750.eta_exp = (data750.HCin_raw - data750.HCout_raw) / data750.HCin_raw
data750.T_array = sp.linspace(250., 650., 100)
data750.Vdot_array = sp.array([data750.Vdot])
data750.set_eta()

data750b = ft.One_Term_Catalyst()
data750b.source = '750sccm 10nmPtPd VariedT rep3.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data750b.worksheet = xlrd.open_workbook(filename=data750b.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data750b.T_raw = sp.array(data750b.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data750b.T_exp = data750b.T_raw
data750b.HCout_raw = sp.array(data750b.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data750b.HCin_raw = sp.array(data750b.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data750b.eta_exp = (data750b.HCin_raw - data750b.HCout_raw) / data750b.HCin_raw

data1000 = ft.One_Term_Catalyst()
data1000.T_a = data250.T_a
data1000.A_arr = data250.A_arr
data1000.Vdot = 1000. * 1.e-6 / 60.
data1000.source = '1000sccm 10nmPtPd VariedT rep2.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data1000.worksheet = xlrd.open_workbook(filename=data1000.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data1000.T_raw = sp.array(data1000.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data1000.T_exp = data1000.T_raw
data1000.HCout_raw = sp.array(data1000.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data1000.HCin_raw = sp.array(data1000.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data1000.eta_exp = (data1000.HCin_raw - data1000.HCout_raw) / data1000.HCin_raw
data1000.T_array = sp.linspace(250., 650., 100)
data1000.Vdot_array = sp.array([data1000.Vdot])
data1000.set_eta()

data1000b = ft.One_Term_Catalyst()
data1000b.source = '1000sccm 10nmPtPd VariedT rep3.xls'
# Define the path to the .xls file(s) containing the conversion data.
# import the worksheet as a sheet object
data1000b.worksheet = xlrd.open_workbook(filename=data1000b.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
data1000b.T_raw = sp.array(data1000b.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
data1000b.T_exp = data1000b.T_raw
data1000b.HCout_raw = sp.array(data1000b.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
data1000b.HCin_raw = sp.array(data1000b.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
data1000b.eta_exp = (data1000b.HCin_raw - data1000b.HCout_raw) / data1000b.HCin_raw

# Plot configuration
FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE - 10
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 8

plt.figure()
plt.plot(data100.T_exp, data100.eta_exp * 100., 'ok', linestyle='',
         label='100sccm exp')
plt.plot(data100.T_array, data100.eta.T * 100., '-k',
         label='100sccm model')

plt.plot(data250.T_exp, data250.eta_exp * 100., 'sr', linestyle='',
         label='250sccm exp')
plt.plot(data250.T_array, data250.eta.T * 100., '-r',
         label='250sccm model')

plt.plot(data250b.T_exp, data250b.eta_exp * 100., 'or', linestyle='',
         label='250sccm new')

# plt.errorbar(data250osman.T_exp, data250osman.eta_exp * 100., linestyle='',
#          yerr=data250osman.errorbar * 100., label='250sccm Osman')

plt.plot(data500.T_exp, data500.eta_exp * 100., 'sg', linestyle='',
         label='500sccm exp')
plt.plot(data500.T_array, data500.eta.T * 100., '-g',
         label='500sccm model')

plt.plot(data500b.T_exp, data500b.eta_exp * 100., 'og', linestyle='',
         label='500sccm new')

plt.plot(data750.T_exp, data750.eta_exp * 100., 'sb', linestyle='',
         label='750sccm exp')
plt.plot(data750.T_array, data750.eta.T * 100., '-b',
         label='750sccm model')

plt.plot(data750b.T_exp, data750b.eta_exp * 100., 'ob', linestyle='',
         label='750sccm new')

plt.plot(data1000.T_exp, data1000.eta_exp * 100., 'sm', linestyle='',
         label='1000sccm exp')
plt.plot(data1000.T_array, data1000.eta.T * 100., '-m',
         label='1000sccm model')

plt.plot(data1000b.T_exp, data1000b.eta_exp * 100., 'om', linestyle='',
         label='1000sccm new')

plt.xlabel(r'Temperature ($^\circ$C)')
plt.ylabel('Conversion Efficiency (%)')
plt.xlim(200,450)
plt.ylim(ymax=30)
# plt.title('Conversion Efficiency v. Flow Rate')
plt.legend(loc='best')
plt.grid()
plt.savefig('Plots/model and exp.pdf')
plt.savefig('Plots/model and exp.png')

plt.show()
