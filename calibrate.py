"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import experimental_data as expdata
reload(expdata)

data1 = expdata.Data()
data1.source = '300sccm 20nmPtPd VariedT.xls'
data1.Vdot = sp.array([300.]) * 1.e-6 / 60. 

# data1.T_array = sp.array([350., 400., 450., 500., 550., 600.])
# data1.HCin = sp.array([3830., 3880., 3860., 3800., 3840., 3850.])
# data1.HCout = sp.array([3780., 3730., 3660., 3560., 3380., 1714.])

data1.T_array = sp.array([350., 500., 600.])
data1.HCin = sp.array([3830., 3800., 3850])
data1.HCout = sp.array([3780., 3560., 3380]) 

data1.set_eta()

data1.A_arr_i = sp.linspace(1., 500., 50) * 1.e10 
data1.T_a_j = sp.linspace(10., 20., 50) * 1.e3
data1.S_r_ij = sp.zeros([sp.size(data1.A_arr_i), sp.size(data1.T_a_j)])

for i in sp.arange(sp.size(data1.A_arr_i)):
    for j in sp.arange(sp.size(data1.T_a_j)):
        data1.A_arr = data1.A_arr_i[i]
        data1.T_a = data1.T_a_j[j]        
        data1.set_eta()
        data1.S_r_ij[i,j] = data1.get_S_r()
        

