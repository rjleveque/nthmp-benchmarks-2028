
from pylab import *

from clawpack.clawutil.util import fullpath_import
try:
    from nthmp28.radial_bowl import true_solution as TS
except:
    print('*** The git repository directory needs to be on your Python path')
    raise


def topo_bowl(r):
    z = -TS.D0 * (1 - r**2/TS.L**2)
    return z


redge = linspace(0, 240, 2401)
zedge = topo_bowl(redge)

topofile = 'topo_bowl.asc'
with open(topofile,'w') as f:
    f.write(f'{len(redge)}   # number of topo edges\n')
    for k in range(len(redge)):
        f.write(f'{redge[k]:10.3f}   {zedge[k]:10.3f}\n')

print(f'Created {topofile}')
