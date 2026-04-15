import gzip
import os
import tempfile

from src.utils import *


def test_valid_sequence_clean():
    # Valid sequence should remain unchanges and returned as valid
    seq = "ATGAAA"
    cleaned, valid = is_valid_sequence(seq)

    assert cleaned == seq
    assert valid is True


def test_empty_sequence():
    # Empty sequence should be considered invalid
    seq = ""
    cleaned, valid = is_valid_sequence(seq)

    assert valid is False


def test_split_into_codons():
    # Sequence should be split into codons
    seq = "ATGTTAGTG"
    codons = split_into_codons(seq)

    assert codons == ["ATG", "TTA", "GTG"]


def test_generate_all_codons():
    # All 64 possible codons should be generated
    codons = generate_all_codons()

    assert len(codons) == 64


def create_fast_file(content: str):
    # Helper to create a temporary plain text file
    tmp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    tmp.write(content)
    tmp.close()

    return tmp.name


def test_load_fasta():
    # Multiple sequences should be loaded into a dictionary correctly
    content = ">seq1\nATGTTACTA\n>seq2\nTGTATTGCG"
    filename = create_fast_file(content)
    data = load_fasta_dict(filename)

    assert data["seq1"] == "ATGTTACTA"
    assert data["seq2"] == "TGTATTGCG"

    os.remove(filename)


def test_load_fasta_uppercase():
    # Input sequence should be converted to uppercase
    content = ">seq1\natggtg"
    filename = create_fast_file(content)
    data = load_fasta_dict(filename)

    assert data["seq1"] == "ATGGTG"

    os.remove(filename)


def test_load_fasta_empty():
    # Empty file should return an empty dictionary
    content = ""
    filename = create_fast_file(content)
    data = load_fasta_dict(filename)

    assert data == {}

    os.remove(filename)
    

def test_load_fasta_invalid():
    # Invalid sequence sohuld return empty result
    content = ">seq1\nATGT"
    filename = create_fast_file(content)
    data = load_fasta_dict(filename)

    assert data == {}

    os.remove(filename)


def create_test_fasta_file(content: str):
    # Helper to create a temporary gzipped file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".gz")
    tmp.close()
    with gzip.open(tmp.name, "wt") as f:
        f.write(content)

    return tmp.name


def test_count_codons():
    # Count codons across sequences with no maximum number of codons
    fasta_content = ">seq1\nATGAAATTA\n>seq2\nTTGATGTTA"
    filename = create_test_fasta_file(fasta_content)
    counts = count_codons_from_fasta(filename, max_codons=None)

    assert counts["ATG"] == 2
    assert counts["AAA"] == 1
    assert counts["TTA"] == 2
    assert counts["TTG"] == 1

    os.remove(filename)


def test_count_codons_with_codon_limit():
    # Count codons across sequences with a maximum limit to the total number of codons
    fasta_content = ">seq1\nATGAAATTA\n>seq2\nTTGATGTTA"
    filename = create_test_fasta_file(fasta_content)
    counts = count_codons_from_fasta(filename, max_codons=4)    
    total = sum(counts.values())

    assert total == 4

    os.remove(filename)
