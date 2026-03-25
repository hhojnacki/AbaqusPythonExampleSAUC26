# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  Abaqus Python script to extract results from gasket self contact example
#
#  This is a prototype version of a script for presentation at SUAC26
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  generic python imports
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
import numpy as np
import sys
#
#  Import the abaqus stuff
import odbAccess as od
#####import gasketClass as gc
import gasketClass2 as gc
#
#
#  get the results from all runs specified in the arguments
if len(sys.argv) < 2: 
	print("At least 1 odb files need to be specified")
	sys.exit(42)
#
#  plot and save
results = [gc.gasketFromFile(odbFile) for odbFile in sys.argv[1:]]
[plt.plot(result.verticalDisp,result.verticalForce,label=result.heading) for result in results]
plt.grid()
plt.legend()
plt.xlabel('Vertical Displacement')
plt.ylabel('Clamping Force')
plt.title('Force-Displacement Behavior')
plt.savefig('ForceVsDeflection.png')
#
#  In Summary
print('\nLoad Case'.ljust(20),'Contact','Min Pr','Max Pr','\n '.ljust(20),
      'Press','Stress','Stress\n',sep='\t')
for lc in results: print(lc.heading.ljust(20),format(lc.maxContactPressure(),'3.2f'),
                          format(min(lc.minPrin),'3.2f'),format(abs(max(lc.maxPrin)),'3.2f'),sep='\t')


