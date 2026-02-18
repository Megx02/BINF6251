# 1. Project Title
Identification of Gene-Specific Codon Adaptation of Influenza A to the Human Host

# 2. Research Question
Do all genes of the Influenza A virus show the same level of adaptation to human codon usage or do different functional gene groups exhibit different levels of host-specific codon adaptation?
## Why this matters
Viruses depend on host translational machinery to produce their proteins. Since translational efficiency can be influenced by codon usage, viral genes that match human codon preferences better may be translated more efficiently. While overall viral codon usage adaptation has been studied, gene-level heterogeneity within the viral genome is less explored. 

Understanding whether codon adaptation varies by gene function could provide information about how a virus balances replication efficiency, immune evasion and evolutionary flexibility. Successfully identifying differences in host codon adaptation among viral genes could also provide insights into newly sequenced viruses whose genes have very little experimental information.

# 2. Algorithm and Algorithm Class
**Algorithm Class:** Markov Chains

**Algorithm:** First-order Markov Chain

Codons in a gene are generally not independent, the choice of one codon can infleucne the next. Markov chains model these dependencies by estimating the probability of each codon following another. Using these probabilities, we can measure how well regions of a viral genome match the host's codon usage. 

# 3. Data Plan
Host organism - Homo sapiens (I plan on using only the coding sequences)

Virus - Influenza A Virus

**Sources:**
+ Human coding sequences from NCBI RefSeq
+ Viral refernece genome and gene annotations from NCBI GenBank

**Data type(s):**
+ FASTA nucleotide squences
+ Coding sequence (CDS) annotations

**Licesning or access:**
+ NCBI data is publicly available.

**Prototype data plan:**

I will use a subset of the host coding sequences (about 50) and 2-3 viral genes for testing and debugging. This allows debugging of the MArkov model training, verification of probability normalization and testing scoring. 

Once the algorithm is validated with the prototype data, it can be scaled up to the full human coding sequence dataset and the full viral gene set.


# 4. Success Criteria
Success for my project is being able to determine whether specific viral genes or genome regions show stronger adaptation to host codon usage than others.
## Expected Outputs
1. A Markov chain model trained on host codon usage.
2. Log-likelihood scores for each viral gene under the host-trained model.
3. Comparitive analysis of scores of the different viral genes.

One way to check if my result is reasonable is to score a sample of the host coding sequences as well as a set of random or unrelated sequences under the host Markov model. The sample of host coding sequences should have high scores while the unrelated sequeces should score low.

# 5. Pitfall Scan
## Data-related Issues
1. Incomplete or low-quality host CDS
+ Some host coding sequences may have errors or be too short.
+ Mitigation: Filter for a minimum length and check sequence quality.

2. Errors in viral gene annotations
+ Some viral genes may be missing or mislabeled.
+ Mitigation: Use curated reference genomes and check annotations.

3. Limited viral samples
+ Using only a few strains may not show overall diversity of the virus.
+ Mitigation: Start with on strain for testing and then expand.

## Algorithmic Issues
1. Zero-probability codon transitions
+ Rare codon pairs may have zero probability, making log-likelihood undefined.
+ Mitigation: Add pseudocounts to all codon transitions when building the model

2. Overfitting to host dataset
+ The model may reflect only the specific host sequences used.
+ Mitigation: Cross check log-likelihood scores with a random sample of host CDS and eventually use the complete host CDS to train the model.

3. Computational limit
+ Large datasets can be difficult to handle.
+ Mitigation: Test on small subsets of data first and use efficient data structures for transition probabilities.

## Evaluation Issues
1. Viral gene adaptation isn't known
+ We don't actually know the codon adaptation levels of the different viral genes.
+ Mitigation: Validate model by testing with a sample of host CDS sequences and a random sample of sequences.

2. Sequence length effects
+ Longer genes may get higher scores because they are longer.
+ Mitigation: Normallize scores by gene length

3. Other biological factors
+ Overlapping genes or RNA structures can affect codon usage, which may change scores.
+ Focus on overall trends across genes and interpret atypical scores carefully.

# 6. Planned Repository Structure (Initial Sketch)
```

final_project/
|
|--- data/
|
|--- src/
|
|--- results/
|
|--- PROPOSAL.md

```

# 7. Generative AI Disclosure (If Used)

NA
