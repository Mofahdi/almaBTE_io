## steps of running almaBTE VCABuilder and steadyMonteCarlo jobs:
1. go to h-GaN and 1443429 folders and make sure that POSCAR, FORCE_CONSTANTS, and FORCE_CONSTANTS_3RD
<br>FORCE_CONSTANTS and FORCE_CONSTANTS_3RD are fake. They only exist there to show an example
2. inside h-GaN and 1443429 folders, run: `python VCA_inputs.py` which uses methods from class ***almaBTE_in*** in **almaBTE_io.py** script
3. you will see the **_metadta** and **VCAbuilder.xml** files created in both h-GaN and 1443429
4. run almaBTE executable **VCAbuilder** to generate the phonon properties files that have the following format: compoundId_gridX_gridY_gridZ.h5
<br>Note: the files with compoundId_gridX_gridY_gridZ.h5 format that are in h-GaN and 1443429 are fake. They only exist there to show an example.
5. go back to the root directory where h-GaN and 1443429 folders are, and run: `python ITC_inputs.py` which also inherits methods from class ***almaBTE_in*** in **almaBTE_io.py** script
6. that will create **h-GaN_1443429** folder and the ***steady_montecarlo1d.xml***
7. run steady_montecarlo1d executable from almaBTE which should generate the files: **basicproperties_300K.txt** and **temperature_300K.csv** files which will enable you to calculate the interfacial thermal conductance (ITC).
8. if you want to obatain the spectral heat flux along with ITC, run `python ITC_inputs_spectral.py` which will generate **h-GaN_1443429_spectral** folder then run the steady_montecarlo1d executable.
<br>Note: an example of reading the ITC outputs and spectral heat flux aross the two material layers figure is shown in **ITC and spectral heat flux outputs example**
