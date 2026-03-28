# Project Title
Identification of Gene-Specific Codon Adaptation of Influenza A to the Human Host

# Research Question
Do all genes of the Influenza A virus show the same level of adaptation to human codon usage or do different functional gene groups exhibit different levels of host-specific codon adaptation?

Viruses depend on host translational machinery to produce their proteins. Since translational efficiency can be influenced by codon usage, viral genes that match human codon preferences better may be translated more efficiently. While overall viral codon usage adaptation has been studied, gene-level heterogeneity within the viral genome is less explored. 

Understanding whether codon adaptation varies by gene function could provide information about how a virus balances replication efficiency, immune evasion and evolutionary flexibility. Successfully identifying differences in host codon adaptation among viral genes could also provide insights into newly sequenced viruses whose genes have very little experimental information.

# Algorithm and Algorithm Class
**Algorithm Class:** Hidden Markov Models

**Algorithm:** Viterbi Algorithm

I chose Hidden Markov Models for this project because codon adaptation may not be uniform across the viral genome. HMMs let us model the sequential structure in terms of hidden adaptation states and identify which regions are more adapted and which are less adapted. The Viterbi algorithm can identify the most likely assignment of adapted and non-adapted states along each gene, which can show how adaptation varies at the gene-level. 

# Data Plan
Host organism - Homo sapiens (I plan on using only the coding sequences)

Virus - Influenza A Virus

**Sources:**
+ Human coding sequences from NCBI RefSeq
+ Viral reference genome and gene annotations from NCBI GenBank

**Data type(s):**
+ FASTA nucleotide sequences
+ Coding sequence (CDS) annotations

**Licensing or access:**
+ NCBI data is publicly available.

**Prototype data plan:**

I will use a subset of the host coding sequences (about 50) and 2-3 viral genes for testing and debugging.

Once the algorithm is validated with the prototype data, it can be scaled up to the full human coding sequence dataset and the full viral gene set.


# Success Criteria
Success for my project is being able to determine whether specific viral genes or genome regions show stronger adaptation to host codon usage than others.
## Expected Outputs
1. A Hidden Markov Model trained using host codon usage.
2. Transition probability matrix between hidden states.
3. Comparative analysis of adaptation levels of the different viral genes.

One way to check if my result is reasonable is to test a sample of the host coding sequences as well as a set of random or unrelated sequences under the HMM. Host coding sequences should mostly be classified as adapted while the unrelated sequences should show a lower proportion of adapted states.

# Pitfall Scan
## Data-related Issues
1. Incomplete or low-quality host CDS and errors in viral gene annotations
+ Some of the host coding sequences might have errors or be too short and some viral genomes could be missing or mislabeled in annotation files.
+ Mitigation: Filter the host coding sequences for a minimum length and check sequence quality, use curated reference genomes and verify annotations.

## Algorithmic Issues
1. Zero-probability emissions
+ Rare codons may not appear in training data, leading to zero emission probabilities.
+ Mitigation: Add pseudocounts while estimating emission probabilities.

## Evaluation Issues
1. Viral gene adaptation isn't known
+ We don't actually know the codon adaptation levels of the different viral genes.
+ Mitigation: Validate results by testing with a sample of host CDS sequences and a random sample of sequences.

# Planned Repository Structure (Initial Sketch)
```

final_project/
├── data/
├── src/
├── results/
└── PROPOSAL.md

```

# Generative AI Disclosure (If Used)

Generative AI was not used for this proposal.
