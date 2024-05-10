import os
from almaBTE_io import almaBTE_output


basic_props_path=os.path.join(os.getcwd(), 'basicproperties_300K.txt')
temp_path=os.path.join(os.getcwd(), 'temperature_300K.csv')
almaBTE_out=almaBTE_output.from_almaBTE_outputs(basic_props_path=basic_props_path, temp_path=temp_path)

# alamBTE outputs
print(almaBTE_out.l1_thick)
print(almaBTE_out.l2_thick)
print(almaBTE_out.heat_flux)
print(almaBTE_out.temp_diff)
print(almaBTE_out.eff_conductance)
print(almaBTE_out.calc_ITC())