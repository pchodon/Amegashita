###Inverter-Characteristics

import numpy as np
import matplotlib.pyplot as plt

import sys
import os

cls = lambda: os.system('clear')
cls()

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Spice.Simulation import CircuitSimulation

'''
#Check Default Simulator
import PySpice
PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR
'''



class simulate_circuit():

    def __init__(self, Vdd =1.1,lp=130,wp=2500,ln=130,wn=1000):

        ###Title###
        self.circuit = Circuit('Inverter Transfer Characteristics') #Name given to circuit i.e. Netlist Title

        ###Supplies###
        # Define the Power and various DC supply voltage value
        self.Vgate = self.circuit.V('gate', 'gatenode', self.circuit.gnd, 0@u_V)
        self.Vpwr  = self.circuit.V('pwr', 'vdd', self.circuit.gnd, u_V(Vdd))
        self.Vdd = Vdd
        ###MOS Models & Circuit Elements###
        self.circuit.include("//home/astra/Downloads/techfile130.pm")

        self.circuit.MOSFET(1, 'vout', 'gatenode', self.circuit.gnd, self.circuit.gnd, model='nmos', l=nano(ln),w=nano(wp))
        self.circuit.MOSFET(2, 'vout', 'gatenode', 'vdd', 'vdd', model='pmos',l=nano(ln),w=nano(wp))


    def update_size(self,nmos_w=1000,pmos_w=2500):
        self.circuit.M1.width = nano(nmos_w)
        self.circuit.M2.width = nano(pmos_w)

    def simulate(self):#Simulator Object
        self.simulator = self.circuit.simulator(temperature=25, nominal_temperature=25)
        #CircuitSimulation.save(M1[gm])
        self.analysis = self.simulator.dc(Vgate =slice(0,self.Vdd,0.01)) #Slice is like range!
        return self.analysis

    ###Plot###
    def plot(self,analysis):
        figure, ax = plt.subplots(figsize=(20, 10))
        ax.plot(analysis['gatenode'], analysis['vout'],analysis['gatenode'],analysis['gatenode'] )
        ax.plot(analysis['gatenode'], u_mA(-analysis.Vpwr))
        ax.legend('Inv characteristic')
        ax.grid()
        ax.set_xlabel('Vgate [V]')
        ax.set_ylabel('Vout [V]')
        plt.tight_layout()
        plt.show()


        return


    def trigger_pt(self,analysis):
        out  = analysis['vout'].as_ndarray()
        inpt = analysis['gatenode'].as_ndarray()

        diff = np.abs(out-inpt)
        trigger_pos = np.argmin(diff)
        trigger_val = out[trigger_pos]

        return trigger_val,np.min(diff)

if __name__ == '__main__':

    inv = simulate_circuit()
    print(inv.circuit)

    analysis_run = inv.simulate()
    inv.plot(analysis_run)

    for i in range(1000,10000,2000):
         inv.update_size(i)
         analysis_run = inv.simulate()
         trigger_val,trigger_diff = inv.trigger_pt(analysis_run)
         inv.plot(analysis_run)
         print("Check:",[inv.circuit.M1.width,inv.circuit.M2.width,trigger_val,trigger_diff])
