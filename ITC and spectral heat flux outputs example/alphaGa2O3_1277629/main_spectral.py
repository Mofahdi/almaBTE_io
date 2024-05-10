import os
from almaBTE_io import almaBTE_output


basic_props_path=os.path.join(os.getcwd(), 'basicproperties_300K.txt')
temp_path=os.path.join(os.getcwd(), 'temperature_300K.csv')
ITC_calc=almaBTE_output.from_almaBTE_outputs(basic_props_path=basic_props_path, temp_path=temp_path)
ITC_calc.spec=True
# print(ITC_calc.calc_ITC())
# print(ITC_calc.temp_diff)
# print(ITC_calc.eff_conductance)
ITC_calc.get_spectral_flux_plot(path='.',dpi=500)