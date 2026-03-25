"""Abaqus Python script to extract results from gasket self contact example

Run within CAE using File > Run script...

This is a prototype version of a script for presentation at SUAC26
"""

#  generic python imports
from pathlib import Path
import sys

#  Import the abaqus stuff
import abaqusConstants as ac
import gasketClass as gc
import visualization
import xyPlot

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def saveContours(odbList):
    """Save png contour plot for a list of open odbs"""

    viewport = session.viewports[session.currentViewportName]
    for odb in odbList:  # loop over the open results
        # Make and save contour plot
        viewport.setValues(displayedObject=odb)
        viewport.odbDisplay.display.setValues(plotState=(ac.CONTOURS_ON_DEF,))
        viewport.view.fitView()
        session.printToFile(
                fileName=str(Path(odb.name).with_suffix('.png')),
                format=PNG,
                canvasObjects=(viewport,),
                )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def plotForce(gasketList):
    """Generate XY plot of force results for a list of gasket class instances"""

    viewport = session.viewports[session.currentViewportName]

    curves = []
    xQuantity = visualization.QuantityType(type=ac.DISPLACEMENT)
    yQuantity = visualization.QuantityType(type=ac.FORCE)

    for gasket in gasketList:
        # Make an XYPlot curve from the extracted gasket data
        xy = xyPlot.XYData(
                legendLabel=gasket.heading,
                data=list(zip(gasket.verticalDisp, gasket.verticalForce)),
                axis1QuantityType=xQuantity,
                axis2QuantityType=yQuantity,
                )
        curves.append(session.Curve(xyData=xy))

    # Plot the gasket curves
    plotName = 'force-vs-displacement'
    if plotName in session.xyPlots:
        del session.xyPlots[plotName]
    xyp = session.XYPlot(plotName)  # create a new XYPlot object
    chartName = xyp.charts.keys()[0]
    chart = xyp.charts[chartName]
    chart.setValues(curvesToPlot=curves)  # add the curves
    viewport.setValues(displayedObject=xyp)  # display the plot

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def printSummary(gasketList):
    """Summarize the results for a list of gasket class instances"""

    print('\nLoad Case'.ljust(20),'Contact','Min Pr','Max Pr','\n '.ljust(20),
                                  'Press','Stress','Stress\n',sep='\t')
    for gasket in gasketList:
        print(gasket.heading.ljust(20),
              format(gasket.maxContactPressure(),'3.2f'),
              format(min(gasket.minPrin),'3.2f'),
              format(abs(max(gasket.maxPrin)),'3.2f'),sep='\t')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  Main program
if __name__ == "__main__":  # was not imported from another script
#
#  Instantiate a gasket class for all odbs open in this session
    odbList = [odb for odb in session.odbs.values()]
    gasketList = [gc.gasket(odb) for odb in odbList]
#
#  Plot the stress contours for the open odbs
    saveContours(odbList)
#
#  Plot x-y curves for force/displacement
    plotForce(gasketList)
#
#  Summarize the results
    printSummary(gasketList)

