import math
import pytest
from src.utils import generate_all_codons, count_codons_from_fasta
from src.hmm import HMM
import src.hmm as hmm


def test_initialize_parameters():
    model = HMM()
    model.initialize_parameters()

    for s in model.states:
        assert s in model.start_probs
        assert isinstance(model.start_probs[s], float)

    
    probs = [math.exp(model.start_probs[s]) for s in model.states]
    assert pytest.approx(sum(probs), 0.0001) == 1.0

    for s in model.states:
        row = model.transition_probs[s]

        assert set(row.keys()) == set(model.states)

        probs = [math.exp(row[t]) for t in model.states]
        assert pytest.approx(sum(probs), 0.0001) == 1.0


def emission_probs_structure(monkeypatch):
    model = HMM()

    fake_codons = ["ATG", "GTC"]
    def fake_generate_all_codons():
        return fake_codons
    
    def fake_count_codons_from_fasta(filename, max_codons):
        return {"ATG": 2, "GTC":3}
    
    monkeypatch.setattr(hmm, "generate_all_codons", fake_generate_all_codons)
    monkeypatch.setattr(hmm, "count_codons_from_fasta", fake_count_codons_from_fasta)

    model.train_emission_probs_from_fasta("fake.fasta", 15)

    assert "A" in model.emission_probs
    assert "N" in model.emission_probs

    for codon in fake_codons:
        assert codon in model.emission_probs["A"]
        assert codon in model.emission_probs["N"]


    probs_A = [math.exp(model.emission_probs["A"][c]) for c in fake_codons]
    assert pytest.approx(sum(probs_A), 0.0001) == 1.0

    probs_N = [math.exp(model.emission_probs["N"][c]) for c in fake_codons]
    assert pytest.approx(probs_N[0], 0.0001) == probs_N[1]
    assert pytest.approx(sum(probs_N), 0.0001) == 1.0
