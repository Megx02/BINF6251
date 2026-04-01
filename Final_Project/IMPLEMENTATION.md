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
+ If you want to test with different training data you can change the filename in `src/main.ipynb` to the path to your file.

I have included a small test dataser (`data/test.fa`) to test the analysis pipeline. This contains 4 synthetic sequences I made for testing purposes. I also have a function in the notebook that generates a dictionary of human-like and random sequences for testing the analysis. 

The training data and test dataset are hardcoded in the notebook, so if you are testing with other input files, change the file path to you file. The generated dictionary for testing is not a separate data file, it is generated within the notebook itself.

After downloading the data, run all the cells in `src/main.ipynb`.

Output:
Adaptation score and state sequence will be printed in the notebook cell output for the corresponding gene ID.
The expected output for analysis on `data/test.fa` is:
```
{'Gene_1': (0.85, 'AAAAAAAAAAAAAAAAANNN'),
 'Gene_2': (0.75, 'NNNNNAAAAAAAAAAAAAAA'),
 'Gene_3': (0.25, 'AAAAANNNNNNNNNNNNNNN'),
 'Gene_4': (0.4, 'NNNNNNNNNNNNAAAAAAAA')}
 ```


# Data Documentation
+ Human CDS data was donwloaded from NCBI for training the HMM model and estimating emission probabilities. It is in the form of a FASTA file with sequences corresponding to coding regions in humans. 
+ The Viterbi algorithm was tested on synthetic data. I created a small test dataset (`data/test.fa`) which contains 4 synthetic sequences. I also have a function that generates 20 human like sequences from the emission probabilities of the human data and 20 random sequences from an equal distribution of codon probabilities for testing the analysis pipeline.

Preprocessing:
+ All the sequences were filtered to make sure they contain only A, C, G and T and have a length divisible by 3.

Since I haven't used real data for the analysis at this stage, the ground truth is based on the process of generation of the synthetic data. Sequences generated using human codon emission probabilities are treated as havign a higher number of adapted states while sequences from a uniform codon distribution are treated as having a relatively lower number of adapted states. 


# Initial Observations
So far the algorithm has given me expected results for the synthetic data. The human-like sequences gave me an average adaptation score between 0.6 and 0.9 during my different test runs and the random sequences gave me average scores between 0.1 and 0.5. I performed a t-test to compare the adaptation scores of the two groups and got a p-value less than 0.05 indicating that the difference between them is statistically significant. This indicates that the algorithm is able to differentiate between human-like and random sequences based on codon usage pattern. 


# Reflection on Changes and Challenges
I didn't run into major issues with the analysis portion, although I have only tested with one set of transition probabilities and pseudocount so I will need to test with other values to see what gives me the most significant results. I also have a relatively simple model that uses only two hidden states right now, I am looking for ways to increase the number of states and observe if that makes results even more signifcant. My main issue was with training the HMM, the FASTA file I used to train the model was quite large and I had initially written the code such that it parsed the file, stored all the sequences in a list, split the sequences into codons and stored those in a list and then counted the codons for the emission probabilities. This caused issues with memory. I realized I only needed the codon counts for the emission probabilities and the actual sequences and codons from it don't need to be stored so I modified the code to directly count the codons while parsing the file. 


# Next Steps
For the final stage of the project, I have planned some imporvements and additions. 
+ The current output is pretty simple, with just the adaptation scores and state sequences for test data. I plan on having it produce more informative outputs when using viral data, such as statistics across genes, maybe some visualizations and more interpretable outputs that show patterns in adaptation. I am also looking for ways to extend the HMM with additional hidden states. 
+ I will implement unit tests to verify teh individual functions of the algorithm and perform a stress test to evaluate the algorithm's performance. My initial validation was done with synthetic data, the next step is to run the algorithm on real Influenza A viral sequences and validate results to see if they are biologicaly meaningful and correct. This will include comparing adaptation patterns across genes and checking consistency with known biological insights. 
+ I will imporve documentation to make the code easier to follow and create a Quick Start guide for users to run a working example of the project.
