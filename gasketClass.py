#
#  gasket is a python class to represent the results from the Abaqus Examples
#   manual case: "Self-contact in rubber/foam components: rubber gasket"
#
#  Created for presentation to SAUC26
#
#
#  Standard Abaqus imports
import odbAccess as od
#
#  Other imports
import numpy as np
#
class gasket:
	def __init__(self, odb):
		self.heading = odb.analysisTitle
		self.model = odb.rootAssembly
		self.step1 = odb.steps['Step-1']
#
#  interesting subsets of data, the node set for the so called "DIE" part, which is an 
#   analytical surface.  This node is where the load is applied
		self.loadNode = self.model.instances['PART-1-1'].nodeSets['DIE']
		if len(self.loadNode.nodes) != 1: print("Improperly Defined Node Set 'DIE'")
#
		gasketElements = self.model.instances['PART-1-1'].elementSets['GASKET']
#
#  Get the vertical displacement and forces for the loaded node
		histPoint = od.HistoryPoint(node=self.loadNode.nodes[0])
		dieHistories = self.step1.getHistoryRegion(point=histPoint)
		dieDisp = dieHistories.historyOutputs['U2'].data
		dieFor = dieHistories.historyOutputs['RF2'].data
		self.verticalForce = [abs(y) for x, y in dieFor]
		self.verticalDisp = [abs(y) for x, y in dieDisp]
#
#  Get the stress and strain values for the final load of the gasket material
		stress = self.step1.frames[-1].fieldOutputs['S'].values
		gasketStress = self.step1.frames[-1].fieldOutputs['S'].getSubset(region=gasketElements).values
		self.minPrin = [v.minPrincipal for v in gasketStress]
		self.maxPrin = [v.maxPrincipal for v in gasketStress]
		self.vonMises = [v.mises for v in gasketStress]
		self.maxShear = [v.tresca for v in gasketStress]
# We could ask for strains here
		self.strain = self.step1.frames[-1].fieldOutputs['LE'].values
#
#  3 - 2 - 1 CONTACT!
		press = self.step1.frames[-1].fieldOutputs['CPRESS   SKIN/DIE'].values
		self.cpress = [p.data for p in press]
#
#  What is the max contact pressure for the skin/dir contact pair
	def maxContactPressure(self):
		return max(self.cpress)
#
#  What is the average pressure for closed contacts on skin/die
	def averageContactPressure(self):
		return np.average([v for v in self.cpress if v > 0])
#
#  sub-class of gasket, creates odb from a .odb file and calls the super class
class gasketFromFile(gasket):
	def __init__(self,odbName):
		self.result = od.openOdb(odbName,readOnly=True)
		gasket.__init__(self,self.result)
		
