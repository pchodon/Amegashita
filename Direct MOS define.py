# Logging information about the simulation
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Spice.Netlist import Circuit # for creating circuits
from PySpice.Unit import *                # for adding units

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size': 14,
                            'text.usetex': True, # use TeX backend
                            'mathtext.fontset': 'cm', # computer modern
                            'mathtext.rm': 'serif'})




def mos_circuit(params=None):
    
    d = {'vg':1, 'vd':2, 'length':1E-6, 'width':10E-6}
    if params:
        for k, v in params.items():
            d[k] = v
        
    circuit = Circuit('MOS circuit')
    circuit.model('NMOS-SH', 'nmos', Kp=190E-6, Vto=0.57, Lambda=0.16, Gamma=0.50, Phi=0.7)
    circuit.V('G', 'VG', 0, d['vg'])
    circuit.V('D', 'VD', 0, d['vd'])
    circuit.M(1, 'VD', 'VG', 0, 0, model='NMOS-SH', l=d['length'], w=d['width'])
    return circuit


def sweep_source(first_source_name, first_source_range, second_source_name, second_source_range):
    y = []
    
    for s in second_source_range:
        circuit = mos_circuit({f'{second_source_name}':s})
        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        if first_source_name == 'vg':
            analysis = simulator.dc(VG=first_source_range)
        else:
            analysis = simulator.dc(VD=first_source_range)
        y.append(- np.array(analysis.branches['vd']))
        
    x = np.array(analysis.nodes[first_source_name])
    
    return x,y 

#def plot(x_label, y_label, title, first_source_name, x, y, second_source_name, second_source_range, func=lambda x: x):
def plot(x_label, y_label, title, first_source_name, x, y, second_source_name, second_source_range):
 
    print(x,y)
   
    
    
# importing the modules


    
first_source_name = 'vd'
first_source_range = slice(0, 3, .01)
second_source_name = 'vg'
second_source_range = np.arange(0, 3, 0.5)

x, y = sweep_source(first_source_name, first_source_range, second_source_name, second_source_range)

x_label ="$V_{DS}\ [V]$"
y_label ="$I_{D}\ [A]$"
title ="MOS Output Characteristics"

plot(x_label, y_label, title, first_source_name, x, y, second_source_name, second_source_range)



