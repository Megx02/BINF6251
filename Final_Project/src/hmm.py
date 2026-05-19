import math

from src.utils import *


class HMM:
    """ Hidden Markov Model """

    def __init__(self, pseudocount: float = 1.0):
        self.states = ["A", "N"]
        self.pseudocount = pseudocount

        self.start_probs = {}
        self.transition_probs = {}
        self.emission_probs = {}

    
    def initialize_parameters(self) -> None:
        """ Function to initialize start and transition probabilities in log space.
        
        Start probabilities are uniform across the states.
        Transition probabilities are biased toward staying the same.
           """

        num_states = len(self.states)

        # Equal start probabilities for each state
        for s in self.states:
            self.start_probs[s] = math.log(1.0/num_states)

        # Transiion probabilities
        for s in self.states:
            self.transition_probs[s] = {}

            for t in self.states:
                if s == t:
                    prob = 0.7
                else:
                    prob = 0.3/(num_states -1) # Split the probability among the remaining states

                self.transition_probs[s][t] = math.log(prob)
    

    def train_emission_probs_from_fasta(self, fasta_filename: str, max_codons: int) -> None:
        """ Function to estimate emission probabilities from training data.

        Uses codon counts from traning data to estimate emission probabilities and adds a pseudocount.
        Probabilities are stored in log space.
        This is a more memory efficient way to estimate emisison probabilities from the human CDS fasta file. 
        It avoids storing the sequences from the file since we only need codon counts.

        Args:
            fasta_filename: Path to FASTA file for training.
            max_codons: Maximum number of codons to use from the file to train the model on.
        """

        # Get all the possible codons
        all_codons = generate_all_codons()

        # Get codon counts for each codon from the training data
        codon_counts = count_codons_from_fasta(fasta_filename, max_codons)

        # Add pseudocount for each codon
        for codon in all_codons:
            codon_counts[codon] += self.pseudocount

        total_count = sum(codon_counts.values())

        # Initialize emission probability dictionary
        for s in self.states:
            self.emission_probs[s] = {}

        # Calculate emission probabilities for codons in "adapted" state from the codon counts
        # Set uniform emission probabilities for "not_adapted" state 
        for codon in all_codons:
            self.emission_probs["A"][codon] = math.log(codon_counts[codon]/total_count)
            self.emission_probs["N"][codon] = math.log(1.0/len(all_codons))
