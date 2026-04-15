import math
from src.analysis import adaptation_score


def test_adaptation_score_empty():

    score = adaptation_score("")
    assert score is None


def test_adaptation_score_all_A():

    score = adaptation_score("AAAAA")
    assert score == 1.0


def test_adaptation_score_all_N():

    score = adaptation_score("NNNNN")
    assert score == 0.0


def test_adaptation_score():

    score = adaptation_score("AANN")
    assert score == 0.5


def test_adaptation_score_bounds():
    for seq in ["AAAAA", "NNNNN", "AANN"]:
        score = adaptation_score(seq)
        assert 0.0 <= score <= 1.0
