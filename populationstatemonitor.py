# -*- coding: utf-8 -*-
from brian import *
import types

class PopulationStateMonitor(StateMonitor):
    """
    Adapted from the Brian standard StateMonitor, it records the population average of a given variable every timestep
    """
    
    def __init__(self,P,varname,clock=None,record=True,timestep=1,when='end'):
        StateMonitor.__init__(self,P,varname,clock,record,timestep,when)
        
    def __call__(self):
        '''
        This function is called every time step.
        '''
        V=self.P.state_(self.varname)
        self._mu+=V.mean()
        self._sqr+=V.mean()*V.mean()
        if self.record is not False and self.curtimestep==self.timestep:
            i = self._recordstep
            if self._values is None:
                self._values = []
                self._times = []
            if type(self.record)!=types.BooleanType:
                self._values.append(V[self.record].mean()) 
            elif self.record is True:
                self._values.append((V.copy()).mean())
            self._times.append(self.clock.t)
            self._recordstep += 1
        self.curtimestep-=1
        if self.curtimestep==0: self.curtimestep=self.timestep
        self.N+=1

    def reinit(self):
        self._values = []
        self._times = []
        ri = self.get_record_indices()
        self._values_cache = zeros((1, 0))
        self.N = 0
        self._recordstep = 0
        self._mu = zeros(len(self.P))
        self._sqr = zeros(len(self.P))

