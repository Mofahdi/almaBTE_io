# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 08:42:42 2022

@author: MALFAHDI
"""

#%%
# https://almabte.bitbucket.io/docs/examples/
import os, re, fnmatch
import numpy as np
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
from jarvis.core.atoms import Atoms
from jarvis.core.kpoints import Kpoints3D

def get_VCA_grids(mat_path):
	files=[]
	for file in os.listdir(mat_path):
		if fnmatch.fnmatch(file, '*_*_*.h5'):
			files.append(file)

	for file in files:
		pat=re.findall('\d+', file)
		grids_pat=re.findall('_\d+_\d+_\d+.', file)
		grids=re.findall('\d+', str(grids_pat))
		mat_pat=re.findall('(.*?)_', file)

	grids_int=list(map(int, grids))

	return grids_int, mat_pat


    
class almaBTE_output:
	def __init__(
				self, 
				l1_thick, 
				l2_thick, 
				heat_flux, 
				temp_diff, 
				eff_cond, 
				spec=False
				):
		self.l1_thick=l1_thick
		self.l2_thick=l2_thick
		self.heat_flux=heat_flux
		self.temp_diff=temp_diff
		self.eff_conductance=eff_cond
		self.spec=spec
        
	@classmethod
	def from_almaBTE_outputs(
							cls, 
							basic_props_path='basicproperties_300K.txt', 
							temp_path='temperature_300K.csv'
							):
		with open(basic_props_path, 'r') as f:
			text=f.readlines()
			l1_thick=float(text[0].strip('\n').replace('(', '').replace(')', '').split()[3])
			l1_thick_unit=text[0].strip('\n').replace('(', '').replace(')', '').split()[4]
			#print(l1_thick_unit)
			if l1_thick_unit=='um':
				l1_thick=l1_thick*1000

			l2_thick=float(text[1].strip('\n').replace('(', '').replace(')', '').split()[3])
			l2_thick_unit=text[1].strip('\n').replace('(', '').replace(')', '').split()[4]
			if l2_thick_unit=='um':
				l2_thick=l2_thick*1000
			heat_flux_unit=text[6].strip('\n').split()[2]
			heat_flux=float(text[6].strip('\n').split()[1]);

		if heat_flux_unit=='GW/m^2':
			# this is done to get ITC in MW/km^2
			heat_flux=float(heat_flux*1000.0) 

		eff_conductance=float(text[11].split()[1])
		eff_conductance_unit=text[11].split()[2]
		if eff_conductance_unit=="kW/K-m^2":
			eff_conductance=eff_conductance/1000.0
                
		data=pd.read_csv(temp_path, names=['dist', 'temp'])
		dat_l1_thick=data[data['dist']<l1_thick]
		dat_l2_thick=data[data['dist']>l1_thick]
		temp1=float(np.array(dat_l1_thick.loc[:, 'temp'])[-1])
		temp2=float(np.array(dat_l2_thick.loc[:, 'temp'])[0])
		temp_diff=temp1-temp2
		return cls(l1_thick, l2_thick, heat_flux, temp_diff, eff_conductance)
    
	def calc_ITC(self):
		ITC=float(self.heat_flux/self.temp_diff)
		return ITC

	def get_spectral_flux_plot(
								self, 
								path, 
								T=300, 
								title=None, 
								fig_name=None, 
								fig_format='jpeg', 
								dpi=400
								):
		if self.spec==False:
			warnings.warn("Please check your calculations! did you includee spectral heat flux in your calculations?")
		csv_files_un=[]
		for file in os.listdir(path):
			if fnmatch.fnmatch(file, 'spectralflux_surface_*'):
				csv_files_un.append(file)
		ph_freq=[]; flux=[]
		for i in range(len(csv_files_un)):
			#print(csv_files_un[i])
			file='spectralflux_surface_'+str(i+1)+'_'+str(T)+'K.csv'
			#print(file)
			df=pd.read_csv(file)
			ph_freq.append(df.iloc[:, 0])
			flux.append(df.iloc[:, 1]) 	
		ph_freq=np.array(ph_freq)
		flux=np.array(flux)
        
		nspace=np.linspace(1, flux.shape[0], flux.shape[0])
		max_flux=max(flux.flatten())
		min_flux=min(flux.flatten())
		max_ph_freq=max(ph_freq.flatten())/2/np.pi
		x_vals=np.empty(flux.shape[1]).copy()

		plt.figure(figsize=(8, 6))
		for dist in range(len(nspace)):
			x_vals[0:flux.shape[1]]=dist+1
			ph_freq_THz=ph_freq[dist, :]/2/np.pi
			plt.scatter(x_vals, ph_freq_THz, c=flux[dist, :], cmap='jet', vmin=min_flux, vmax=max_flux)
		cb_ticks=np.linspace(min_flux, max_flux, 10, endpoint=True)
		cb=plt.colorbar(label='Flux (W/m$^2$)', orientation="vertical", ticks=cb_ticks)
		cb.set_ticks(cb_ticks)
		ax = cb.ax
		text = ax.yaxis.label
		font = matplotlib.font_manager.FontProperties(size=12)
		text.set_font_properties(font)
		cb.ax.tick_params(labelsize=11)

		#if title==None:
		#	title='{formula_1}-{formula_2} spectral heat flux'.format(formula_1=self.formula_1, formula_2=self.formula_2)
		plt.title(title, fontsize=14)
		plt.xlabel('Position (nm)', fontsize=13)
		plt.xticks(fontsize=12)
		plt.ylabel('Phonon ang. freq. (THz)', fontsize=13)
		y_ticks=np.linspace(0, max_ph_freq, 8)
		plt.yticks(y_ticks, fontsize=12)
		plt.tight_layout()
		plt.xlim([0, max(nspace)+1])
		plt.ylim([0, max_ph_freq])
		#if fig_name==None:
		#	fig_name='%s-%s_spec_flux_fig'%(self.formula_1, self.formula_2)
		fig_name='ITC_spectral_heat_flux'
		plt.savefig(fig_name+'.'+fig_format, dpi=dpi)




class almaBTE_in:
	def __init__(
				self, 
				formula, 
				spec=False
				):
		self.formula=formula
		self.spec=spec
	
	def create_metadata(
						self, 
						file_path, 
						IFC_2nd_sc, 
						IFC_3rd_sc, 
						IFC_nn=3,
						):
		filename=os.path.join(file_path, '_metadata')
		with open(filename, 'w') as f:
			f.write('Compound: '+self.formula+'\n')
			f.write(f'2nd IFC supercell: (n1,n2,n3) = {IFC_2nd_sc[0]} {IFC_2nd_sc[1]} {IFC_2nd_sc[2]}\n')
			f.write(f"3rd IFC supercell: (n1',n2',n3', cutoff) = {IFC_3rd_sc[0]} {IFC_3rd_sc[1]} {IFC_3rd_sc[2]} -{IFC_nn}\n")
	
	def line_kpoints(
					self, 
					file_path='./', 
					length=50
					):
		atoms=Atoms.from_poscar(os.path.join(file_path, 'POSCAR'))
		kpts=Kpoints3D().automatic_length_mesh(lattice_mat=atoms.lattice_mat, length=length)
		print(kpts.kpts[0])
		return kpts.kpts[0]
        
	def create_VCABuilder(
							self, 
							file_path='./', 
							mat_root_dir='..', 
							file_name='VCAbuilder.xml', 
							grids=[20, 20, 20]
							):
		direct=os.path.join(file_path, file_name)
		with open(direct, 'w') as f:
			f.write('<singlecrystal>\n')
			f.write('  <!-- Equals the current work directory when omitted. -->\n')
			f.write('  <materials_repository root_directory="%s"/>\n'%mat_root_dir)
			f.write('  <compound name=\"%s\"/>\n'%self.formula)
			f.write('  <gridDensity A="%d" B="%d" C="%d"/>\n'%(grids[0], grids[1], grids[2]))
			f.write('  <!-- Directory is relative to current work directory. -->\n')
			#f.write('  <target directory="../%s"/>\n\n'%self.formula)
			f.write('  <target directory="."/>\n\n')
			f.write('  <overwrite/>\n')
			f.write('</singlecrystal>\n')

	# good method tp read the grids in VCAbuilder calculation ouputs
	def get_VCA_grids(
						self, 
						mat_path
						):
		files=[]
		for file in os.listdir(mat_path):
			if fnmatch.fnmatch(file, '*_*_*.h5'):
				files.append(file)

		for file in files:
			pat=re.findall('\d+', file)
			grids_pat=re.findall('_\d+_\d+_\d+.', file)
			grids=re.findall('\d+', str(grids_pat))
			print(grids)
			mat_pat=re.findall('(.*?)_', file)

		grids=list(map(int, grids))
		return grids, mat_pat

	def create_steady_montecarlo(
								self, 
								formula2, 
								path, 
								file_name='steady_montecarlo1d.xml',
								H5_root='../', 
								grids1=[20, 20, 20], 
								grids2=[20, 20, 20],
								thick1=100, 
								thick2=100, 
								delta_T=5, 
								nparticles='1e6', 
								nbins=300,
								target_dir='.', 
								transport_axis=[0, 1, 0],
								freq_bins=200, 
								spec_start=None, 
								spec_end=None, 
								spec_step=1
								):

		formula1=self.formula
		direct=os.path.join(path, file_name)
		with open(direct, 'w') as f:
			f.write('<materials>\n')
			f.write('  <H5repository root_directory="%s"/>\n'%H5_root)
			f.write('  <material label="%s" directory="%s" compound="%s" gridA="%d" gridB="%d" gridC="%d"/>\n'%(formula1, formula1, formula1, grids1[0], grids1[1], grids1[2]))
			f.write('  <material label="%s" directory="%s" compound="%s" gridA="%d" gridB="%d" gridC="%d"/>\n'%(formula2, formula2, formula2, grids2[0], grids2[1], grids2[2]))
			f.write('</materials>\n')
			f.write('<layers>\n')
			f.write('  <!-- The index (starting from 1) specifies the order from "top" to "bottom". -->\n')
			f.write('  <!-- Thicknesses are expressed in nm. -->\n')
			f.write('  <layer label="device" index="1" material="%s" thickness="%d"/>\n'%(formula1, thick1))
			f.write('  <layer label="substrate" index="2" material="%s" thickness="%d"/>\n'%(formula2, thick2))
			f.write('</layers>\n')
			f.write('<simulation>\n')
			f.write('  <!-- Set temperature differential, number of particles, and number of space bins. -->\n')
			f.write('  <!-- Reservoirs are set to Ttop = Tref + deltaT/2, Tbottom = Tref - deltaT/2. -->\n')
			f.write('  <core deltaT="%d" particles="%s" bins="%d"/>\n'%(delta_T, nparticles, nbins))
			f.write('  <!-- Set cartesian vector that describes the normal to the layer structure. -->\n')
			f.write('  <transportAxis x="%d" y="%d" z="%d"/>\n'%(transport_axis[0], transport_axis[1], transport_axis[2]))
			f.write('  <target directory="%s"/>\n'%(target_dir))
			f.write('</simulation>\n')
			if self.spec:
				if not spec_start:
					spec_start=1
				if not spec_end:
					spec_end=thick1+thick2
				f.write('\n<spectralflux>\n')
				f.write('    <resolution frequencybins="%d"/>\n'%freq_bins)
				f.write('    <locationrange start="%d" stop="%d" step="%d"/>\n'%(spec_start, spec_end, spec_step))# locations are expressed in nm
				f.write('</spectralflux>\n')

