## Generation of Search Routes From  Probabality Imagea

This is similar to SHARD, but an exploration on the use of a Probabilistic Greyscale Image, as the spource. So review the map of probabilites, and select the highest probabilities,as the way point Sensor Search points. The greyscale image map is ingested, scalled to 100x100 pixels using cv2 and each pixel divided down by 255 to represent a probablity of threat.    

![picture alt](https://github.com/JulesVerny/ProbASWRoute/blob/main/data/ASW1.png "Raw Image Pic")


The main parameters for the effective route calculation are then Sensor range (For non overlapping points) and the preferred highest number of Sensor Search points, to limit the coverage. Then a simulated anhealing methods is used to create an effective route sequence. So in the following the 12 most non overlapping dipping points are used to create the following route againt the input image above.  

![picture alt](https://github.com/JulesVerny/ProbASWRoute/blob/main/CalcRoute.PNG "Route Pic")


### Technologies  ###

This is entirely written in python, with cv2 to ingest the original image and  pygame used for the main route display.
  
### Useage ###

  * python ProcessASWMap.py     
 
### Main Python Packages  ###
 
python packages: cv2, numpy, pygame

### Acknowledgments: ###
Eric Phanson: Solving of the the TSP in Ten Lines of python code using some "simulated anhealing" method:

https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/
