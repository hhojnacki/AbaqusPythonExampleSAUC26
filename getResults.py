# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  Abaqus Python script to extract results from gasket self contact example
#
#  This is a prototype version of a script for presentation at SUAC26
#
#  To run: "abaqus python getResults.py"
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  generic python imports
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
#
#  Import the abaqus stuff
import odbAccess as od
#
#  Open the odb file and get the upper level things
result = od.openOdb("gasketBaseline.odb")
gasketModel = result.rootAssembly
#
#  Extract the node that has the applied disp BC
#  Check to dee if there is only 1 node in ths set
dieNode = gasketModel.instances['PART-1-1'].nodeSets['DIE']
if len(dieNode.nodes) != 1: print("Improperly Defined Node Set 'DIE'")
#
#  Get the set of elements that are elastomer material
gasketElements = gasketModel.instances['PART-1-1'].elementSets['GASKET']
#
#  recover the load/deflection data for the loaded node using history data
step1 = result.steps['Step-1']
histPoint = od.HistoryPoint(node=dieNode.nodes[0])
dieHistories = step1.getHistoryRegion(point=histPoint)
dieDisp = dieHistories.historyOutputs['U2'].data
dieFor = dieHistories.historyOutputs['RF2'].data
verticalForce = [abs(y) for x, y in dieFor]
verticalDisp = [abs(y) for x, y in dieDisp]
#
#  Recover load/deflect from field output data, resulting from the followiing .inp lines:
#   *OUTPUT,FIELD,FREQUENCY=1
#   *NODE OUTPUT,NSET=DIE
#   U,RF
#
#  Using getSubset method
step1 = result.steps['Step-1']
dieDisp = [f.fieldOutputs['U'].getSubset(region=dieNode) for f in step1.frames]
dieFor = [f.fieldOutputs['RF'].getSubset(region=dieNode) for f in step1.frames]
verticalForce = [abs(f.values[0].data[1]) for f in dieFor]
verticalDisp = [abs(d.values[0].data[1]) for d in dieDisp]
#
#  plot and save
plt.plot(verticalDisp,verticalForce)
plt.grid()
matplotlib.pyplot.savefig('ForceVsDeflection.png')

