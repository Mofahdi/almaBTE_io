import os
from almaBTE_io import almaBTE_output


basic_props_path=os.path.join(os.getcwd(), 'basicproperties_300K.txt')
temp_path=os.path.join(os.getcwd(), 'temperature_300K.csv')
almaBTE_out=almaBTE_output.from_almaBTE_outputs(basic_props_path=basic_props_path, temp_path=temp_path)

# alamBTE outputs
print('layer 1 thickness:', almaBTE_out.l1_thick)
print('layer 2 thickness:', almaBTE_out.l2_thick)
print('heat flux:', almaBTE_out.heat_flux)
print('temperature difference:', almaBTE_out.temp_diff)
print('effective conductance:', almaBTE_out.eff_conductance)
print('ITC:', almaBTE_out.calc_ITC())
