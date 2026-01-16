# EXPLORATION OF SECONDARY METABOLITE GENE CLUSTERS IN WOOD DECAYING BASIDIOMYCOTA

This project used a combination of exising software tools and self written programs to establish a workflow from raw annotated genome data to identifies secondary metabolite gene clusters, families of clusters, and a phylogeny of their respective core biosynthetic genes.

This README will cover every part of that workflow with a focus on the self written programs. The documentation for the existing software tools will be linked. All scripts including the analysis can be accessed in the scripts folder. The excel file SecondMetaProjectsResults_withgeneID.xlxs contains all data derived from the AntiSMASH results. Due to their size the raw AntiSMASH and BiG-SCAPE files could not be uploaded to Git-Hub but can be accessed on request under the email-adress al4118he-s@student.lu.se.

Different Programs are used in the following order:
1. Genomic data is given to AntiSMASH which identifies SMGCs in the Genomes
2. Data derived from the AntiSMASH results are recorded in the excel table SecondMetaProjectsResults_withgeneID.xlxs
3. The raw data from AntiSMASH is given to BiG-SCAPE to identify families of clusters
4. The cluster files from BiG-SCAPE are downloaded to be visualized in Cytoscape, the program Cytoscape_CSV_editor.py is employed to append these files with species names
5. The sequence data recorded in the excel file in step 2. are collected in one multifasta file together with other useful information using the program FastaWriterPKS.py
6. Data from the same excel table is subsequently statistically analysed using the R script TableAnalysis.R and visualised as a heatmap using SMGC_Heatmap.py


## Initialising the virtual environment

To ensure a safe and clean workflow and to install all dependencies required for Big-Scape, conda was used to create a virtual environment:

```bash
conda create -n bigscape
conda activate bigscape
```

## AntiSMASH genome processing

The genomes for the selected species were found using the NCBI genome browser https://www.ncbi.nlm.nih.gov/datasets/genome/ (more information about specific strains and accession number used can be found under SecondMetaProjectsResults_withgeneID.xlxs). 
AntiSMASH can be accessed freely under https://fungismash.secondarymetabolites.org/#!/start . Relaxed detection strictness was applied. More information can be accessed in AntiSMASHs own documentation under https://docs.antismash.secondarymetabolites.org/intro/.

All AntiSMASH results files were safed offline in the folder "Results":

```bash
mkdir Results
cd Results
```

## BiG-SCAPE test runs and final analysis

For more information on how to sucessfully install BiG-SCAPE and run it, please consult the BiG-SCAPE documentation under: https://github.com/medema-group/BiG-SCAPE/wiki

To safe all BiG-SCAPE outputs a new folder was created together with a subfolder for the test runs.

```bash
mkdir Bigscape
mkdir Bigscape/Testruns
cd Bigscape
```

The following overview contains a number of testruns of BiG-SCAPE for parameter optimisation.

1. This runs BiG-SCAPE with default parameters and includes singeltons

```bash
bigscape cluster -i ../Results -o Testruns/Output1/ -p pfam/Pfam-A.hmm -v --include-singletons
```

2. Alignment mode: auto

```bash
bigscape cluster -i ../Results -o Testruns/Output2/ -p pfam/Pfam-A.hmm -v --include-singletons --alignment-mode auto
```

3. Extend strategy: simple Match

```bash
bigscape cluster -i ../Results -o Testruns/Output3/ -p pfam/Pfam-A.hmm -v --include-singletons --extend-strategy simple_match
```

4. Extend strategy: greedy

```bash
bigscape cluster -i ../Results -o Testruns/Output4/ -p pfam/Pfam-A.hmm -v --include-singletons --extend-strategy greedy
```

5. Use Bigscape 1 legacy weights when calculating distances

```bash
bigscape cluster -i ../Results -o Testruns/Output5/ -p pfam/Pfam-A.hmm -v --include-singletons --legacy-weights --classify category
```

6. Combine legacy weights with simple match extension strategy

```bash
bigscape cluster -i ../Results -o Testruns/Output6/ -p pfam/Pfam-A.hmm -v --include-singletons --extend-strategy simple_match --legacy-weights --classify category
```

7. Now with alignment mode global

```bash
bigscape cluster -i ../Results -o Testruns/Output7/ -p pfam/Pfam-A.hmm -v --include-singletons --extend-strategy simple_match --legacy-weights --classify category --alignment-mode global
```

8. Or alignment mode local

```bash
bigscape cluster -i ../Results -o Testruns/Output8/ -p pfam/Pfam-A.hmm -v --include-singletons --extend-strategy simple_match --legacy-weights --classify category --alignment-mode local
```
Followed by a two final runs with optimized parameters, both with and without singletons:

```bash
bigscape cluster -i ../Results/ -o Output_final/ -p pfam/Pfam-A.hmm -v --include-singletons --extend-strategy simple_match --legacy-weights --classify category

bigscape cluster -i ../Results/ -o Output_final_nosingletons/ -p pfam/Pfam-A.hmm -v --include-singletons --extend-strategy simple_match --legacy-weights --classify category
```

## Cluster visualization in Cytoscape

The BiG-SCAPE clusters were downloaded and visualized in Cytoscape according to https://github.com/medema-group/BiG-SCAPE/wiki/12.-Tutorials#loading-big-scape-output-into-cytoscape .

However, the network files created by BiG-SCAPE only contain information about the NCBI genome accession number, not however the species, the self written program CytoscapeCSV_editor.py was used to append that table with species names and family and add them in cytoscape as labels. More information on Cytoscape can be accessed here: https://cytoscape.org/

Script: CytoscapeCSV_editor.py

Python version: 3.11.14

Description: This program is designed to append a network node file exported from Cytoscape with information about the entries organisms and gene cluster family. It is thus intented for downstream processing after running BiG-SCAPE. It requires 3 input files, the Cytoscope node file, which will also be used as the output. A BiG-SCAPE cluster file with information about gene cluster families, and an annotation file that links the entry names of the Cytoscope file to their respective organisms.

Usage:
```bash
python3 CytoscapeCSV_editor.py Cytoscape_file.csv Clustering_file.tsv Annotation_file.tsv
```
Here run as:

```bash
python3 CytoscapeCSV_editor.py C:\Users\heck-\Documents\Uni\FungiProject\Bigscape\Output_final\output_files\2025-12-16_13-31-07_c0.3\terpene\terpene_c0.3.network default node.csv 
C:\Users\heck-\Documents\Uni\FungiProject\Bigscape\Output_final\output_files\2025-12-16_13-31-07_c0.3\terpene\terpene_clustering_c0.3.tsv 
C:\Users\heck-\Documents\Uni\FungiProject\Bigscape\Output_final\output_files\2025-12-16_13-31-07_c0.3\record_annotations.tsv
```

## Writing of a single multi fasta file for phylogenetic analysis

Using the recorded data in SecondMetaProjectsResults_withgeneID.xlxs the program FastaWriterPKS.py is run to create one single multi fasta file. This file is subsequently aligned and a phylogenetic tree constructed using MEGA (more information under https://megasoftware.net/).

Script: FastaWriterPKS.py

Python version: 3.11.14

Description: This Program takes one input xlsx file and from that constructs one single multi-fasta file.

Usage:
```bash
python3 FastaWriterPKS.py input_file.xlsx output_name.fasta
```
 Here run as (all files were stored in the same directory):
 ```bash
 python3 FastaWriterPKS.py SecondMetaProjectsResults_withgeneID.xlsx PKS_CoreProteins.fasta
 ```

## Statistical data analysis and visualisation

Subsequently the data in SecondMetaProjectsResults_withgeneID.xlxs was statistically analised using the R script TableAnalysis.R in R studio 2025.9.02 and visualised using the python script SMGC_Heatmap.py.

Script: TableAnalysis.R

Usage: This is a R script meant for the data analysis of this specific dataset. It can be run in R Studio version 2024.9.02

Script: SMGC_Heatmap.py

Python version: 3.11.14

Description: This program takes one excel input file and constructs a heatmap from the data.

Usage:
```bash
python3 FastaAlignerPlotter.py input_table.xlsx sheet_name
```

Here run as (both script and file were stored in the same directory):

```bash
python3 FastaAlignerPlotter.py SecondMetaProjectsResults_withgeneID.xlxs Full_list
```