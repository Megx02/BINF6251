# Project Overview
This project investigates whether different genes of the Influenza A virus show varying levels of adaptation to human host codon usage. Since viruses depend on host translational machinery, codon usage bias may influence translation efficiency, so genes may adapt to host codon usage for better translation efficiency. 

This project implements a Hidden Markov Model with two hidden states - Adapted and Not Adapted. The Viterbi Algorithm identifies the top k optimal paths of hidden states for each viral gene based on codon observations and then calculates the adaptation score for each path and the average adaptation score for each gene based on the fraction of adapted states in the paths. 

Input data:
+ Human CDS sequences (training data)
+ Influenza A gene sequences (test data)

Ouput data:
+ Top k Viterbi paths of hidden states for each gene
+ Adaptation score for each path
+ Average adaptation score for each gene
+ Viterbi log-probability score for each path

# Installation/Setup
Requirements:
+ Python >= 3.11

Set up:
A virtual environment is recommended.

Option 1: venv
```
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```
Option 2: Conda
```
# Create environment with Python
conda create -n project_env python=3.11

# Activate environment
conda activate project_env

# Install dependencies
pip install -r requirements.txt
```

Dependencies:

All required Python packages are listed in `requirements.txt`.

Quick verification:
```
python -c "import numpy, scipy, pytest; print('Setup OK')"
```


# Quick start
The program is run from the root directory `Final_Project`, using a command-line interface (CLI). 

Two subcommands are available:
+ `train`: trains the HMM on host (human) coding sequences.
+ `analyze`: runs the Viterbi algorithm on the viral gene sequences

These are separated so you can train the model once and reuse it to analyze multiple viruses without repeated retraining.

**Note:** If `python` is not recognized on your system, use `python3` for all the commands instead.

### Train the HMM model:

From `Final_Project`, to train the HMM model run:
```
python -m src.main train 
```
Inputs (with defaults):
+ `training_data`: Host coding sequences that you want to train the model on (default: `data/GCF_000001405.40_GRCh38.p14_cds_from_genomic.fna.gz`)
+ `max_codons`: maximum number of codons to use for training (default: `None`)

### Analyze Viral Gene Data:
From `Final_Project`, to analyze viral data run:
```
python -m src.main analyze
```
Inputs (with defaults):
+ `analysis_data`: Path to file containing gene sequences of virus that you want to score for adaptation (default: `data/influenza_A_genes.txt`)
+ `num_paths`: number of top paths to return from the Viterbi algorithm (default: `2`)
+ `output_file`: output filename to store the scoring results of all the genes (default: `results/results.txt`)
+ `ranked_genes`: Path to file to store ranked genes (default: `results/ranked_genes.txt`)

### Help:
To see all the configurable arguments:
```
python -m src.main --help
python -m src.main train --help
python -m src.main analyze --help
```

Expected output:

Two files are expected as output, both will be created in teh `results/` directory.

1. Analysis results

Scoring results are written to `results/results.txt`.

For each viral gene, the output includes:
+ Top k paths of hidden states
+ Adaptation score for each path
+ Viterbi log-score for each path
+ Average adaptation score for each gene

Example Output:
```
Gene: lcl|LC660659.1_cds_BDC79445.1_1
Path 1:
AAAANNNNAAAAAA
Adaptation score: 0.714
Viterbi log-score: -2134.52

Path 2:
AAAAAAANNNNNAA
Adaptation score: 0.643
Viterbi log-score: -2134.79

Average adaptation score: 0.679
```
2. Gene ranking results

Based on the adaptation scores, genes are ranked in decreasing order of score and written to `results/ranked_genes.txt`.

Example Output:
```
Rank 1: lcl|LC660656.1_cds_BDC79442.1_1
Average adaptation score: 0.898

Rank 2: lcl|LC660658.1_cds_BDC79444.1_1
Average adaptation score: 0.873
```

### Notebook
A notebook version of this project is available at `notebooks/main.ipynb`. This is a way to view the results without saving them in a file. The input data files are hardcoded in the notebook.

Note: To run the notebook, you may need Jupyter kernel support for your environment.

### Prototype Notebook

To run a prototype version of this project, you can run the notebook `notebooks/test.ipynb`.
This notebook runs the algorithm on two synthetic sets of sequences, one generated from human-like codon usage and the other from a uniform distribution of codons.

## Note
+ All inputs have defualt values, so the pipeline can be run without addition arguments, however the subcommands `train` or `analyze` must included while running the steps of the pipeline.
+ The repository includes two output files `results/results.txt` and `results/ranked_genes.txt` generated from a previous run of the pipeline. Running the pipeline again will overwrite these files unless a different output file is specified.


# Usage and Options
The main script is `src/main.py`.
Command structure (from root):
```
python -m src.main <subcommand> <arguments>
```
Subcommands: `train`, `analyze`
Arguments for `train`: `--train_data`, `--max_codons`
Arguments for `analyze`: `--analysis_data`, `--num_paths` 

Other scripts:
+ `src/hmm.py`: HMM implementation
+ `src/viterbi.py`: Viterbi algorithm to return top k paths and viterbi log score for each sequence of observation
+ `src/analysis.py`: Runs the viterbi algorithm on each gene and calculates the adaptation score
+ `src/utils.py`: Helper functions (loading data, processing etc)

Parameters that affect behavious:
+ `num_paths`: higher number of paths provides more insight into alternative adaptation patterns but also increases computational cost.
+ `max_codons`: smaller values speed up training but reduce accuracy of codon usage estimates, higher values increase accuracy but als increase runtime of training.

Example command lines:
```
python -m src.main train --max_codons 100000
python -m src.main analyze --num_paths 3 --output_file "results/influenza.txt"
```

# Limitations and Assumptions

Key Assumptions:
+ Human CDS accurately represents human codon usage bias.
+ Training data sequences are of lengths that are multiples of 3, since all data used are coding sequences (the algorithm will not fail if they aren't but will just exclude the remaining bases)
+ Sequences are properly aligned and in-frame.

Limitations:
+ Model simplicity: The HMM model has 2 states, which might be oversimplifying adaptation.
+ No structural/functional context: The algorithm doesn't provide any information about the protein structure or gene function. To interpret adaptation scores, the user would have to research the gene's function independently.
+ Top-k viterbi complexity: Computing multiple optimal paths increases runtime and memory usage, especially for longer sequences.
+ Sensitivity to parameters: Transition/Emission probabilities can affect results.
+ Sequences with characters that represent uncertainity like `N`, `R`, etc, are replaced randomly with one of the `ATGC` characters that they represent. For example, `R` could be `A` or `G` so the code randomly picks one and replaces it. This could result in inaccurate scores if a large portion of the sequence consists of these characters. This was done because replacing ambiguous bases seemed like a better trade off than removing an entire gene from the test data due to the presence of 1 or 2 ambiguos bases.


# Evidence of Correctness
This project includes multiple forms of validation:
+ Automated pipeline testing: Unit tests using `pytest` are available in the `tests/` directory. These cover preprocessing, HMM parameter intialization, Viterbi decoding and adaptation score calculation.
+ Sanity checks: The implementation enforces key invariants such as normalized probability distributions and valid Viterbi paths. these can be found in the `tests/` directory as well.
+ Synthetic data validation: The model was evaluated on synthetic datasets, as shown in `notebooks/test.ipynb`.
+ Top k decoding validation: This model returns multiple high probability paths to capture uncertainty in hidden state assignments.

A detailed description of the validation for this project is available in `test/TESTING.md`.
