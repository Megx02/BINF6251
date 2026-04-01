from src.utils import split_into_codons
from src.viterbi import viterbi

def adaptation_score(state_sequence):
    """ Calculates the adaptation score of a gene based on its state sequence. """
    
    # Return None if there is no sequence of states
    if not state_sequence:
        return None
    
    # Set count of "adapted" states to 0
    adapted_count = 0

    # Loop through the states and increase count for every "adapted" state
    for s in state_sequence:
        if s == "A":
            adapted_count += 1

    # Calculate fraction of adapted states
    adaptation_score = adapted_count/len(state_sequence)

    return adaptation_score


def analyze_genes(seq_dict, hmm):
    """ Runs the Viterbi algorithm on the input dictionary of genes. """

    # Store results for each gene
    results = {}

    # Loop through the dictionary to process each gene
    for gene_id, seq in seq_dict.items():
        # Split sequence into codons
        codons = split_into_codons(seq)

        # Run viterbi to get the optimal state sequence for the gene
        states = viterbi(codons, hmm.states, hmm.start_probs, hmm.transition_probs, hmm.emission_probs)

        # Calculate teh adaptation score for the gene based on the state sequence
        score = adaptation_score(states)

        # Store the score and sequence of states in a dictionary
        results[gene_id] = (score, "".join(states))
    
    return results