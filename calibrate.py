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

data1.T_array = sp.array([350., 400., 450., 500., 550., 600.])
data1.HCin = sp.array([3830., 3880., 3860., 3800., 3840., 3850.])
data1.HCout = sp.array([3780., 3730., 3660., 3560., 3380., 1714.])

# data1.T_array = sp.array([350., 500., 600.])
# data1.HCin = sp.array([3830., 3800., 3850])
# data1.HCout = sp.array([3780., 3560., 3380]) 

# data1.T_array = sp.array([500., 600.])
# data1.HCin = sp.array([3800., 3850])
# data1.HCout = sp.array([3560., 3380]) 

# data1.A_arr_i = sp.linspace(25., 75., 100) * 1.e15
# data1.T_a_j = sp.linspace(26., 27., 25) * 1.e3
# data1.S_r_ij = sp.zeros([sp.size(data1.A_arr_i), sp.size(data1.T_a_j)])

# for i in sp.arange(sp.size(data1.A_arr_i)):
#     print i, 'of', sp.size(data1.A_arr_i)
#     for j in sp.arange(sp.size(data1.T_a_j)):
#         data1.A_arr = data1.A_arr_i[i]
#         data1.T_a = data1.T_a_j[j]        
#         data1.set_eta()
#         data1.S_r_ij[i,j] = data1.get_S_r()
        
Z_list = list()
a_list = list()
D_list = list()

data1.A_arr = 5.e16
data1.T_a = 26900.

for i in sp.arange(2):
    data1.set_eta()
    data1.eta_model = data1.eta_model.reshape(sp.size(data1.T_array)) 

    D = sp.array(data1.eta_exp - data1.eta_model)
    D_list.append(D)
    d_eta_dA_arr = data1.perturb_A_arr()
    d_eta_dT_a = data1.perturb_T_a()

    Z = sp.array([d_eta_dA_arr,
    d_eta_dT_a]).reshape(sp.size(data1.T_array),2) 
    Z_list.append(Z)

    delta_a = sp.dot(sp.linalg.inv(sp.dot(Z.T, Z)), sp.dot(Z.T, D))
    print delta_a
    a_list.append(delta_a)

    data1.A_arr = data1.A_arr + delta_a[0]
    data1.T_a = data1.T_a + delta_a[1]
