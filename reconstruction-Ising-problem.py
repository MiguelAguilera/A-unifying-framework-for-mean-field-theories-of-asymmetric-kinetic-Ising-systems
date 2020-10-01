#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 15:45:08 2018

@author: maguilera
"""

from mf_ising import mf_ising
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

def nsf(num, n=4):
    """n-Significant Figures"""
    numstr = ("{0:.%ie}" % (n-1)).format(num)
    return float(numstr)

size = 512

R = 1000000
gamma1 = 0.5
gamma2 = 0.1

T = 128
iu1 = np.triu_indices(size, 1)

B = 201
#B = 21


betas = 1 + np.linspace(-1, 1, B) * 0.3


filename1 = 'data/data-gamma1-' + str(gamma1) + '-gamma2-' + str(
        gamma2) + '-s-' + str(size) + '-R-' + str(R) + '-beta-1.0.npz'
data1 = np.load(filename1)
s0 = data1['s0']
del data1

modes=['d','r']        # Direct and reconstruction modes
mode = modes[0]
#mode = modes[1]
#for ib in range(len(betas)):
for ib in range(123,200):
    beta_ref = round(betas[ib], 3)
    print(beta_ref*1000)
    exit()

    # Load data
    
    filename = 'data/results/inverse_100_R_' + str(R) +'.npz'
    print(beta_ref,mode)
    
    data = np.load(filename)
    HP_t1_t = data['HP_t1_t']*beta_ref
    JP_t1_t = data['JP_t1_t']*beta_ref
    HP_t = data['HP_t']*beta_ref
    JP_t = data['JP_t']*beta_ref
    HP_t1 = data['HP_t1']*beta_ref
    JP_t1 = data['JP_t1']*beta_ref
    HP2_t = data['HP2_t']*beta_ref
    JP2_t = data['JP2_t']*beta_ref
    

    J=data['J']*beta_ref
    H=data['H']*beta_ref
    del data
#    plt.figure()
#    plt.plot(H,HP2_t,'*')
#    plt.plot([np.min(H),np.max(H)],[np.min(H),np.max(H)],'k')
#    plt.figure()
#    plt.plot(J.flatten(),JP2_t.flatten(),'.')
#    plt.plot([np.min(J),np.max(J)],[np.min(J),np.max(J)],'k')
#    
#    plt.figure()
#    plt.plot(H,HP_t,'*')
#    plt.plot([np.min(H),np.max(H)],[np.min(H),np.max(H)],'k')
#    plt.figure()
#    plt.plot(J.flatten(),JP_t.flatten(),'.')
#    plt.plot([np.min(J),np.max(J)],[np.min(J),np.max(J)],'k')

#    print('P',np.mean((H-HP_t)**2),np.mean((J-JP_t)**2))
#    print('P2',np.mean((H-HP2_t)**2),np.mean((J-JP2_t)**2))
#    plt.show()

    # Run Plefka[t-1,t], order 2
    I = mf_ising(size)
    if mode == 'd':
        I.H = H.copy()
        I.J = J.copy()
    elif mode =='r':
        I.H = HP_t1_t.copy()
        I.J = JP_t1_t.copy()
    I.initialize_state(s0)
    for t in range(T):
        print('beta',beta_ref,'P_t1_t_o2', str(t) + '/' + str(T),nsf(np.mean(I.m)), nsf(np.mean(I.C[iu1])), nsf(np.mean(I.D)))
        I.update_P_t1_t_o2()
    mP_t1_t_final = I.m
    CP_t1_t_final = I.C
    DP_t1_t_final = I.D

    # Run Plefka[t], order 2
    I = mf_ising(size)
    if mode == 'd':
        I.H = H.copy()
        I.J = J.copy()
    elif mode =='r':
        I.H = HP_t.copy()
        I.J = JP_t.copy()
    I.initialize_state(s0)
    for t in range(T):
        print('beta',beta_ref,'P_t_o2', str(t) + '/' + str(T),nsf(np.mean(I.m)), nsf(np.mean(I.C[iu1])), nsf(np.mean(I.D)))
        I.update_P_t_o2()
    mP_t_final = I.m
    CP_t_final = I.C
    DP_t_final = I.D

    # Run Plefka2[t], order 2
    I = mf_ising(size)
    if mode == 'd':
        I.H = H.copy()
        I.J = J.copy()
    elif mode =='r':
        I.H = HP2_t.copy()
        I.J = JP2_t.copy()
    I.initialize_state(s0)
    for t in range(T):
        print('beta',beta_ref,'P2_t_o2', str(t) + '/' + str(T),nsf(np.mean(I.m)), nsf(np.mean(I.C[iu1])), nsf(np.mean(I.D)))
        I.update_P2_t_o2()
    mP2_t_final = I.m
    CP2_t_final = I.C
    DP2_t_final = I.D

    # Run Plefka[t-1], order 1
    I = mf_ising(size)
    if mode == 'd':
        I.H = H.copy()
        I.J = J.copy()
    elif mode =='r':
        I.H = HP_t1.copy()
        I.J = JP_t1.copy()
    I.initialize_state(s0)
    for t in range(T):
        print('beta',beta_ref,'P_t1_o1', str(t) + '/' + str(T),nsf(np.mean(I.m)), nsf(np.mean(I.C[iu1])), nsf(np.mean(I.D)))
        I.update_P_t1_o1()
    mP_t1_final = I.m
    CP_t1_final = I.C
    DP_t1_final = I.D

    # Save results to file

    filename = 'data/reconstruction/transition_'+mode+'_' + str(int(round(beta_ref * 1000))) + '_R_' + str(R) +'.npz'
    np.savez_compressed(filename,
                        mP_t1_t=mP_t1_t_final,
                        mP_t=mP_t_final,
                        mP_t1=mP_t1_final,
                        mP2_t=mP2_t_final,
                        CP_t1_t=CP_t1_t_final,
                        CP_t=CP_t_final,
                        CP_t1=CP_t1_final,
                        CP2_t=CP2_t_final,
                        DP_t1_t=DP_t1_t_final,
                        DP_t=DP_t_final,
                        DP_t1=DP_t1_final,
                        DP2_t=DP2_t_final)

