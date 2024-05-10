import os
import numpy as np 
from almaBTE_io import almaBTE_in


mat='h-GaN'
mat_path=os.getcwd()
IFC_2nd_sc=[3,3,3]
IFC_3rd_sc=[3,3,3]

# create a metadata file. You have to get the supercell dimensions of the 2nd and 3rd order IFCs with its nearest neighbors truncation
almaBTE_in(formula=mat).create_metadata(file_path=mat_path, IFC_2nd_sc=IFC_2nd_sc, IFC_3rd_sc=IFC_3rd_sc, IFC_nn=3)

# get the grids based on the lattice vectors of the POSCAR in the mat_path provided in the "line_kpoints" function in "alamaBTE_in" class
grids=almaBTE_in(formula=mat).line_kpoints(file_path=mat_path, length=50)

# create a VCABuilder file for the material in the mat_path directory. "mat_root_dir" variable is the directory where the material's path exist.
# Note: name the material's directory as the compound name in metadata and VCABuilder.xml files
almaBTE_in(formula=mat).create_VCABuilder(file_path=mat_path, mat_root_dir='..', file_name='VCAbuilder.xml',grids=grids)

