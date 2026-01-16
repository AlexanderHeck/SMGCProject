#!/usr/bin/env python3
'''
FastawriterPKS.py

Description: This Program takes one input xlsx file and from that constructs one single multi-fasta file.

User-defined functions:
    None
    
Non-standard modules: 
    sys: here it is used to allow for command line arguments to be passed onto this script
    pandas: for reading an xlsx file and data frame handling
    
Procedure:
    1. The script needs to be run from the command line, providing the names of the input file and output file
    2. The program then reads the excel file and saves it as a datafram
    3. This dataframe is then iterated over line by line, constructing the fasta file in parralel
       using the information from both sheets of the excel file. To the Output file saved are
       the Gene ID, Species, Order, Decay Type, and sequence 
    
Input: input.xlsx file
Output: Output.fasta file
    
Usage: python3 FastaWriterPKS.py input_file.xlsx output_name.fasta
Example: python3 FastaWriterPKS.py SecondMetaProjectsResults_withgeneID.xlsx PKS_CoreProteins.fasta

Version: 1.00
Date: 2022-12-15
Name: Alexander Heck

'''

#%% Import requires modules
import pandas as pd
import sys

#%% Take command line arguments
Filename=sys.argv[1]
Outputname=sys.argv[2]

#%% Open input file separated by sheets

dataPKS = pd.read_excel(Filename, 1)
dataFull = pd.read_excel(Filename, 0, index_col='Species')


#%% Write Output file

with open(Outputname, 'w') as Output:               # Open the Output file
    for row in dataPKS.itertuples():                # Iterate over the dataframe
        species = row.Species                       # In the following all required information is saved in the respective variables
        order = dataFull.loc[species, 'Order']      
        decay_type = dataFull.loc[species, 'Decay type']
        if decay_type == 'BR':                      # if it is brown-rot decay, also add the clade of brown rot
            clade = dataFull.loc[species, 'Clade of BR']
            decay_type = f'{decay_type} {clade}'
        species = species.replace(" ", "_")
        contigedge=False                            # set the on contig edge variable to false by default
        if row.Contig_edge=='t':                    # set to true if the gene was on a contig edge       
            contigedge=True
        proteinid=row.PKS_core_protein_id
        proteinlength=row.Protein_length
        sequence=row.Sequence
        if proteinlength==len(sequence):            # Make sure the sequence has the correct length
            print(f'Protein {proteinid} okay...')
        else:
            print(f'Protein {proteinid} is shorter/longer than expected...')
        if contigedge == True:                      # lastly write the output to file
            Output.write(f'>{proteinid}_{species}\t{order}\t{decay_type}\tOn contig edge\n{sequence}\n')
        else:
            Output.write(f'>{proteinid}_{species}\t{order}\t{decay_type}\n{sequence}\n')