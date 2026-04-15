## Full Human CDS sequences (for HMM training)
The human CDS dataset from NCBI is required to train the HMM emission probabilities:
+ File: `GCF_000001405.40_GRCh38.p14_cds_from_genomic.fna.gz`
+ This file is already available in `data/`, but if you would like to download it from NCBI use: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/ 



## Viral gene sequences (for analysis)
This is the file that the Viterbi algorithm is run on:
+ `influenza_A_genes.txt` contains the sequences of each gene from the Influenza A virus, specifically Influenza A virus (H1N1) A/Iwate/1130/2009. 
+ This file is already available in `data/`, but if you would like to download it from NCBI use: https://www.ncbi.nlm.nih.gov/nuccore/?term=Influenza+A+virus+(H1N1)+A%2FIwate%2F1130%2F2009 . Select all the hits that contain the complete CDS of a gene from this virus (some hits have two genes grouped together). Once selected, they can all be dowloaded together as one file despite being separate hits. The download will be a `.txt` file but it will contain sequences in the FASTA format so it will work in this program.
+ Similarly, gene sequence data from other viruses can be saved in a file and used in this project. 


## Small test dataset (for analysis)
`test.fa` contains 4 synthetic sequences I generated for quickly testing the prototype. This dataset does not train the HMM, it is only used to test the analysis. The expected result is that the first two sequences have a relatively higher adaptation score and the last two sequences should have relatively lower scores.

**To run analysis on this dataset:**
+ Make sure the HMM has been trained on the human CDS dataset.
+ Run the "Small test dataset" cell in the notebook `src/test.ipynb`.


## Generating synthetic data (for analysis)
The notebook `src/test.ipynb` contains a function to generate synthetic sequences:
+ It will generate 20 human-like and 20 random sequences.
+ There is a code cell that runs analysis on these sequences as well.
+ No random seed is set, so new sequences will be generated each time.

This is the code I used to generate the sequences:
```
def generate_sample_sequence(codons, probs, n):
    return "".join(random.choices(codons, weights=probs, k=n))
    

codon_list = generate_all_codons()
probs = [math.exp(hmm.emission_probs["A"][codon]) for codon in codon_list]

human_like_seq = {}
random_seq = {}

for i in range(1, 21):
    human_like_seq[f"h{i}"] = generate_sample_sequence(codon_list, probs, 20)
    random_seq[f"r{i}"] = generate_sample_sequence(codon_list, [1/64]*64, 20)
```
The sequences are generated based on the emission probabilities from the training data so it does require the use of the training dataset. 
