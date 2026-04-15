from src.utils import split_into_codons
from src.viterbi import viterbi


def adaptation_score(state_sequence: str) -> float | None:
    """ Function to calculate the adaptation score of a gene from its state sequence.
    
    The adaptation score is calculated by counting the number of states labelled "A" in the sequence and
    dividing that by the total number of states.

    Arg:
        state_sequence: A string of the hidden states in the path.

    Returns:
        The adapttaion score as a float between 0 and 1, None if the sequence is empty

    Examples:
        >>> adaptation_score("ANNN")
        0.25
    """
    
    # Return None if there is no sequence of states
    if not state_sequence:
        return None 

    adapted_count = state_sequence.count("A")
    adaptation_score = adapted_count/len(state_sequence)

    return adaptation_score


def analyze_genes(seq_dict: dict[str, str], hmm, K: int) -> dict[str, dict]:
    """ Function to analyze genes using a Hidden Markov Model (HMM) and Viterbi decoding.

    For each gene, the function splits its sequence into codons, runs Viterbi on it to get the top K paths of hidden
    states, calculates the adaptation scores for each path and calculates an average adaptation score per gene.

    Args:
        seq_dict: Dictionary mapping gene IDs to their corresponding DNA sequences.
        hmm: A Hidden Markov Model.
        K: Number of top Vitebri paths to compute.

    Retruns:
        A dictionary mapping the gene IDs to their analysis results.
    """

    gene_results = {}
    
    for gene_id, seq in seq_dict.items():
        # Split the sequence into codons
        codons = split_into_codons(seq)

        # Run viterbi to get top K paths
        paths = viterbi(codons, hmm.states, hmm.start_probs, hmm.transition_probs, hmm.emission_probs, K=K)

        scored_paths = []
        adaptation_scores = []
        viterbi_scores = []

        # Score each path
        for viterbi_log_score, path in paths:
            a_score = adaptation_score(path)
            scored_paths.append({"path" : path, "adaptation_score" : a_score, "viterbi_log_score" : viterbi_log_score})

            adaptation_scores.append(round(a_score, 3))
            viterbi_scores.append(round(viterbi_log_score, 3))

        # Calculate average score for each gene
        avg_adaptation_score = round(sum(adaptation_scores)/len(scored_paths), 3)

        gene_results[gene_id] = {
            "paths": scored_paths,
            "avg_adaptation_score": avg_adaptation_score,
        }

    return gene_results


def write_genes_ranked_in_order(gene_results: dict[str, dict], output_file: str) -> None:
    """ Function to write genes ranked by adaptation score to a file.

    Args:
        gene_results: Dictionary of gene analysis results.
        output_file: Path to the output file.

    Returns:
        None    
    """
    # Sort genes by average adaptation score in decreasing order.
    sorted_genes = sorted(gene_results.items(), key=lambda item: item[1]["avg_adaptation_score"], reverse=True)

    # Write results to file
    with open(output_file, "w") as f:
        for rank, (gene_id, data) in enumerate(sorted_genes, start=1):
            f.write(f"Rank {rank}: {gene_id}\n")
            f.write(f"Average adaptation score: {data['avg_adaptation_score']}\n\n")
            