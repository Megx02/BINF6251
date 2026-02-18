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

## Algorithmic Issues

## Evaluation Issues

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


