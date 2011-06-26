"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import first_term as ft
import experimental_data as expdata

real_cat = ft.One_Term_Catalyst()
real_cat.T_array = sp.array([350., 400., 450., 500., 550., 600.]) 
real_cat.Vdot = sp.array([300.]) * 1.e-6 / 60. 

data1 = expdata.Data()
data1.source = '300sccm 20nmPtPd VariedT.xls'
data1.Vdot_setpoint = 300.
data1.T = sp.array([350., 400., 450., 500., 550., 600.])
data1.HCin = sp.array([3830., 3880., 3860., 3800., 3840., 3850.])
data1.HCout = sp.array([3780., 3730., 3660., 3560., 3380., 1714.]) 
data1.set_eta_T()

def get_R(real_cat, data1):
    """Returns value for R for a particular A and T_a"""
    real_cat.set_eta_dimensional()
    R = sp.sum((real_cat.eta_ij[0,:] - data1.eta_T)**2)
    return R

R = sp.empty(0)
A_arr = sp.array([1., 2., 3.]) * 1.e10
T_a = sp.array([14., 15., 16.]) * 1.e3

real_cat.T_a = T_a[0]

for j in sp.arange(3):
    real_cat.A_arr = A_arr[j]
    R = sp.append(R, get_R(real_cat, data1))
dRdA_arr = (R[1:] - R[:-1]) / (A_arr[1:] - A_arr[:-1])
d2RdA_arr2 = sp.array([(dRdA_arr[1] - dRdA_arr[0]) / (A_arr[1] - A_arr[0])])

# for k in sp.arange(3):
#     real_cat.T_a = T_a[k]
#     R = sp.append(R, get_R(real_cat, data1))
# dRdT_a = (R[4:] - R[3:-1]) / (T_a[1:] - T_a[:-1])
# d2RdT_a2 = sp.array([(dRdT_a[1] - dRdT_a[0]) / (T_a[1] - T_a[0])])

i = 2
j = 2

A_arr = sp.append(A_arr, -dRdA_arr[j-1] / d2RdA_arr2[j-2])
real_cat.A_arr = A_arr[j+1]
R = sp.append(R, get_R(real_cat, data1))
dRdA_arr = sp.append(dRdA_arr, (R[i+1] - R[i]) / (A_arr[j+1] -
                                                  A_arr[j]))   
d2RdA_arr2 = sp.append(d2RdA_arr2, (dRdA_arr[j] - dRdA_arr[j-1]) /
                       (A_arr[j+1] - A_arr[j]))  
i = i + 1
j = j + 1
