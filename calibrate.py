"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import first_term as ft
reload(ft)
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

real_cat.A_arr = 6.e10 - 2000.
real_cat.T_a = 13.2e3

Z_list = list()
a_list = list()
a_mag = sp.empty(0)

for i in sp.arange(4):
    real_cat.set_eta_dim()
    eta = real_cat.eta_dim.reshape(6)

    D = sp.array(data1.eta_T - eta)
    d_eta_dA_arr = real_cat.perturb_A_arr()
    d_eta_dT_a = real_cat.perturb_T_a()

    Z = sp.array([d_eta_dA_arr, d_eta_dT_a]).reshape(6,2)
    Z_list.append(Z)

    delta_a_i = sp.dot(sp.linalg.inv(sp.dot(Z.T, Z)), sp.dot(Z.T, D))
    a_list.append(delta_a_i)
    a_mag = sp.append(a_mag, sp.sqrt(a_list[i][0]**2 + a_list[i][1]**2))

    real_cat.A_arr = real_cat.A_arr + delta_a_i[0]
    real_cat.T_a = real_cat.T_a + delta_a_i[1]
