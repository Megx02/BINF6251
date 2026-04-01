def viterbi(observations, states, start, transition, emission):
    """ Implements the Viterbi algorithm to find the optimal sequence of hidden states for a sequence of observations using a Hidden Markov Model. """


    N = len(observations)
    # Return an empty list if there are no observations
    if N == 0:
        return []
    
    # Initialize probability matrix V and backpointer matrix B
    V = {}
    B = {}

    # Initialize all probabilities to negative infinity and all backpointers to None
    for s in states:
        V[s] = [float("-inf")] * N
        B[s] = [None] * N

    # Initialize for first observation
    for s in states:
        V[s][0] = start[s] + emission[s][observations[0]]

    # Fill in the matrices for each observation
    for n in range (1,N):
        for s in states:
            # Initialize variables to track max probability and the corresponding state
            best_prob = float("-inf")
            best_prev = None

            # Consider all possible previous states and calculate the probability of the observation given the current state
            for p in states:
                prob = V[p][n-1] + transition[p][s] + emission[s][observations[n]]

                # Update if this path is better than the current best path
                if prob > best_prob:
                    best_prob = prob
                    best_prev = p
            
            # Store the best probability and previous state (backpointer)
            V[s][n] = best_prob
            B[s][n] = best_prev

    # Find the state with the highest probability at the last observation
    best_final_score = float("-inf")
    last_state = None
    for s in states:
        if V[s][N-1] > best_final_score:
            best_final_score = V[s][N-1]
            last_state = s

    path = [last_state]
    # Find the optimal path by following the backpointers (best previous state)
    for t in range (N-1, 0, -1):
        path.append(B[path[-1]][t])
    
    # Reverse the path to get correct order from start to end
    path.reverse()

    return path