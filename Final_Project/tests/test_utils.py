import gzip
import os
import tempfile

from src.utils import *


def test_valid_sequence_clean():
    seq = "ATGAAA"
    cleaned, valid = is_valid_sequence(seq)

    assert cleaned == seq
    assert valid is True


def test_empty_sequence():
    seq = ""
    cleaned, valid = is_valid_sequence(seq)

    assert valid is False


def test_split_into_codons():
    seq = "ATGTTAGTG"
    codons = split_into_codons(seq)

    assert codons == ["ATG", "TTA", "GTG"]


def test_generate_all_codons():
    codons = generate_all_codons()

    assert len(codons) == 64


def create_fast_file(content: str):
    tmp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    tmp.write(content)
    tmp.close()

    return tmp.name


def test_load_fasta():
    content = ">seq1\nATGTTACTA\n>seq2\nTGTATTGCG"
    filename = create_fast_file(content)
    data = load_fasta_dict(filename)

    assert data["seq1"] == "ATGTTACTA"
    assert data["seq2"] == "TGTATTGCG"

    os.remove(filename)


def test_load_fasta_uppercase():
    content = ">seq1\natggtg"
    filename = create_fast_file(content)
    data = load_fasta_dict(filename)

    assert data["seq1"] == "ATGGTG"

    os.remove(filename)


def test_load_fasta_empty():
    content = ""
    filename = create_fast_file(content)
    data = load_fasta_dict(filename)

    assert data == {}

    os.remove(filename)
    

def test_load_fasta_invalid():
    content = ">seq1\nATGT"
    filename = create_fast_file(content)
    data = load_fasta_dict(filename)

    assert data == {}

    os.remove(filename)


def create_test_fasta_file(content: str):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".gz")
    tmp.close()
    with gzip.open(tmp.name, "wt") as f:
        f.write(content)

    return tmp.name


def test_count_codons():
    fasta_content = ">seq1\nATGAAATTA\n>seq2\nTTGATGTTA"
    filename = create_test_fasta_file(fasta_content)
    counts = count_codons_from_fasta(filename)

    assert counts["ATG"] == 2
    assert counts["AAA"] == 1
    assert counts["TTA"] == 2
    assert counts["TTG"] == 1

    os.remove(filename)


def test_count_codons_with_codon_limit():
    fasta_content = ">seq1\nATGAAATTA\n>seq2\nTTGATGTTA"
    filename = create_test_fasta_file(fasta_content)
    counts = count_codons_from_fasta(filename, max_codons=4)    
    total = sum(counts.values())

    assert total == 4

    os.remove(filename)
