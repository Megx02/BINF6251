## Full Human CDS sequences (for HMM training)
The human CDS dataset from NCBI is required to train the HMM emission probabilities:
+ File: `GCF_000001405.40_GRCh38.p14_cds_from_genomic.fna.gz`
+ This file is already committed in `data/`, but if you would like to download it from NCBI use: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/ 
+ The notebook `src/main.ipynb` has the file path hard coded, so it will automatically use this file to train the HMM before analysis.


## Small test dataset (for analysis)
`test.fa` contains 4 synthetic sequences I generated for quickly testing the prototype. This dataset does not train the HMM, it is only used to test the analysis. The expected result is that the first two sequences have a relatively higher adaptation score and the last two sequences should have relatively lower scores.

**To run analysis on this dataset:**
+ Make sure the HMM has been trained on the human CDS dataset.
+ Run the "Small test dataset" cell in the notebook `src/main.ipynb`.


## Generating synthetic data (for analysis)
The notebook `src/main.ipynb` contains a function to generate synthetic sequences:
+ It will generate 20 human-like and 20 random sequences.
+ There is a code cell that runs analysis on these sequences as well.
+ No random seed is set, so new sequences will be generated each time.
