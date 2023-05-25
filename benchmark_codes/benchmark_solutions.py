import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import solve_bvp

# Deterministic model benchmark solving with boundary value problem

## A benchmark solution for the deterministic case that solves the model with shooting 
class Benchmark_deterministic: 
    def __init__(self,
                 sigma = 1.0, # log utility function, focussing on CRRA
                 rho = 0.03, #discount factor
                 alpha = 1.0/3.0, #Cobb-Douglas coffeficient
                 z = 1.0, # tfp
                 w = 1.0, # fixed wage
                 a_0 = 0.0001, # initial asset holding a(0) 
                 ):
        self.sigma = sigma # log utility function
        self.rho = rho # discount factor
        self.alpha = alpha # Cobb-Douglas coffeficient
        self.z = z # tfp
        self.w = w # fixed wage
        self.a_0 = a_0 # initial asset holding a(0) 

        # finiding the steady states
        def dynamic_root(phase_vec):
            a = phase_vec[0]
            c = phase_vec[1]
            eqn_a = (self.z) * (a**self.alpha)+ self.w - c
            eqn_c = (c/self.sigma)* (self.z*self.alpha*(a**(self.alpha-1))-self.rho)    
            return [eqn_a,eqn_c]
        
        self.initial_point = np.array([30.0, 4.0]) 
        steady_states = fsolve(dynamic_root, self.initial_point)
        self.a_star = steady_states[0]
        self.c_star = steady_states[1]

        # solving for the trajectories using boundary value problems 
        T = 200 # long time horizon to approximate infinity
        delta_a = 0.001 # distance from assets steady state at T
        self.a_T = self.a_star-delta_a # the value of the asset at T
        
        def dynamic(t, y): # t is time, y a matrix first row is y_0 for assets and the second row is y_1 for consumption
            return np.vstack((self.z*(y[0]**self.alpha) + self.w - y[1], 
                     (y[1]/self.sigma)*(z*self.alpha*(y[0]**(self.alpha-1)) -self.rho)))
        def bc(ya, yb):
            return np.array([ya[0]-self.a_0, yb[0]-self.a_T])
        
        t_grid = np.linspace(0, T, 500) # a grid for time 
        initial_guess = 1*np.ones((2, t_grid.size)) # an initial guess for the solution, the results are very sensetive to this coice
        self.solution_path = solve_bvp(dynamic, bc, t_grid, initial_guess) # Solving the boundary value problem

        self.a_path = self.solution_path.sol(t_grid)[0] # generates the path for a
        self.c_path = self.solution_path.sol(t_grid)[1] # generates the path for c
        self.time_values = t_grid
