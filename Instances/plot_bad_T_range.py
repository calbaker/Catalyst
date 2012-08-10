"""Generates plot of hydrocarbon conversion efficiency versus temperature comparing
performance of catalyst with control experiment.  This plot is used in paper.
"""

import numpy as np
import matplotlib.pyplot as plt
import xlrd
import os
import sys

cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import experimental_data as expdata
reload(expdata)
import catalyst 
reload(catalyst)

plt.close('all')

cat = catalyst.Catalyst()
cat.Vdot = 750. * 1.e-6 / 60.

cat.source = '../data/750sccm 10nmPtPd VariedT rep2.xls'
# Define the path to the .xls file(s) containing the conversion cat.
# import the worksheet as a sheet object
cat.worksheet = xlrd.open_workbook(filename=cat.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
cat.T_raw = np.array(cat.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
cat.T_exp = cat.T_raw
cat.HCout_raw = np.array(cat.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
cat.HCin_raw = np.array(cat.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
cat.eta_exp = (cat.HCin_raw - cat.HCout_raw) / cat.HCin_raw

cat.Vdot_array = np.array([cat.Vdot])
cat.T_array = np.linspace(cat.T_raw.min(), cat.T_raw.max(), 50.)

cat.A_arr = 1.129e7
cat.T_a = 6822.

cat.set_eta_ij()

cat_empty = catalyst.Catalyst()
# cat_empty.source = 'alumina_holder_only.xls' # this data needs to be
# cleared with Hall and Ezekoye
cat_empty.source = '1000sccm empty tube rep2.xls'
cat_empty.A_arr = A_arr
cat_empty.T_a = T_a
# Define the path to the .xls file(s) containing the conversion cat.
# import the worksheet as a sheet object
cat_empty.worksheet = xlrd.open_workbook(filename=cat_empty.source).sheet_by_index(0)
# Import conversion data from worksheet and store as scipy arrays
cat_empty.T_raw = np.array(cat_empty.worksheet.col_values(0, start_rowx=4, 
                                                 end_rowx=None)) 
cat_empty.T_exp = cat_empty.T_raw
cat_empty.HCout_raw = np.array(cat_empty.worksheet.col_values(4, start_rowx=4, 
                                                     end_rowx=None))
cat_empty.HCin_raw = np.array(cat_empty.worksheet.col_values(8, start_rowx=4,
                                                    end_rowx=None))
cat_empty.eta_exp = (cat_empty.HCin_raw - cat_empty.HCout_raw) / cat_empty.HCin_raw


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

plt.plot(cat.T_exp, cat.eta_exp * 100., 'sr', linestyle='',
         label='750sccm exp')
plt.plot(cat.T_array, cat.eta.T * 100., '-r',
         label='750sccm model')

plt.plot(cat_empty.T_exp, cat_empty.eta_exp * 100., 'om', linestyle='',
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
