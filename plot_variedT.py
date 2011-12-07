"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import first_term as ft
import experimental_data as expdata

mpl.close('all')

real_cat = ft.One_Term_Catalyst()
real_cat.A_arr = 50.e10
real_cat.T_a = 16.e3

real_cat.T_array = np.arange(200., 650., 10.)
real_cat.Vdot = np.array([100., 300.]) * 1.e-6 / 60. 

real_cat.set_Da()
real_cat.set_Pe()
real_cat.set_eta_dim()

data1 = expdata.Data()
data1.source = '300sccm 20nmPtPd VariedT.xls'
data1.Vdot_setpoint = 300.
data1.T = np.array([350., 400., 450., 500., 550., 600.])
data1.HCin = np.array([3830., 3880., 3860., 3800., 3840., 3850.])
data1.HCout = np.array([3780., 3730., 3660., 3560., 3380., 1714.]) 
data1.set_eta_T()

data2 = expdata.Data()
data2.source = '100sccm 20nmPtPd VariedT.xls'
data2.Vdot_setpoint = 100.
data2.T = np.array([450., 475., 500., 500., 550., 600.]) 
data2.HCin = np.array([5620., 6450., 6450., 5620., 4470., 3800.]) 
data2.HCout = np.array([4290., 2660., 1757., 3120., 334., 115.])   
data2.set_eta_T()

data3 = expdata.Data()
data3.source = '100sccm 20nmPtPd VariedT rep1.xls'
data3.Vdot_setpoint = 100.
data3.T = np.array([450., 475., 500., 525., 550., 575., 600., 600.])
data3.HCin = np.array([4310., 4270., 4240., 4250., 4120., 4080.,
                       3170., 4330.])
data3.HCout = np.array([3410., 2960., 2390., 1629., 1233., 620., 350.,
                        492.])
data3.set_eta_T()

data4 = expdata.Data()
data4.source = '100sccm 20nmPtPd VariedT rep2.xls'
data4.Vdot_setpoint = 100.
data4.T = np.array([425., 450., 475., 500., 525., 550., 575., 600., 600.])
data4.HCin = np.array([3920., 3860., 3850., 3820., 3830., 3640.,
                       3760., 2890., 3920.])
data4.HCout = np.array([3470., 3280., 2950., 2480., 2160., 1489.,
                        841., 390., 636.])
data4.set_eta_T()

data_set = (data1, data2, data3, data4)

# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

mpl.figure()
for i in np.arange(np.size(real_cat.eta_dim,0)):
    mpl.plot(real_cat.T_array, real_cat.eta_dim[i,:]*1e2,
             label=str(real_cat.Vdot[i] * 60 * 1e6) + ' sccm')  

for j in range(len(data_set)):
    mpl.plot(data_set[j].T, data_set[j].eta_T*1e2,
    label=str(data_set[j].Vdot_setpoint) + ' sccm, exp data',
    marker='x', linestyle='None') 

mpl.xlabel('Temperature (C)')
mpl.ylabel('Conversion Efficiency (%)')
mpl.title('Conversion Efficiency v. Flow Rate')
mpl.legend(loc='best')
mpl.grid()
mpl.savefig('Plots/model and exp.pdf')
mpl.savefig('Plots/model and exp.png')

mpl.show()
