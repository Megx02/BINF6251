import math
import pytest

from src.hmm import HMM
import src.hmm as hmm


def test_initialize_parameters():
    model = HMM()
    model.initialize_parameters()

    # Start probabilities should exist for every state and should be floats
    for s in model.states:
        assert s in model.start_probs
        assert isinstance(model.start_probs[s], float)

    # Convert log start probabilities back to normal space and check that probabilities sum up to 1
    probs = [math.exp(model.start_probs[s]) for s in model.states]
    assert pytest.approx(sum(probs), 0.0001) == 1.0


    for s in model.states:
        trans_probs = model.transition_probs[s]

        # Check that every state is present in the transition probability dictionary
        assert set(trans_probs.keys()) == set(model.states)

        # Check that transition probabilities sum up to 1 for each state
        probs = [math.exp(trans_probs[t]) for t in model.states]
        assert pytest.approx(sum(probs), 0.0001) == 1.0


def test_emission_probs_structure(monkeypatch):
    model = HMM()

    # Small codons set for testing
    fake_codons = ["ATG", "GTC"]

    def fake_generate_all_codons():
        return fake_codons
    
    # Fake codon counts for testing
    def fake_count_codons_from_fasta(filename, max_codons):
        return {"ATG": 2, "GTC":3}
    
    # Replace real functions with controlled test doubles
    monkeypatch.setattr(hmm, "generate_all_codons", fake_generate_all_codons)
    monkeypatch.setattr(hmm, "count_codons_from_fasta", fake_count_codons_from_fasta)

    model.train_emission_probs_from_fasta("fake.fasta", 15)

    # CHeck that the model contains emission probabilities for both states
    assert "A" in model.emission_probs
    assert "N" in model.emission_probs

    # Check that each codon is present in the emission probability distribution
    for codon in fake_codons:
        assert codon in model.emission_probs["A"]
        assert codon in model.emission_probs["N"]

    # Emission probabilities for "A" should sum up to 1 
    probs_A = [math.exp(model.emission_probs["A"][c]) for c in fake_codons]
    assert pytest.approx(sum(probs_A), 0.0001) == 1.0

    # Emission probabilities for "N" should sum up to 1 and be uniformly distributed
    probs_N = [math.exp(model.emission_probs["N"][c]) for c in fake_codons]
    assert pytest.approx(probs_N[0], 0.0001) == probs_N[1]
    assert pytest.approx(sum(probs_N), 0.0001) == 1.0
