import math
from src.viterbi import viterbi


def test_empty_observations():
    result = viterbi([], ["A", "B"], {}, {}, {}, K=1)
    assert result == []


def test_single_observation():
    observations = ["x"]
    states = ["A", "B"]

    start = {"A": math.log(1), "B": float("-inf")}
    emission = {
        "A": {"x": math.log(1)},
        "B": {"x": float("-inf")}
    }
    transition = {
        "A": {"A": math.log(1), "B": float("-inf")},
        "B": {"A": float("-inf"), "B": math.log(1)}
    }

    result = viterbi(observations, states, start, transition, emission, K=1)

    # A should win (higher log prob)
    assert result[0][1] == "A"


def test_simple_known_case():
    # Classic tiny HMM
    observations = ["x", "y"]
    states = ["A", "B"]

    start = {"A": math.log(1), "B": float("-inf")}

    emission = {
        "A": {"x": math.log(1), "y": float("-inf")},
        "B": {"x": float("-inf"), "y": math.log(1)}
    }

    transition = {
        "A": {"A": float("-inf"), "B": math.log(1)},
        "B": {"A": math.log(1), "B": float("-inf")}
    }

    result = viterbi(observations, states, start, transition, emission, K=1)

    # Best path should be A -> B
    assert result[0][1] == "AB"


def test_top_k_paths():
    observations = ["x", "y"]
    states = ["A", "B"]

    start = {"A": math.log(1), "B": float("-inf")}

    transition = {
        "A": {"A": math.log(0.5), "B": math.log(0.5)},
        "B": {"A": math.log(0.5), "B": math.log(0.5)}
    }

    emission = {
        "A": {"x": math.log(0.5), "y": math.log(0.5)},
        "B": {"x": math.log(0.5), "y": math.log(0.5)}
    }

    result = viterbi(observations, states, start, transition, emission, K=2)

    # There are multiple equally good paths
    assert len(result) == 2

    paths = [p for _, p in result]
    assert all(len(p) == 2 for p in paths)


def test_output_format():
    observations = ["x"]
    states = ["A"]

    start = {"A": math.log(1.0)}
    transition = {"A": {"A": math.log(1.0)}}
    emission = {"A": {"x": math.log(1.0)}}

    result = viterbi(observations, states, start, transition, emission, K=1)

    prob, path = result[0]

    assert isinstance(prob, float)
    assert isinstance(path, str)