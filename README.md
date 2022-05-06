# tsp_cs5100
A Markov Chain with  Superposition Multi-Traveling Salesman Group project 

The TSPAttempt1 file is current final product of this project. It can be run as is when the proper packages are installed and present. 
This can also be run on the google colab at the link: 
https://colab.research.google.com/drive/1LJI7ExrPnTbl-_H4Nx8YEU-3EiNV0zfw

The First Attempt File was an eailer version of the TSPAttempt file. 

The entry.py is a potential starting point for running the TSP on different data sets brought in via JSON. 
The supporting json files are in the output folder. This file can be run with command args to change while data sets are in use. 

The Processor_json file has some funcitons from reading and processing json. These can be used to load data and turn it into 
an ajaceney matrix which is then passed into the funcitons present in TSPAttempt instead of the random data found in that file. 

Index Information 
  
entry.py: starting  point that accepts command args
map.py: file for map data sets
processor_json.py: the processor library that executes the different json functions, Builds adj_mtrx 
TSPAttempt1.py: The initial attempt of the TSP using Monte Carlo Markov Chains
FirstAttempt.py: theoretical groundwork for problem development.
output folder: default output location for writing Json files
