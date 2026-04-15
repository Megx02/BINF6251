# Automated Unit Tests

This directory includes multiple unit test scripts implemented using `pytest`
To run the tests, run this from the root directory `Final_Project`:
```
pytest
```

## Test Coverage

**Preprocessing and Utilities**
+ Parses input files correctly
+ Validates and cleans sequences
+ Splits sequences into codons
+ Generates all 64 codons

**HMM**
+ Initialization of start probabilities
+ Normalization of transition probabilities (they sum up to 1 for each state)
+ Normalization of emission probabilities (they sum up to one for each state)
+ Correct structure of emission distributions (all states and possible observations are present)

**Viterbi Decoding**
+ Handles empty inputs correctly
+ Decodes correctly for single and multiple observations
+ Validation on known toy example with a determined outcome
+ Generates top k paths correctly
+ Output format is correct

**Adptation Scoring**
+ Correctly calculates adaptation score
+ Edge cases:
    + Completely adapted sequence
    + Completely not adapted sequence
    + Mixed sequence


# Sanity checks and Invariants
The implementation checks for:
+ Transition probabilities sum up to 1 for ecah state
+ Emission probabilities sum up to 1 for each state
+ Output paths have a length equal to the number of observatios
+ Adaptation scores are within [0,1]

# Synthetic Data Validations
To evaluate model behavious, the pipeline was tested on two synthetic datasets:
+ Human-like sequences, generated to reflect human codon usage.
+ Random sequences, generated from a uniform codon distribution

Observations:
+ Human-like sequences produced higher and consistent adaptation score
+ Random sequences produced lower more variable scores
+ Both datasets showed a non-normal distribution (p < 0.05), so the Mann-Whitney U test was used to compare the distributions.
+ The resulting p-values was < 0.05, indicating a statistically significant difference between the human-like sequences and random sequences.
