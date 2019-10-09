import fileinput
import re
import shutil
import os
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

#
from tkMessageBox import *
#
def defCreate(defPath,fName,info):
	# define dummy filenames to be used in duplication and relocation 
	output_File = 'ddscat.par'
	input_File = 'Def_dds_par.par'

	# Check if directory already exists
	if foldCreate(defPath, fName) == False: return False

	# Move default parameter file to new folder, copy, and rename
	fileOut = 'C:\Users\Neretina Lab PC\Desktop\DDSCAT' + '\\' + fName + '\\' + 'Def_dds_par.par'
	fileIn = 'C:\Users\Neretina Lab PC\Desktop\DDSCAT\Default Files\Def_dds_par.par'
	shutil.copyfile(fileIn,fileOut)

	# Set dummy strings to be replaced by entry widget strings
	replaceMe = ['Default Diel 1','Default Diel 2','Default Tol',
		'Default Wave','Default Er','Default Pol','Default Numb']

	# Set directory to be open and rewritten with entry widget strings
	fileIn_new = 'C:\Users\Neretina Lab PC\Desktop\DDSCAT' + '\\' + fName + '\\' + input_File
	
	# open and read default parameter file
	fIn = open(fileIn_new,'rt')
	data = fIn.read()
	for k in range(7): 
		# Substitute entry widget strings into default file at dummy string positions
		data = re.sub(replaceMe[k],info[k],data)
	fIn.close()

	# Write modified parameters to new ddscat.par file
	fOut = open(fileIn_new,'w')
	fOut.write(data)
	print('Created New DDSCAT Parameter File')
	fOut.close()

	# Remove original parameters file and return
	os.chdir('C:\Users\Neretina Lab PC\Desktop\DDSCAT' + '\\' + fName)
	if os.path.exists(output_File): os.remove(output_File)
	os.rename(input_File,output_File)	
	return True	

def foldCreate(defPath,fName):

	# Initiate and set empty parameter
	print('Creating directory at: %s' % (defPath + '\\' + fName))
	empty = None

	# Check for previous existence / contradiction in directory
	# Throw warning, prompt for replacement - 'No' or 'cancel' both return nothing
	if os.path.exists(defPath + '\\' + fName) == True: 
		reply, switch = choiceScreen('Warning: Given Folder Already Exists\n\nWould you like to replace it?',fName)

		if reply == 'Yes':

			# Back up in directory to allow tree to be removed
			os.chdir('C:\Users\Neretina Lab PC\Desktop')
			shutil.rmtree(defPath + '\\' + fName)
			empty = True
			print("Folder Path Cleared")

		# no and cancel both simply don't make the folder	
		else: 
			print('Folder Not Created')
			return False
	
	# Given removed folder or no initial folder of the name given, copy in 
	# executables for ddscat and near-field calculation
	if empty == True or os.path.exists(defPath + '\\' + fName) == False: 
		os.mkdir(defPath + '\\' + fName)
		shutil.copyfile(defPath + '\\' + 'Default Files' + '\\' + 'ddscat.exe',
			 defPath + '\\' + fName + '\\' + 'ddscat.exe')
		shutil.copyfile(defPath + '\\' + 'Default Files' + '\\' + 'ddpostprocess.exe', 
			defPath + '\\' + fName + '\\' + 'ddpostprocess.exe')
		print('New Simulation Folder Created: %s' % fName)
		return True

def saveQtable(path):
	wave, extinc, absor, scatt = [],[],[],[]
	location = path + '\\' + 'qtable'
	destination = path + '\\' + 'LSPR DDA Results Table.txt'
	#
	with open(destination,'w+') as newFile:
		with open(location,'r') as qData:
			for k, line in enumerate(qData):
				# Skipping over the header in qtable file(s)
				if k >= 15:
					#
					inData = line.strip()
					inData = inData.split()
					#
					nmWave = '%d' % (np.float(inData[1]*1000))
					#
					wave.append(np.float(nmWave))
					extinc.append(np.float(data[2]))
					absor.append(np.float(data[3]))
					scatt.append(np.float(data[4]))
					#
					writeMe = str(nmWave + '\t' + data[2] + 
						'\t' + data[3] + '\t' + data[4] + '\n')
					newFile.write(writeMe)

	return wave, extinc, absor, scatt

def analyzeResults(wave, eData, aData, sData):
	# runs after ddscat.exe finishes and finds peak wavelengths / intensities
	# connect to plot editing window options

	#Arrange as arrays and find local maxima
	allData = [np.array(eData),np.array(aData),np.array(sData),np.array(wave)] 
	extMax, absMax, scaMax, maxVals = [],[],[],[]
	for ii in range(3): maxVals.append(sig.argrelmax(allData[ii], order=3))
	#
	# Save wavelengths and intensities of maxima for extinction, absoption and scattering
	for p in range(len(maxVals[0][0])): 
		extMax.append([wave[maxVals[0][0][p]],eData[maxVals[0][0][p]]])
		absMax.append([wave[maxVals[0][0][p]],aData[maxVals[0][0][p]]])
		scaMax.append([wave[maxVals[0][0][p]],sData[maxVals[0][0][p]]])
	#
	NF = [0,0]
	#
	return extMax, absMax, scaMax, NF

def plotResults(wave, eData, aData, sData, NF):
	# plots and displays curves for extinction, absorption, scattering
	#
	fig = plt.figure()
	plt.gcf().canvas.set_window_title('DDSCAT LSPR Results')
	fig.patch.set_facecolor('white')	
	#
	gs = gridspec.GridSpec(2, 2, hspace=0.3, wspace=0.3)
	#
	axTL = plt.subplot(gs[0,0])
	axTR = plt.subplot(gs[0,1])
	axBL = plt.subplot(gs[1,0])
	axBR = plt.subplot(gs[1,1])
	#
	####### integrate NF calculations into this eventually ###############

	axesList = [axTL,axTR,axBL,axBR]
	dataList = [eData,aData,sData,NF]
	yLabel_List = ['Extinction','Absorption','Scattering','NF']
	col = ['r','g','#008B8B','b']
	#
	for num, j in enumerate(axesList): 
		fig.add_subplot(j)
		#
		if num == 3: break
		#
		j.plot(wave, dataList[num],col[num],linewidth=1.8)
		j.set(ylabel=yLabel_List[num],xlabel='Wavelength (nm)')
		j.tick_params(axis='both',which='both',direction='out',width=2,right=None,top=None,pad=5)
		for k in j.spines: j.spines[k].set_linewidth(1.8)
	#
	#plt.subplot_tool()
	plt.show()

def NF_Def_Create(base, info):
	#
	fileName = base+'\\'+info[0]+'\\'+'ddscat.par'
	temp = base+'\\'+info[0]+'\\'+'DDS_TEMP.par'
	#
	if os.path.exists(temp): os.remove(temp)
	os.rename(fileName,temp)
	#
	extensLine = info[2]+' '+info[2]+' '+info[3]+' '+info[3]+' '+info[4]+' '+info[4]+' '
	#
	with open(temp, 'rt') as fIn:
		data = fIn.read()
		data = re.sub('0 = NRFLD','1 = NRFLD', data)
		with open(fileName, 'w+') as fOut:
			fOut.write(data)

			###############  FIX ME  #################
		 	for j, line in enumerate(data):
		 		if j == 17:
		 			line2 = extensLine+'(fract. extens. of calc. vol. in -x,+x,-y,+y,-z,+z)\n'
		 			fOut.write(line2)
					pass
		 		elif j == 27: 
		 			lineNew = info[1]+' '+info[1]+" 1 'LIN' = wavelengths (first,last,how many,how=LIN,INV,LOG)\n"
		 			fOut.write(lineNew)
		 		else: fOut.write(line)
			fOut.close()
		fIn.close()
	#
	os.remove(temp)
	return True

def choiceScreen(cap,fName):
	confirm = askyesnocancel(Title=None,message=cap)
	switch = False 
	if confirm: 
		reply = 'Yes'
		switch = True
		print('Switch: True')
	elif confirm is None:
		reply = 'cancel'
	else:
		reply = 'No'
	return reply, switch
	
