def viterbi(
        observations: list[str],
        states: list[str],
        start: dict[str, float],
        transition: dict[str, dict[str, float]],
        emission: dict[str, dict[str, float]],
        K: int
        ) -> list[tuple[float, str]]:
    """ Function to compute the top k most probable hidden state sequences using the Viterbi algorithm.

    Implements a best k variant of the Viterbi algorithm for a Hidden Markov Model (HMM)
    for a given sequence of observations.

    Args:
        observations: A list of observations.
        states: A list of hidden states in the model.
        start: A dictionary of log initial probabilities for each state.
        transition: A nested dictionary of log transition probabilities between states.
        emission: A nested dictionary of log emission probabilities for each state.
        K: The number of top sequences to return.

    Returns:
        A list of tuples, in which each tuple contains the total log probability of the path and the corresponding path.
    """

    N = len(observations)

    # Return an empty list if there are no observations
    if N == 0:
        return []
    
    # Initialize dictionaries
    V = {}  # To store best score for each state at each position
    B = {}  # To store where each score came from (backtracking)

    # Initialize list for each state (to hold K possible paths)
    for s in states:
        V[s] = [[] for i in range(N)]   
        B[s] = [[] for i in range(N)]   

    # Initialize for first observation
    for s in states:
        V[s][0] = [start[s] + emission[s][observations[0]]]
        B[s][0] = [(None, None)]

    # Fill in the values for each observation
    for n in range (1,N):
        for s in states:
            candidates = []

            # Consider all possible previous states and calculate the probability of the observation given the current state
            for p in states:
                for k_idx, prev_score in enumerate(V[p][n-1]):
                    prob = prev_score + transition[p][s] + emission[s][observations[n]]

                    # Store all the possible paths, their probabilities and their indices
                    candidates.append((prob, p, k_idx))
            
            # Sort all the possible paths by probabilities and keep only top K options
            candidates.sort(reverse=True)
            top_k = candidates[:K]

            # Save probabilities and state, index for backtracking
            V[s][n] = [x[0] for x in top_k]
            B[s][n] = [(x[1], x[2]) for x in top_k]

    # Get all the possible final states
    final_candidates = []
    for s in states:
        for k_idx, score in enumerate(V[s][N-1]):
            final_candidates.append((score, s, k_idx))

    # Keep only the top K final states
    final_candidates.sort(reverse=True)
    final_candidates = final_candidates[:K]

    # Reconstruct the path by following the backpointers
    def backtrack(state, k_idx):
        path = [state]
        for t in range(N-1, 0, -1):
            prev_state, prev_k = B[state][t][k_idx]
            path.append(prev_state)
            state, k_idx = prev_state, prev_k
        path.reverse()

        return path
    
    # Store final results in a list
    results = []
    for final_prob, state, k_idx in final_candidates:
        path = backtrack(state, k_idx)
        results.append((final_prob, "".join(path)))

    return results