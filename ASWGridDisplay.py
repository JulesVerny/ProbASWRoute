
#  A Display Grid  Class 
# ============================================================================================
import pygame 
import math
# ===========================================================================================================
#size of our window
SCREENWIDTH = 600
SCREENHEIGHT = 600
FPS = 20	#  Experiment Performance Seems rather sensitive to Computer performance 

GRIDSIZE = 100
CELLWIDTH = 5
GRIDDISPLAYBIAS = 50
SENSORWIDTH=8.0*CELLWIDTH

#RGB colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LOWGREY = (40,40,40)
MEDGREY= (100,100,100)
HIGHGREY= (175,175,175)
GRIDGREY = (10,10,10)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (200,200,0)
# =====================================================================
# Create the Main PyGame Environment
pygame.init()
FPSCLOCK = pygame.time.Clock()
TheScreen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('ASW Grid Display')
	
MainGameFont = pygame.font.SysFont("calibri",20)
LegItemFont = pygame.font.SysFont("calibri",16)

TranspaprentSurface = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
TranspaprentSurface.set_colorkey((0,0,0))
TranspaprentSurface.set_alpha(4)
# =====================================================
#game class
class GridDisplay:
	def __init__(self,):
		self.DisplayedRoute = []
		self.ASWPlotPoints = []
		self.ASWDipPoints = []
		self.BottomThreshold = 0.0
		self.LowThreshold = 0.25
		self.HighThreshold = 0.75
	# =====================================================================================
	def PlotASWPoints(self, TheASWPlotPoints):
		self.ASWPlotPoints = TheASWPlotPoints
	# =====================================================================================
	def PlotASWDipPoints(self, TheDipPoints, LowestValue,HighestValue):
		self.ASWDipPoints = TheDipPoints
		self.BottomThreshold = LowestValue - 0.001
		self.LowThreshold = LowestValue + 0.333*(HighestValue-LowestValue)
		self.HighThreshold = LowestValue + 0.666*(HighestValue-LowestValue)

	# =====================================================================================	
	def CreateRouteDisplay(self, TheRouteSequence):
		self.DisplayedRoute.clear()
		if(len(TheRouteSequence)>1):
			for i in range (0,len(TheRouteSequence)):
				DipInstance1 = -1
				DipInstance2 = -1
				DipInstance1 = TheRouteSequence[i]
				if((i+1)<len(TheRouteSequence)):
					NextIndex = i+1
				else:
					NextIndex=0
				DipInstance2 = TheRouteSequence[NextIndex]
				
				if((DipInstance1>-1) and (DipInstance2>-1)):
					(PtX,PtY,PtValue) = self.ASWDipPoints[DipInstance1]
					LegStartPoint = (GRIDDISPLAYBIAS+PtX*CELLWIDTH+2, GRIDDISPLAYBIAS+PtY*CELLWIDTH+2) 
					(PtX,PtY,PtValue) = self.ASWDipPoints[DipInstance2]
					LegEndPoint = (GRIDDISPLAYBIAS+PtX*CELLWIDTH+2, GRIDDISPLAYBIAS+PtY*CELLWIDTH+2)
					self.DisplayedRoute.append((LegStartPoint,LegEndPoint))		
					
	# =======================================================================
    #  Main Display Update
	def UpdateDisplay(self,):
	
		Quit = False	
		# ====================================
		#  Process Keyboard Entry
		KeyPressed = pygame.key.get_pressed()
		if (KeyPressed[pygame.K_ESCAPE]):
			print("Esc pressed")
			Quit = True  			
		pygame.event.pump() # process event queue
		# ===================================
		TheScreen.fill(BLACK)
				
		# Need to clear downs the TranspaprentSurface
		TranspaprentSurface.fill(BLACK)
		
		# Draw N+1 Vertical Lines
		LineLength = GRIDSIZE * CELLWIDTH
		for vindex in range (0,GRIDSIZE+1):
			pygame.draw.line(TheScreen, GRIDGREY, (GRIDDISPLAYBIAS+vindex*CELLWIDTH,GRIDDISPLAYBIAS),(GRIDDISPLAYBIAS+vindex*CELLWIDTH,GRIDDISPLAYBIAS+LineLength))
			
		# Now Draw the Horizontal Lines
		for hindex in range (0,GRIDSIZE+1):
			pygame.draw.line(TheScreen, GRIDGREY, (GRIDDISPLAYBIAS,50+hindex*CELLWIDTH),(GRIDDISPLAYBIAS+LineLength,GRIDDISPLAYBIAS+hindex*CELLWIDTH))
		
		# Now Display The ASW Plot Points
		for (PtX,PtY,PtValue) in self.ASWPlotPoints:
			SPRect = pygame.Rect(GRIDDISPLAYBIAS+PtX*CELLWIDTH, GRIDDISPLAYBIAS+PtY*CELLWIDTH, CELLWIDTH, CELLWIDTH)
			if((PtValue > self.BottomThreshold) and (PtValue < self.LowThreshold)):
				pygame.draw.rect(TheScreen, LOWGREY, SPRect)
			if((PtValue > self.LowThreshold) and (PtValue < self.HighThreshold)):
				pygame.draw.rect(TheScreen, MEDGREY, SPRect)
			if(PtValue > self.HighThreshold):
				pygame.draw.rect(TheScreen, HIGHGREY, SPRect)

		# Now Display The ASW Dip Points
		for (PtX,PtY,PtValue) in self.ASWDipPoints:
			SPRect = pygame.Rect(GRIDDISPLAYBIAS+PtX*CELLWIDTH, GRIDDISPLAYBIAS+PtY*CELLWIDTH, CELLWIDTH, CELLWIDTH)
			pygame.draw.rect(TheScreen, RED, SPRect)
			# Now Draw the Sensor Circles
			SensorDipCircle = pygame.Rect(GRIDDISPLAYBIAS+PtX*CELLWIDTH-SENSORWIDTH, GRIDDISPLAYBIAS+PtY*CELLWIDTH-SENSORWIDTH, SENSORWIDTH*2, SENSORWIDTH*2)	
			pygame.draw.ellipse(TranspaprentSurface,GREEN, SensorDipCircle)
			TheScreen.blit(TranspaprentSurface, (0,0))


		# Draw the Displayed Route if it exists
		for (StartPt,EndPoint) in self.DisplayedRoute:
			pygame.draw.line(TheScreen, GREEN, StartPt,EndPoint)
		
		# Now update the PyGame Display
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		
		return Quit
	# =========================================================================
	def Closedown(self,):
		pygame.quit()
	
	# ==========================================================================================