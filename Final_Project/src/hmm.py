import math
from src.utils import *
from collections import defaultdict


class HMM:
    """ Hidden Markov Model """

    def __init__(self, states, pseudocount=1.0):
        self.states = states
        self.pseudocount = pseudocount

        self.start_probs = {}
        self.transition_probs = {}
        self.emission_probs = {}

    
    def initialize_parameters(self):
        """ Initialize start and transition probabilities (in log space). """

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
    

    def train_emission_probs_from_fasta(self, fasta_filename, max_codons=None):
        """ 
        This is a more memory efficient way to estimate emisison probabilities from the human CDS fasta file. 
        It avoids storing the sequences from the file since we only need codon counts.
        """

        all_codons = generate_all_codons()

        # Get codon counts for each codon from the training data
        codon_counts = count_codons_from_fasta(fasta_filename, max_codons)

        # Add pseudocount for each codon
        for codon in all_codons:
            codon_counts[codon] += self.pseudocount

        total_count = sum(codon_counts.values())

        for s in self.states:
            self.emission_probs[s] = {}

        # Calculate emission probabilities for codons in "adapted" state from the codon counts
        # Set uniform emission probabilities for "not_adapted" state 
        for codon in all_codons:
            self.emission_probs["adapted"][codon] = math.log(codon_counts[codon]/total_count)
            self.emission_probs["not_adapted"][codon] = math.log(1.0/64.0)
