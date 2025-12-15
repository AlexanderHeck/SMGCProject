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
       using the information from the excel file
    
Input: input.xlsx file
Output: Output.fasta file
    
Usage: python3 FastaWriterPKS.py input_file.xlsx sheet_name output_name.fasta
Example: python3 FastaWriterPKS.py SecondMetaProjectsResults_withgeneID.xlsx PKS_ids PKS_CoreProteins.fasta

Version: 1.00
Date: 2022-12-15
Name: Alexander Heck

'''

#%% Import requires modules
import pandas as pd
import sys

#%% Take command line arguments
Filename=sys.argv[1]
Sheetname=sys.argv[2]
Outputname=sys.argv[3]


#%% Open input file

data = pd.read_excel(Filename, sheet_name=Sheetname)

#%% Write Output file

with open(Outputname, 'w') as Output:               # Open the Output file
    for row in data.itertuples():                   # Iterate over the dataframe
        species=row.Species                         # Save all the information in the respective variables
        species=species.replace(" ", "_")
        genomeacc=row.Whole_genome_accession
        region=row.Region
        scaffoldacc=row.Scaffold_accession
        contigedge='False'
        if row.Contig_edge=='t':                    
            contigedge='True'
        proteinid=row.PKS_core_protein_id
        proteinlength=row.Protein_length
        sequence=row.Sequence
        if proteinlength==len(sequence):            # Make sure the sequence has the correct length
            print(f'Protein {proteinid} okay...')
        else:
            print(f'Protein {proteinid} is shorter/longer than expected...')
        Output.write(f'>{proteinid}_{species}\tGenome accession:{genomeacc}\tScaffold accession:{scaffoldacc}\tRegion:{region}\tGene on contig edge:{contigedge}\n{sequence}\n')