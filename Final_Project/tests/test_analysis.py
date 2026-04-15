from src.analysis import adaptation_score


def test_adaptation_score_empty():
    # Empty input should return None
    score = adaptation_score("")
    assert score is None


def test_adaptation_score_all_A():
    # Sequence with onl "A" should return 1.0
    score = adaptation_score("AAAAA")
    assert score == 1.0


def test_adaptation_score_all_N():
    # Sequence with only "N" should return 0.0
    score = adaptation_score("NNNNN")
    assert score == 0.0


def test_adaptation_score():

    score = adaptation_score("AANN")
    assert score == 0.5


def test_adaptation_score_bounds():
    # Scores should always be within [0.0, 1.0]
    for seq in ["AAAAA", "NNNNN", "AANN"]:
        score = adaptation_score(seq)
        assert 0.0 <= score <= 1.0
