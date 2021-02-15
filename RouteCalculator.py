# "Simulated Anhealing Route Calculation 
# Note this variant uses an alternative TSP solver - using simulated annealing  
#  https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/
#  Solves the Travelling Salesman Problem (TSP) through  simulated annealing (In ten Lines of Code !)
# ===============================================================================
import random, math, copy
import numpy as np 
# =====================================================================================
def CalculateRoute(TheDippingList):
    CoordinatesList = []
    for (PtX,PtY,PtValue) in TheDippingList:   
        CoordinatesList.append([PtX, PtY])    # Note arrange as [List of [x,y]] instead of tuples
    # =================== 	
    cities = CoordinatesList
    NumberOfCities = len(cities)
	# ==================================		
	# Main TSP Anenealing Method in tens Lines of Code
	# And I really do not pretend to undestand this code
	# See https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/  for an attempted explanation !
    tour = random.sample(range(NumberOfCities),NumberOfCities)
    for temperature in np.logspace(0,5,num=100000)[::-1]:
        [i,j] = sorted(random.sample(range(NumberOfCities),2))
        newTour =  tour[:i] + tour[j:j+1] +  tour[i+1:j] + tour[i:i+1] + tour[j+1:]
        if math.exp( ( sum([ math.sqrt(sum([(cities[tour[(k+1) % NumberOfCities]][d] - cities[tour[k % NumberOfCities]][d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]]) - sum([math.sqrt(sum([(cities[newTour[(k+1) % NumberOfCities]][d] - cities[newTour[k % NumberOfCities]][d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]])) / temperature) > random.random():
            tour = copy.copy(newTour)

    BestSequence = [tour[i % NumberOfCities] for i in range(NumberOfCities+1)]
    BestSequenceNP = np.array(BestSequence[:-1])
	#print("Best Sequence: ", BestSequenceNP)
	# ======================
	# Now Rotate the numpy BestSequence order to start at First Coordinate	
    ZeroIndex =   np.where(BestSequenceNP==0)[0]			# Find the Index of Item= 0, only need the fisrt element
    OptimisedSequence = np.roll(BestSequenceNP,-ZeroIndex) # Rotate the numpy array unsing the numpy roll method
		
	# Now Convert the Opimisised Sequence to a List to allow Jsonfiy to serialise the return 
    RtnSequence = OptimisedSequence.tolist()
    print(" The Calculated Route Sequence: ", RtnSequence)
    #
    return RtnSequence
# =========================================================================================


