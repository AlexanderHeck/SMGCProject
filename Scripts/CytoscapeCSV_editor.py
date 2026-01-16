#!/usr/bin/env python3
'''
CytoscapeCSV_editor.py

Description: This program is designed to append a network node file exported from Cytoscape with information
             about the entries organisms and gene cluster family. It is thus intented for downstream
             processing after running BiG-SCAPE. It requires 3 input files, the Cytoscope node file,
             which will also be used as the output. A BiG-SCAPE cluster file with information about
             gene cluster families, and an annotation file that links the entry names of the Cytoscope
             file to their respective organisms.

User-defined functions:
    None
    
Non-standard modules: 
    sys: here it is used to allow for command line arguments to be passed onto this script
    pandas: for reading an xlsx file and data frame handling
    
Procedure:
    1. The script needs to be run from the command line, providing the names of the input file and output file
    2. The program then reads the excel file and saves it as a datafram
    3. This dataframe is then iterated over line by line, constructing the fasta file in parralel
       using the information from the excel file
    
Input: input.xlsx file
Output: Output.fasta file
    
Usage: python3 CytoscapeCSV_editor.py Cytoscape_file.csv Clustering_file.tsv Annotation_file.tsv
Example: python3 CytoscapeCSV_editor.py  PKS_c0.3.network default node.csv PKS_clustering_c0.3.tsv record_annotations.tsv

Version: 1.00
Date: 2022-12-17
Name: Alexander Heck

'''

#%% Import requires modules
import pandas as pd
import sys

#%% Take command line arguments
Filename=sys.argv[1]
Clusteringfile=sys.argv[2]
Annotationfile=sys.argv[3]

#%% Open input file

data = pd.read_csv(Filename, index_col="name")
cluster = pd.read_csv(Clusteringfile, sep='\t', index_col="Record")
annotation = pd.read_csv(Annotationfile, sep='\t', index_col="Record")

#%% Write Output file

data["Organism"]="n.a."         # introduce a new column called Organism
data["Family"]="n.a."           # introcude a new column called Family
namelist=data.index.tolist()    # initiate a list of all species names

for name in namelist:           # iterate through the name list and write both the corresponding organism and family in the correct row
    organism=annotation.loc[name, "Organism"]
    data.loc[name, "Organism"]=organism
    family=cluster.loc[name, "Family"]
    data.loc[name, "Family"]=family
    
data.to_csv(Filename)           # export the dataframe to a csv
