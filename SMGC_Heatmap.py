#!/usr/bin/env python3
"""
SMGC_Heatmap.py

Description: This program takes one excel input file and constructs a heatmap from the data.

User-defined functions: 
    heatmap(data): core function, it creates the heatmap
Non-standard modules: 
    sys: here it is used to allow for command line arguments to be passed onto this script
    matplotlib.pyplot: used to generate the heatmap
    pandas: used to read in excel data into a dataframe
    numpy: the dataframe imported with pandas is converted to an array that is then plotted
    
Procedure:
    1. The script needs to be run from the command line, providing the name of the input file and the specific sheet
    2. The dataframe is reduced to those rows that contain gene clusters and columns relevant for the heatmap
    3. The dataframe is then converted into a numpy array that is subsequently visualizes as a heatmap
    4. The plot is saved.
    
Input: Input excel
Output: heatmap_SMGC.png
    
Usage: python3 FastaAlignerPlotter.py input_table.xlsx

Version: 1.00
Date: 2022-12-19
Name: Alexander Heck

"""

#%% First enter the sequences
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#%% Read in excel file

Inputname = sys.argv[1]
Sheetname = sys.argv[2]
    
data = pd.read_excel(Inputname, sheet_name = Sheetname)     # read input excel file

data = data[data['Total Clusters']!=0]                      # exlude all rows with 0 total clusters

data = data.iloc[:,list(range(0,2)) + list(range(9,18))]    # only keep columns relevant for the heatmap

#%% turn the excel table into a heatmap

def heatmap(data):
    array = data.iloc[:,list(range(2,11))].to_numpy()
    fig, ax = plt.subplots(figsize=(6, 10), dpi=300)                            # create an empty figure
    ax.imshow(array, cmap='viridis', aspect='auto', interpolation='nearest')    # plot the array to a grid plot
    ax.set_yticks(np.arange(len(data.Species)))                                 # set the x and y labels
    ax.set_yticklabels(data.Species, fontsize = 10)
    ax.set_ylabel('Species', fontsize=15)
    ax.set_xticks(np.arange(len(data.columns)-2))
    ax.set_xticklabels(data.columns[2:], rotation = 90, fontsize=10)
    ax.set_xlabel('Cluster Type', fontsize=15)
    ax.set_title('Heatmap of SMGC Cluster Type by\nSpecies', fontsize=18, loc='left')
    for i in range(array.shape[0]):                                             # annotate the cells
        for j in range(array.shape[1]):
            ax.text(j, i, f"{int(array[i, j])}", ha="center", va="center", fontsize=10)
    fig.savefig("heatmap_SMGC.png", dpi=600, bbox_inches="tight")               # save the figure
    print('Heatmap successfully created and saved under "heatmap_SMGC.png"')
            
heatmap(data)   #execute the function
























