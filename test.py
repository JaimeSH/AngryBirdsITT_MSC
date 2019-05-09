import time
import scipy
import pylab
from yaspin.yaspin import yaspin
import pylab.plot as plt
import matplotlib.pyplot as plt


# Context manager:
with yaspin():
    time.sleep(3)  # time consuming code

# Function decorator:
@yaspin(text="Loading...")
def some_operations():
    time.sleep(3)  # time consuming code

some_operations()

lista = [0,1,2,3,4,5,6,7,8,9,10]
for c in enumerate(lista):
    con.append(c)
    plot.
    
    
import matplotlib.pyplot as plt
import numpy
import random

hl, = plt.plot([], [])

def update_line(hl, new_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data))
    plt.draw() 

for c in enumerate(lista):
    update_line(hl, [random.randint(0,10),random.randint(0,10)])
    
    
    
    
    
    
import pylab
import time
import random

dat=[0,1]
pylab.plot(dat)
pylab.ion()
pylab.draw()    
for i in range (18):
    dat.append(random.uniform(0,1))
    pylab.plot(dat)
    pylab.draw()
    time.sleep(1)