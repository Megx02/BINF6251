# Project Snapshot
This project aims to see whether different genes of the Influena A virus show varying levels of adaptation to human codon usage. Since viruses depend on host translationary machinery, codon usage bias may influence translation efficiency, so some genes may adapt to host codon usage for better translation efficiency. 

I implemented a Hidden Markov Model with two hidden states - adapted and not adapted. I used the Viterbi Algorithm to identify the optimal sequence of hidden states for each viral gene based on codon observations and then calculated the adaptation score based on the fraction of adapted states in the optimal sequence. 

## Current implementation status:
A working prototype has been implemented that can:
+ Train emission probabilities from human CDS data
+ Run the Viterbi algorithm on some test data
+ Output state sequences and adaptation scores for test data
+ Run a statistical test on the results to evaluate significance of results


# What is Implemented
Fully implemented:
+ FASTA parsing and sequence filtering.
+ Codon splitting function.
+ HMM model with parameter setups.
+ Viterbi algorithm with traceback.
+ Adaptation score calculation 
+ Synthetic data generation (both human-like and random sequences)
+ Basic statistical tests for comparison of results

Partially implemented:
+ Parameter tuning (I have only tested with one value for pseudocount, start and transition probabilities, I will be testing with other values)
+ Validation of model and algorithm (I've tested it with synthetic data and a statistical test, but I'd like to do more validation)

Not implemented yet:
+ Stress test and Unit tests
+ Parallelization for large datasets
+ More complex state models (I only have 2 hidden states right now, I want to test the model with more states but I am still figuring out how that would work)

Deviations from pseudocode:
The pseudocode included functions to parse the training data file and get a list of sequences, split the sequences into codons and calculate the codon count from the list of codons. I had to change this and create a function that counted the codons while parsing the file instead of storing the list of sequences and list of codons due to memory constraints during runtime. I made this choice since only the codon count is needed for calculating the emission probabilities and the list of sequences and list of codons are not needed to be stored.


# Prototype Demo Description
To run the prototype on synthetic data:

First the human CDS sequences need to be downloaded following the instructions in `data/README.md`.
+ The input file expected is `GCF_000001405.40_GRCh38.p14_cds_from_genomic.fna.gz`.
+ This is the data file that will be used to train the model.

Since the prototype is generating synthetic data there is no input data file for the Viterbi algorithm and analysis right now. Instead there is a function to generate synthetic data in the notebook with the driver program `src/main.ipynb`.

After downloading the data, run all the cells in `src/main.ipynb`.

Output:
Adaptation score and state sequence will be printed in the cell output for the corresponding gene ID.


# Data Documentation
+ Human CDS data was donwloaded from NCBI for training the HMM model and estimating emission probabilities.
+ The Viterbi algorithm was tested on synthetic data - human like sequences were generated from the emission probabilities of the human data and random sequences were generated from an equal distribution of codon probabilities

Preprocessing:
+ All the sequences were filtered to make sure they contain only A, C, G and T and have a length divisible by 3.




# Initial Observations




# Reflection on Changes and Challenges



# Next Steps
