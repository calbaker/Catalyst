"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import experimental_data as expdata
reload(expdata)

data1 = expdata.Data()
data1.source = 'Osman July 3'
data1.Vdot = sp.array([250.]) * 1.e-6 / 60. 

data1.T_array = sp.arange(350., 625., 25.)
data1.HCin = sp.array([
data1.HCout = sp.array([
data1.set_eta()

data2 = expdata.Data()
data2.source = 'Osman July 3'
data2.Vdot = sp.array([250.]) * 1.e-6 / 60.

data2.T_array = sp.arange(350., 625., 25.)
data2.HCin = sp.array([3895., 3740., 3510., 2700., 1924., 220., 98., 41.])     
data2.HCout = sp.array([4950., 4920., 5170., 5450., 5560., 5040., 4500., 4620.])
data2.set_eta()

data3 = expdata.Data()
data3.source = 'Osman July 3'
data3.Vdot = sp.array([250.]) * 1.e-6 / 60. 

data3.T_array = sp.arange(350., 625., 25.)
data3.HCin = sp.array([ 3890., 3720., 3500., 2740., 1935., 225., 103., 45.])
data3.HCout = sp.array([4940., 4950., 5140., 5560., 5580., 5050., 4540., 4610.])
data3.set_eta()

data_all = expdata.Data()
data_all.source = "average of all data points"
data_all.eta_exp = ( (data3.eta_exp + data2.eta_exp + data1.eta_exp) /
3. )
data_all.eta_model = data3.eta_model

data_all.A_arr_i = sp.linspace(25., 75., 100) * 1.e15
data_all.T_a_j = sp.linspace(26., 27., 25) * 1.e3
data_all.S_r_ij = sp.zeros([sp.size(data_all.A_arr_i),
                            sp.size(data_all.T_a_j)])
data_all.Vdot = sp.array([250.]) * 1.e-6 / 60.
data_all.T_array = sp.arange(350., 625., 25.)

for i in sp.arange(sp.size(data_all.A_arr_i)):
    print i, 'of', sp.size(data_all.A_arr_i)
    for j in sp.arange(sp.size(data_all.T_a_j)):
        data_all.A_arr = data_all.A_arr_i[i]
        data_all.T_a = data_all.T_a_j[j]        
        data_all.set_eta_dim()
        data_all.eta_model = data_all.eta_dim
        data_all.S_r_ij[i,j] = data_all.get_S_r()
        
# Z_list = list()
# a_list = list()
# D_list = list()

# data_all.A_arr = 5.e16
# data_all.T_a = 26900.

# for i in sp.arange(2):
#     data_all.set_eta()
#     data_all.eta_model = data_all.eta_model.reshape(sp.size(data_all.T_array)) 

#     D = sp.array(data_all.eta_exp - data_all.eta_model)
#     D_list.append(D)
#     d_eta_dA_arr = data_all.perturb_A_arr()
#     d_eta_dT_a = data_all.perturb_T_a()

#     Z = sp.array([d_eta_dA_arr,
#     d_eta_dT_a]).reshape(sp.size(data_all.T_array),2) 
#     Z_list.append(Z)

#     delta_a = sp.dot(sp.linalg.inv(sp.dot(Z.T, Z)), sp.dot(Z.T, D))
#     print delta_a
#     a_list.append(delta_a)

#     data_all.A_arr = data_all.A_arr + delta_a[0]
#     data_all.T_a = data_all.T_a + delta_a[1]
