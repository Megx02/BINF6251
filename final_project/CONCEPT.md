# Recap of Project
This project investigates whether different genes of the Influenza A virus show different levels of adaptation to human codon usage. Viruses rely on host translation machinery to produce proteins. Codon usage bias may affect translation efficiency, meaning viral genes that match host codon usage may be translated more efficiently. 
The algorithm to be implemented for this project is the Viterbi algorithm from of the Hidden Markov Model (HMM) class. The HMM will model codon sequences with hidden states representing different levels of host codon adaptation (ex: adapted, not adapted). The Viterbi algorithm will be used to determine the most likely sequence of hidden states for a viral gene sequence. 
This project will work with nucleotide sequence data:
+ FASTA file for host organism (Human) - human coding sequences (CDS), source: NCBI RefSeq
+ FASTA file for virus (Influenza A) - sequences from different genes, source: NCBI GenBank
Human sequences will be used to estimate codon emission probabilities for adapted states and the viral gene sequences will be evaluated using the trained HMM.

# Inputs, Outputs and Assumptions
## Input
1. Host coding sequences
+ Input Format: FASTA file of sequences
+ Data type: List of nucelotide sequences
+ Will be used to train the HMM model by estimating codon emission probabilities for adapted states

2. Viral gene sequences
+ Input Format: FASTA file of sequences
+ Data type: Dictionary of gene id and sequence 

3. HMM Parameters:
+ Hidden states
+ Transition probabilities between states
+ Pseudocount value

## Output
1. Sequence of states for each viral gene

Example:
```
Gene_A: Adapted, Adapted, Adapted, Not Adapted, Not Adapted ...
```
2. Adaptation score per gene

Example:
```
Gene_A: 0.72
Gene_B: 0.3
Gene_C: 0.92
```

## Assumptions
+ All sequences contain only A, C, G and T and they are uppercase.
+ Sequences are of lengths that are mutliples of 3.
+ Distribution of codons for not adapted state is uniform (1/64)

# Detailed Pseudocode
```
Algorithm overview:
1. Convert human sequences into codons.
2. Estimate codon emission probabilities from human sequences.
3. Run the Viterbi algorithm on the viral genes.
4. Calculate adaptation score for each viral gene.
```
```
1. Load the human sequences from FASTA file
    def load_training_data(human_CDS_filename)
        Filter sequences based on length (should be a multiple of 3) and invalid characters (should only contain A, C, G and T)
        Append sequences from human_CDS_filename to a list -> human_sequences
        return list of sequences

2. Split sequences into codons
    def split_into_codons(sequences)
        Initialize an empty list to store the codons -> codons
        For each sequence in the sequences:
            For i from 0 to len(sequence)-3, step 3:
                codon = sequence[i: i+3]
                Append codon to codons
        return list of codons

3. Estimate codon emission probabilities from list of codons from human sequences
    def compute_emission_probabilities(human_codons)
        Initialize a dictionary for all 64 codons with pseudocounts -> codon_counts[codon] = pseudocount

        Get counts for each codon in the human sequence:
        For codon in human_codons:  
            codon_counts[codon] += 1
        
        total_codons = sum of all codons in list of codons
        
        Convert the counts to emission probabilities 
            For each codon:
                emission[adapted][codon] = codon_counts[codon]/total_codons
                emission[not_adapted][codon] = 1/64 -> Assuming uniform distribution for non adapted state
        return emission

4. Define HMM parameters -> this is a separate step in the process but doesn't need to be a separate function since it is just defining certain parameters

        states = {adapted, not_adapted}
        
        start_probabilities:
        start[adapted] = 0.5
        start[not_adapted] = 0.5

        transition probabilities:
        transition[adapted][adapted] = 0.7
        transition[adapted][not_adapted] = 0.3
        transition[not_adapted][not_adapted] = 0.7
        transition[not_adapted][adapted] = 0.3

5. Viterbi algorithm   
    def viterbi(observations, states, transition, emission, start)
        N = length of observations
        If N == 0: -> edge case
            return empty list for state sequence

        create a matrix V[state][n] to store best log probabilities  
        create a matrix T[state][n] to store best previous state

        Initialization step (for the first codon):
            For each state s:
                V[s][0] = log(start[s]) + log(emission[s][observations[0]]) -> start probability for the state and emission probability of the codon for that state
                B[s][0] = None
        
        Recursion step:
            For n from 1 to N-1:
                For each state s in states:
                    Initialize best probability and best previous state
                    best_prob = -infinity 
                    best_prev_state = None

                    For each previous state p in states: -> we calculate the probability for all the possible states to see which is the optimal state
                        prob = V[p][n-1] + log(transition[p][s]) + log(emission[s][observations[n]]) -> probability of the previous state, transition probability to current state and emission probability of the codon for the current state

                        if prob > best_prob:
                            Update the best probability and the current optimal state to become the best previous state
                            best_prob = prob
                            best_prev_state = p
                    Save the best probability and the best previous state in their respective matrices
                    V[s][n] = best_prob
                    B[s][n] = best_prev_state

            call traceback function to get optimal state path
            return state_sequence

6. Traceback
    def traceback(V, T, states, N)
        best_final_state = state with maximum V[state][N-1]

        Initialize empty list to store path of states throughout the sequence -> state_sequence = []
        current_state = best_final_state

        For n from N-1 to 0: -> going backwards since we traceback from the last state to get the optimal path
            Append current_state to state_sequence
            current_state = T[current_state][n] -> this is where we stored the best previous state
        Reverse state_sequence (since we appended states starting from the final state)
        return state_sequence

7. Load the viral genes from FASTA file, split the sequences into codons and run viterbi on each gene
    def viral_genes(virus_filename)
        Filter sequences based on length (should be a multiple of 3) and invalid characters (should only contain A, C, G and T)
        viral_genes = dictionary -> {gene_id: sequence} from virus_filename

        For each gene in the viral_genes:
             sequence = viral_genes[gene_id]
             convert the sequence into a list of codons -> observations -> call split_into_codons function here
             run viterbi on the observations -> call viterbi function here
             compute adaptation score for gene -> call adaptation score function here
             store gene id, state sequence and adaptation score in a dictionary -> {gene_id:(state_sequence, adaptation_score)}

8. Compute adaptation score:
    def adaptation_score(state_sequence)
        If state_sequence is an empty list: -> edge case
            adapted_proportion = None
        else:
            adapted_count = number of adapted states in state_sequence
            adapted_proportion = adapted_count/Total number of states in state_sequence 
                       
        return adapted_proportion
```

# Complexity and Bottlenecks
With N = the number of codons, V = the number of viral genes, H = total number of codons in the host dataset and S = the number of states 

Emission probability estimation:
+ Time Complexity: O(H) 
+ Space Complexity: O(S x 64) -> since there are 64 possible codons

Viterbi algorithm (per sequence):
+ Time complexity: O(N x S^2) per gene
+ Space complexity: O(N x S)

Total estimated runtime: O(V x N x S^2 + H)  -> here N is the average number of codons per gene

+ The most expensive step is the Viterbi dynamic programming loop. It runs for every viral gene and it scales with sequence length. However, since the number of states is small (I currently have 2 states), it shouldn't cause too much of an issue even for long viral genes.
+ Large host training datasets may slow down HMM training. Counting codons can become slow for large number of human CDS sequences. This is a one time cost though, unlike the Viterbi algorithm step.

Performance might become an issue if/when:
+ I scale up to large viral datasets.
+ I increase the number of states S (since the time complexity for the Viterbi algorithm is S^2).
+ The sequences I process are very long.

Example:
If I move from my current plan of 2 states to 5 states, complexity increases from 4N to 25N per gene

Mitigation strategies:
+ Precomputation of emission probabilities - I will compute the emission probabilities once and reuse them to avoid recounting codons.
+ Model simplification - I can keep the number of states S small, unless it becomes necessary that I increase it. Currently my plan has an S value of 2.
+ Parallelization - If the number of viral genes is large, I can run Viterbi on multiple genes in parallel.

# Validation and Testing Plan
1. Small, hand-crafted example
I will create a small codon sequence and control the emission probabilities to check if the algorithm gives the output I expect.
Example:
```
viral_gene = {"gene_1":"AGATTAGCGCGA"}
codons = ["AGA", "TTA", "GCG", "CGA"]
```
I will define the emission probabilities such that ```"AGA"``` and ```"TTA"``` have high probabilities in the adapted state and ```"GCG"``` and ```"CGA"``` have low probabilities in the adapted state.

Expected result:
```
gene: gene_1
state_sequence: adapted, adapted, not_adapted, not_adapted
adaptation_score: 0.5
```
+ The algorithm should give a sequence of states with a clear switch when encountering codons with different probabilities.
+ The output sequence of states shouldn't be completely uniform despite there being codons of different probabilities, but it also shouldn't switch constantly alternating between states for every codon such as 
```adapted, not adapted, adapted, not adapted ...```

2. Synthetic dataset
I will generate two types of sequences:
+ Human-like sequences: I will sample codons based on the human codon frequency distribution used to train the model.
+ Random sequences: I will sample codons uniformly from all 64 codons.

Expected results:
+ High fraction of adapted states for human-like sequences and lower fraction of adapted states for random sequences.
+ If both datasets produce similar adaptation levels it indicates that the algorithm may be incorrect.

Statistical validation: I will compare adaptation scores between human-like sequences and random sequences using a t-test.

Stress testing: I will run the algorithm on very long sequences (3-5 times the average viral gene length) and sequences with extreme codon patterns like a single codon repeating throughout the sequence or switching between human-like and random codons frequently to see if the algorithm still behaves as expected. 

3. Automated tests
+ Unit tests: Verify that each function (ex: read fasta file, split into codons, emission probability calculation, etc) return the expected outputs. This is to check for any coding errors and make sure each subfunction works.
+ Edge case tests for empty sequences, sequence of a length not divisible by 3, invalid characters, etc.
+ Property check: Check that transition probabilities and emission probabilities sum up to 1 individually, final path length is equal to the number of codons.
+ End-to-end test: Run the full pipeline on a small sample dataset to validate that all the components of the algorithm work correctly.

# Updated Pitfall and Risk Log
Pitfalls from Part 1:
1. Data quality issues: This has been mitigated by filtering sequences before processing for things like length, invalid characters, etc.
2. Zero-probability emissions for rare codons: This has also been mitigated by including a pseudocount, however, testing needs to be done to determine the optimal pseudocount value.
3. True viral gene adaptation levels aren't known: This is still a relevant issue. Although I have mentioned the use of sample data for validation of the model, to validate the results, I will check that the scores correlate with biological expectations (highly expressed or essential viral genes should have higher adaptation scores). Statistical tests (such as t-test) will be used to confirm whether differences between viral genes are significant, but biological validation will determine whether the scores are meaningful.  

New pitfalls: 
1. Oversimplification of states
+ Using only "adapted" and "not adapted" might not reflect the complete variability of codon adaptation. 
+ Mitigation: I will start with these two states and see how the model works and possibly increase the number of states depending on the output. I will need to keep in mind though that increasing the number of states increases the time complexity.

2. Parameter choices
+ The results will depend largely on the choice of parameters like the pseudocount value and the transition probabilities.
+ Mitigation: I will test multiple values for parameters.


