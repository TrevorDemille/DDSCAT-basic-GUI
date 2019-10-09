import Tkinter as tk
from tkMessageBox import *
from PIL import ImageTk,Image
import tkFont as tkfont
import ttk
from DDA_UI_Library_1 import *
#
#

class DDA_Application(tk.Tk):
	#
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		#
		self.title_font = tkfont.Font(family='Times New Roman', size=12, weight='bold')

		# Stacking up my frames in container, and raising the one I want visible individually
		container = tk.Frame(self)
		container.pack(side='top', fill='both', expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.myFrames = {}

		for F in (Main_Page, LSPR, Near_Field):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.myFrames[page_name] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("Main_Page")

	def show_frame(self, page_name):
		#
		frame = self.myFrames[page_name]
		frame.tkraise()

class Main_Page(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.controller = controller
		#
		self.extSpecSelect = tk.Button(self, text="Calculate LSPR Spectra", 
			width=25, command=lambda: controller.show_frame("LSPR"))
		self.QUIT = tk.Button(self, text="Quit Application", fg="red", 
			width=15, command=self.controller.destroy)
		self.nearField = tk.Button(self, text="Near-Field Enhancement", 
			width=25, command=lambda: controller.show_frame("Near_Field"))
		#
		self.extSpecSelect.grid(row=1, column=0, pady=5, padx=2)
		self.QUIT.grid(row=3, column=1, pady=5, padx=5, sticky='SE')
		self.nearField.grid(row=1, column=1, pady=5, padx=2)
		#
		# Set image files for UI display - must be in default folder
		im_path = 'C:\Users\Neretina Lab PC\Desktop\DDSCAT\Default Files'
		ims = ['Cubic_Cage_SEM.png','LSPR_image.png','NF_image.png','Wulff_Cage.png']
		self.imObj = []
		for j in range(len(ims)): 
			ims[j] = im_path + '\\' + ims[j]
			self.imObj.append(ImageTk.PhotoImage(Image.open(ims[j])))
		#
		self.aboutLabel = tk.Canvas(self, width=400, height=68, bg='#add8e6', relief='raised')
		self.aboutLabel.grid(row=0, columnspan=2, pady=2, padx=2)
		self.lspr_Image_label = tk.Canvas(self, width=200, height=200, relief='raised')
		self.lspr_Image_label.grid(row=2, column=0, pady=0, padx=2)
		self.NF_image_label = tk.Canvas(self, width=200, height=200, relief='raised')
		self.NF_image_label.grid(row=2, column=1, pady=0, padx=2)
		#
		self.aboutLabel.create_text(10,5, anchor='nw', 
			text='**READ ME** Graphical interface for plasmonic and electrodynamic\nsimulations of arbitrary geometries using DDSCAT. Shape-files are taken\nto dictate representative individual dipole volumes at each coordinate\nand (shape.dat) must contain arrays of cubic integer coordinates.')
		self.lspr_Image_label.create_image(100, 102, anchor='center', image=self.imObj[1])
		self.NF_image_label.create_image(100, 102, anchor='center', image=self.imObj[2])


class LSPR(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.controller.geometry('415x360')
		self.controller.title('DDSCAT v7.3 GUI')
		self.controller.configure(background='grey')
		#
		self.folderName = tk.Label(self, text="Simulation Folder Name").grid(
			row=1, column=0, sticky='W', padx=5)
		self.material_1 = tk.Label(self, text="Set Metal Species").grid(
			row=2, column=0, sticky='W', padx=5)
		self.material_2 = tk.Label(self, text="Set Substrate Species").grid(
			row=3, column=0, sticky='W', padx=5)
		self.errTol = tk.Label(self, text="Error Tolerance Order").grid(
			row=4, column=0, sticky='W', padx=5)
		self.range1 = tk.Label(self, text="Initial Wavelength (um)").grid(
			row=5, column=0, sticky='W', padx=5)
		self.range2 = tk.Label(self, text="Final Wavelength (um)").grid(
			row=6, column=0, sticky='W', padx=5)
		self.steps = tk.Label(self, text="Number of Steps (integer)").grid(
			row=7, column=0, sticky='W', padx=5)
		self.effRadius = tk.Label(self, text="Effective Radius (um)").grid(
			row=8, column=0, sticky='W', padx=5)
		self.yPol = tk.Label(self, text="Y-Polarization Vector Magnitude").grid(
			row=9, column=0, sticky='W', padx=5)
		self.xPol = tk.Label(self, text="Z-Polarization Vector Magnitude").grid(
			row=10, column=0, sticky='W', padx=5)
		
		# Set dropdown menu options for materials
		choices = {'Sapphire', 'Quartz', 'None'}
		metChoices = {'Au (gold)', 'Ag (silver)', 'Cu (copper)', '50/50 Au/Ag', 'None'}

		self.MatChoice = tk.StringVar(self)
		self.MetalChoice = tk.StringVar(self)
		self.MatChoice.set('Sapphire') # default choice
		self.MetalChoice.set('Au (gold)') # default choice

		# Build entry widgets	- 
		# Grid positioning must happen separately to avoid returning Nonetype at get()
		self.fNameEntry = tk.Entry(self)
		self.fNameEntry.grid(row=1, column=1, columnspan=1, sticky='EW')
		#
		self.mat1Entry = tk.OptionMenu(self, self.MetalChoice, *metChoices)
		self.mat1Entry.grid(row=2, column=1, sticky='EW')
		#
		self.mat2Entry = tk.OptionMenu(self, self.MatChoice, *choices)
		self.mat2Entry.grid(row=3, column=1, sticky='EW')
		#
		self.errTolEntry = tk.Entry(self)
		self.errTolEntry.grid(row=4, column=1, columnspan=1, sticky='EW')
		#
		self.range1Entry = tk.Entry(self)
		self.range1Entry.grid(row=5, column=1, columnspan=1, sticky='EW')
		#
		self.range2Entry = tk.Entry(self)
		self.range2Entry.grid(row=6, column=1, columnspan=1, sticky='EW')
		#
		self.stepsEntry = tk.Entry(self)
		self.stepsEntry.grid(row=7, column=1, columnspan=1, sticky='EW')
		#
		self.effRadEntry = tk.Entry(self)
		self.effRadEntry.grid(row=8, column=1, columnspan=1, sticky='EW')
		#
		self.polSetyEntry = tk.Entry(self)
		self.polSetyEntry.grid(row=9, column=1, columnspan=1, sticky='EW')
		#
		self.polSetxEntry = tk.Entry(self)
		self.polSetxEntry.grid(row=10, column=1, columnspan=1, sticky='EW')
		#
		self.enterButton = tk.Button(self, text="Build", fg='blue', width=6, 
			command=self.getInfo).grid(row=12, column=0, padx=5, sticky='W')
		self.runButton = tk.Button(self, text='Run', fg='red', width=6, command=self.runLSPR).grid(
			row = 12, column=0, padx=5, sticky='S')
		self.returnButton = tk.Button(self, text='Return to Main Page', 
			width = 20, command=lambda: controller.show_frame("Main_Page")).grid(row = 12, column=1, sticky='e')

		self.polVal = tk.IntVar()
		self.chkBox = tk.Checkbutton(self, text="Multiple Polarization Angles", variable= self.polVal)
		self.chkBox.grid(row=11, column=0, sticky='W')
		#
		self.textBox = tk.Canvas(self, width=400, height=68, bg='#add8e6', relief='raised')
		self.textBox.grid(row=0, columnspan=4, pady=2, padx=5)
		#
		self.text1 = self.textBox.create_text(10, 5, anchor='nw', 
			text='**LSPR Parameters** This builds a parameter (ddscat.par) file according\nto the above inputs, and creates a new directory to house it.\n**Note** Multiple polarization setting is used to simulate unpolarized\nlight by averaging the results of 90 polarizations 2 degrees apart.')

	def runLSPR(self):
		#
		path = self.fNameEntry.get()

		#############################################
		# path = 'C:\Users\Neretina Lab PC\Desktop\DDSCAT\Default Files\Test_Analyze_Me.txt'
		# wave, eData, aData, sData = [],[],[],[]
		# with open(path) as f:
		# 	for k, line, in enumerate(f):
		# 		data = line.strip()
		# 		data = data.split()

		# 		wave.append(np.float(data[0]))
		# 		eData.append(np.float(data[1]))
		# 		aData.append(np.float(data[2]))
		# 		sData.append(np.float(data[3]))
		############################################
		#
		os.chdir(self.basePath)
		os.system("ddscat.exe")
		wave, eData, aData, sData = saveQtable(path)
		#
		extMax, absMax, scaMax, NF = analyzeResults(wave, eData, aData, sData)
		extMaxList = []
		for l,j in enumerate(extMax):
			extMaxList.append(str(extMax[l][1])+ ' intensity at '+str(extMax[l][0])+' nm\n')
		extMaxList = ''.join(extMaxList)
		
		self.textBox.itemconfigure(self.text1, text='Found %d extinction local maxima:\n%s ' % (len(extMax),extMaxList))
		if askyesnocancel(title=None, message='Would you like to plot results?\n\n(Extinction, Absoption, and Scattering)'):
			plotResults(wave, eData, aData, sData, NF)


	def getInfo(self):
		# Define root path for simulation files
		defPath = 'C:\Users\Neretina Lab PC\Desktop\DDSCAT'

		# Store entry inputs from UI 
		info = [self.fNameEntry.get(),self.MetalChoice.get(),self.MatChoice.get(),
			self.errTolEntry.get(),self.range1Entry.get(), self.range2Entry.get(), 
			self.stepsEntry.get(),self.effRadEntry.get(), self.polSetyEntry.get(),
			self.polSetxEntry.get(),self.polVal.get()]
		# Instantiate array to hold compiled input information 
		compInfo=[]

		# Material string assignment from plasmonic materials options menu - specific to the filename of each
		# dielectric data file (../DDSCAT/diel/filename)
		if info[1] == 'Au (gold)': compInfo.append("'../diel/Au_evap'")
		elif info[1] == 'Ag (silver)': compInfo.append("'../diel/Ag.txt'")
		elif info[1] == 'Cu (copper)': compInfo.append("'../diel/Cu.txt'")
		elif info[1] == '50/50 Au/Ag': compInfo.append("'..\diel\Au50_Ag50.txt")
		else: self.warningScreen('No Plasmonic Material Entered')

		# Input string compiling to fit DDSCAT v7.3 par-file syntax
		compInfo.append("'../diel/" + info[2] + ".txt'")
		compInfo.append('5e-' + info[3])
		compInfo.append(info[4] + ' ' + info[5] + ' ' + info[6])
		compInfo.append(info[7] + ' ' + info[7] + ' 1')
		compInfo.append('(0,0) (' + info[8] + ',0.) (' + info[9] + ',0.)')
		compInfo.append(str(info[10]+1))

		# Note to self
		if info[10] == 2:
			print('***** SET UP MULTIPOL FUNCTION *****')

		# Return warning screen for failure to enter parameter value(s)`
		for e in range(len(compInfo)): 
			if compInfo[e] == '': self.warningScreen('Must enter a value for all parameters')
		
		# Store filename and build directory and parameter file for input simulation 
		fName = info[0]
		defCreate(defPath,fName,compInfo)

	def warningScreen(self,cap):
		showerror('Error: Invalid Entry', cap)

class Near_Field(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		#
		self.basePath = os.path.dirname(os.path.realpath('DDSCAT_UI.py'))

		self.returnButton = tk.Button(self, text='Return to Main Page', 
			width = 20, command=lambda: controller.show_frame("Main_Page")).grid(row = 6,
			column=1, padx=5, pady=5, sticky='SE')
		
		# Setting canvas for READ ME label - configurable object
		self.textBox = tk.Canvas(self, width=400, height=68, bg='#add8e6', relief='raised')
		self.textBox.grid(row=0, columnspan=4, pady=2, padx=5)
		self.text1 = self.textBox.create_text(10, 5, anchor='nw', 
			text='\t**Electric Near-Field Enhancement Calculations**\nThis solves for the square of the driven/incident E-field intensity ratio for\na given wavelength and LSPR spectra. **Note** This requires a prior built\nddscat.par parameters file (Calculate LSPR Spectra page)')

		# Setting labels for first column
		self.folderName = tk.Label(self, text="Simulation Folder Name").grid(
			row=1, column=0, sticky='W', padx=5)
		#
		self.waveVal = tk.Label(self, text="Desired Wavelength (um)").grid(
			row=2, column=0, sticky='W', padx=5)
		#
		self.NFspaceX= tk.Label(self, text="Calculated X-Volume Extension").grid(
			row=3, column=0, sticky='W', padx=5)
		#
		self.NFspaceY= tk.Label(self, text="Calculated Y-Volume Extension").grid(
			row=4, column=0, sticky='W', padx=5)
		#
		self.NFspaceZ= tk.Label(self, text="Calculated Z-Volume Extension").grid(
			row=5, column=0, sticky='W', padx=5)
		#
		# Setting Entry widgets to match labels
		self.default_Response = tk.StringVar(self, value='0.5')
		#
		self.fNameEntry = tk.Entry(self)
		self.fNameEntry.grid(row=1, column=1, columnspan=1, sticky='EW')
		#
		self.waveEntry = tk.Entry(self)
		self.waveEntry.grid(row=2, column=1, columnspan=1, sticky='EW')
		#
		self.NFspaceXEntry = tk.Entry(self, textvariable=self.default_Response)
		self.NFspaceXEntry.grid(row=3, column=1, columnspan=1, sticky='EW')
		#
		self.NFspaceYEntry = tk.Entry(self, textvariable=self.default_Response)
		self.NFspaceYEntry.grid(row=4, column=1, columnspan=1, sticky='EW')
		#
		self.NFspaceZEntry = tk.Entry(self, textvariable=self.default_Response)
		self.NFspaceZEntry.grid(row=5, column=1, columnspan=1, sticky='EW')
		#

		# Setting up buttons for the two functions solveNF and showNF
		self.runButton = tk.Button(self, text="Run", fg='red', width=6, 
			command=self.solveNF).grid(row=6, column=0, padx=5, pady=5, sticky='N')
		self.updateButton = tk.Button(self, text='Update', fg='blue', width=6, 
			command=self.update_Par).grid(row = 6, column=0, padx=5, pady=5, sticky='W')
		self.showButton = tk.Button(self, text="Show", fg='blue', width=6, 
			command=self.showNF).grid(row=6, column=0, padx=5, sticky='E')

		# Verbose Canvas for user updates
		self.verboseBox = tk.Canvas(self, width=400, height=130, bg='#add8e6', relief='raised')
		self.verboseBox.grid(row=7, columnspan=4, pady=2, padx=5)
		self.userInfo = self.verboseBox.create_text(10, 5, anchor='nw', 
			text=' **Info >>')

	def User_Update(self, caption):
		#
		self.verboseBox.itemconfigure(self.userInfo, text=caption)

	def solveNF(self):
		#
		path = self.basePath + '\\' + self.fNameEntry.get()
		#
		self.User_Update(' **Info >> Launching DDSCAT v7.3 executable for %s.' % self.fNameEntry.get())
		#
		os.chdir(path)
		print(os.getcwd())
		os.system("ddscat.exe")
		#
		self.User_Update(' **Info >> DDSCAT executable complete for %s.' % self.fNameEntry.get())

	def update_Par(self):
		#
		info = [self.fNameEntry.get(), self.waveEntry.get(), self.NFspaceXEntry.get(), 
		self.NFspaceYEntry.get(), self.NFspaceZEntry.get()]
		#
		if NF_Def_Create(self.basePath, info): 
			self.User_Update(' **Info >> DDSCAT Parameter file updated for new LSPR peak wavelength\nat %s um.' % info[1])

	def showNF(self):
		a=2

if __name__ == "__main__":
	app = DDA_Application()
	app.mainloop()