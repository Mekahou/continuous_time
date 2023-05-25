import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from utilities import plot_params

### finding and adding the path for the benchmark code
main_dir =  os.path.dirname(os.path.dirname(__file__)) # finding the main dirctory address
benchmark_codes_path = os.path.join(main_dir, 'benchmark_codes') # creating the path for benchmark codes
sys.path.append(benchmark_codes_path)
#for i in sys.path: # checking it is in there
    #print(i) 
###---------------------------------------------------------------------

from benchmark_solutions import Benchmark_deterministic

### Setting the path where the plot is going to get saved
output_dir = "./figures"
plot_name = "deterministic_sequential"
output_path = output_dir + "/" + plot_name + ".pdf"
###---------------------------------------------------------------------

### Getting the benchmark solution 
benchmark_solution = Benchmark_deterministic()
a_path = benchmark_solution.a_path
c_path = benchmark_solution.c_path
c_ss = benchmark_solution.c_star
a_ss = benchmark_solution.a_star
t = benchmark_solution.time_values
###---------------------------------------------------------------------

### Plotting the resultes
params = plot_params((8, 3.5))
plt.rcParams.update(params)


ax_a = plt.subplot(121)
plt.plot(t, a_path, color='k')
ax_a.axhline(a_ss, linestyle='--', color='k', label = r"$a^*$")
plt.title(r"Equilibrium path for assets $a(t)$")
plt.legend(prop={"size": params["font.size"]}, loc= 'lower right' )
plt.xlabel(r"Time(t)")

ax_c = plt.subplot(122)
plt.plot(t,c_path, color='b')
ax_c.axhline(c_ss, linestyle='--', color='b', label = r"$c^*$")
plt.title(r"Equilibrium path for consumption $c(t)$")
plt.xlabel(r"Time(t)")
plt.legend(prop={"size": params["font.size"]}, loc= 'lower right' )
plt.tight_layout()
###---------------------------------------------------------------------
plt.savefig(output_path)