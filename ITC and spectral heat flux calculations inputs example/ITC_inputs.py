import os
import numpy as np 
from almaBTE_io import almaBTE_in, get_VCA_grids


formula='h-GaN'
VCA_builder_dir=os.getcwd()

mat='1443429'
dir_name=formula+'_'+mat
new_dir=os.path.join(os.getcwd(), dir_name)
if not os.path.isdir(new_dir):
	os.mkdir(new_dir)

# provide the path where you ran the VCABuilder run so you can read the grids of both materials. 
grids1=get_VCA_grids(os.path.join(VCA_builder_dir, formula))[0]
grids2=get_VCA_grids(os.path.join(VCA_builder_dir, mat))[0]

# "formula" is the heat source material. "formula2" is the heat sink or substrate
almaBTE_in(formula=formula, spec=False).create_steady_montecarlo(formula2=mat, 
								file_name='steady_montecarlo1d.xml',
								path=new_dir, 
								H5_root=VCA_builder_dir,
								grids1=grids1, 
								grids2=grids2,
								transport_axis=[0, 1, 0]
								)


