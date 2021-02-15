#  Using https://stackoverflow.com/questions/31805560/how-to-create-surface-plot-from-greyscale-image-with-matplotlib
#
# matplot 3d Plot Types:  https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#surface-plots
#
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import cv2
import scipy.misc
import pygame
import math
import ASWGridDisplay
import RouteCalculator
# =====================================================================
ASWDipPoints = []
SonarRangeSquared = 8.0*8.0
print()
print(" ==================== ")
# =======================================================================
# Read the Raw ASW heatmap
ASWProbData = cv2.imread("./data/ASW1.png", 0)
cv2.imshow('Raw ASW heatMap', ASWProbData)

# downscaling has a "smoothing" effect
ASWProbData = cv2.resize(ASWProbData, (100,100))
ASWProbData = ASWProbData /256.0
print("ASWProbData is an Numpy Array: ", type(ASWProbData), " of Shape: ", ASWProbData.shape)
GRIDSIZE = ASWProbData.shape[0]
HighestASWProb = 1.0
LowestASWProb = 0.0
# =====================================================================
# Display it on a 3D Map
# create the x and y coordinate arrays (here we just use pixel indices)
"""
xx, yy = np.mgrid[0:ASWProbData.shape[0], 0:ASWProbData.shape[1]]

# create the figure
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(xx, yy, ASWProbData ,rstride=1, cstride=1, cmap=plt.cm.jet,
                linewidth=0)

# show it
plt.show()
"""
# =====================================================================
# Find the next Highest (Non Overlaping Point)
def FindNextPeak(LastPeak):
    HighestPeakValue = -1.0
    HighX = -1
    HighY = -1
    for vindex in range (0, GRIDSIZE):
        for hindex in range (0,GRIDSIZE):
            if((ASWProbData[vindex,hindex]>HighestPeakValue) and (ASWProbData[vindex,hindex]<LastPeak)):
                # Have Found a Peak - 
                if(len(ASWDipPoints)>0):
                    # Need to check  within Range of any existing Dipping Points
                    OverlappingAny = False
                    for (DipX,DipY,DipValue) in ASWDipPoints:
                        sqrdistance = (hindex-DipX)*(hindex-DipX) + (vindex-DipY)*(vindex-DipY)
                        if(sqrdistance<SonarRangeSquared*1.5):
                            OverlappingAny = True
                    if(not OverlappingAny):
                        HighX = hindex
                        HighY = vindex
                        HighestPeakValue = ASWProbData[vindex,hindex] 
                else:
                    HighX = hindex
                    HighY = vindex
                    HighestPeakValue = ASWProbData[vindex,hindex]

    return (HighX,HighY, HighestPeakValue)
# =====================================================================
# Perhaps Limit it at a  Threshold value
#  
COURSETHREASHOLD = 0.075
ASWProbData[ASWProbData<COURSETHREASHOLD] = 0

#cv2.imshow('Processed ASW heatMap', ASWProbData)
# ===============================================================================
#
TheDisplay = ASWGridDisplay.GridDisplay()
#
# Some Sample Points
#SigPoints = [(67,22),(68,22),(34,17),(45,23),(84,22),(18,94),(34,45),(35,46),(36,47),(19,43),(40,92),(19,55),(78,7),(27,29),(78,34),(67,22),(89,45),(78,67),(94,45),(29,56),(56,89),(19,24), (19,25)]
#
"""
ASWPlotPoints = []
NumberofPoints = 0
for vindex in range (0, GRIDSIZE):
    for hindex in range (0,GRIDSIZE):
        if(ASWProbData[vindex,hindex]>0.001):
            ASWPlotPoints.append(((hindex),(vindex)))    # Reverse axis order to align to Image
            NumberofPoints = NumberofPoints +1
TheDisplay.PlotASWPoints(ASWPlotPoints)
TheDisplay.UpdateDisplay()
print("Number of ASW Plot Points:", NumberofPoints)
"""
# ============================================================================
# Now Iterate through and find the Dipping Points from Highest peak downwards
MAXNUMBERDIPPOINTS = 12
CurrentPeakProb = 1.0
NextDipX = 1
NumberDipPoints = 0
#
while ((NextDipX>0) and (NumberDipPoints<MAXNUMBERDIPPOINTS)):
    NextDipX,NextDipY,DipThreatValue = FindNextPeak(CurrentPeakProb)
    if(NextDipX>-1):
        ASWDipPoints.append((NextDipX,NextDipY,DipThreatValue))
        CurrentPeakProb = DipThreatValue
        if(NumberDipPoints==0):
            HighestASWProb = CurrentPeakProb
        NumberDipPoints = NumberDipPoints+1
LowestASWProb = CurrentPeakProb
print(" Number of Suitable Dipping Points Found: ",NumberDipPoints)
print("Lowset Dip Prob Threshold Value: ", LowestASWProb)
#
# =========================================
# Revise the Background ASWPlotpoints against the Lowest threshold Value
ASWPlotPoints = []
for vindex in range (0, GRIDSIZE):
    for hindex in range (0,GRIDSIZE):
        if(ASWProbData[vindex,hindex]>(CurrentPeakProb-0.0001)):
            ASWPlotPoints.append((hindex,vindex,ASWProbData[vindex,hindex]))    

# ============================================================================================
TheDisplay.PlotASWDipPoints(ASWDipPoints,LowestASWProb, HighestASWProb)
TheDisplay.PlotASWPoints(ASWPlotPoints)
# ============================================================================================        
#  Now Calculate the ASW Dipping Route
RouteDipSequence = RouteCalculator.CalculateRoute(ASWDipPoints)
TheDisplay.CreateRouteDisplay(RouteDipSequence)

# =============================================
TheDisplay.UpdateDisplay()

# ======================================================
print()
print("==> Completed Press Any Key to Finish : ")
dog = input()
print(" ===========================================")
# ===================================================