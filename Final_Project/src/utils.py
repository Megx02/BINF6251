from typing import List, Dict
from collections import defaultdict
import gzip

def is_valid_sequence(seq: str) -> bool:
    """ Check if the sequence contains only A, C, G and T and if it's length is divisible by 3. """

    # Check if sequence length is divisble by 3, return False if not
    if len(seq) % 3 != 0:
        return False
    
    # Check if every character in the sequence is A, C, G or T, if not return False
    for base in seq:
        if base not in {"A", "C", "G", "T"}:
            return False
    
    return True


def load_fasta_dict(filename: str) -> Dict[str, str]:
    """ Returns a dictionary with ID and the correspodning sequence for the data to be analyzed. """

    data = {}           # Dictionary to store sequences with their IDs
    current_ID = None   # Tracks current sequence ID
    current_seq = ""    # Accumulates sequence from lines 


    # Open and read the FASTA file
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_ID is not None:
                    # Save sequence if it is valid
                    if is_valid_sequence(current_seq):
                        data[current_ID] = current_seq

                # Update sequence and ID
                current_ID = line[1:]
                current_seq = ""
            
            else:
                # Add seqeunce lines together and convert all the characters to uppercase
                current_seq += line.upper()
        
        # Add the last sequence
        if current_seq:
                data[current_ID] = current_seq
    
    return data


def split_into_codons(sequence: str) -> List[str]:
    """ Splits a sequence into codons. """

    # Initialize empty list to store codons
    codons = []

    # Loop through the sequence 3 bases at a time
    for i in range(0, len(sequence)-2, 3):
        codons.append(sequence[i:i+3])

    return codons


def generate_all_codons() -> List[str]:
    """ Generates all 64 codons. """

    bases = ["A", "C", "G", "T"]
    codons = []

    for i in bases:
        for j in bases:
            for k in bases:
                codons.append(i+j+k)

    return codons


def count_codons_from_fasta(filename: str, max_codons: int = None) -> Dict[str, int]:
    """ Calculates codon count fro each codon from sequences in a fasta file. """

    all_codons = generate_all_codons()
    # Initialize counts to 0 for each codon
    codon_counts = {codon: 0 for codon in all_codons}

    # Track total number of codons
    total_codons = 0
    sequence = ""

    # Open gzipped FASTA file
    with gzip.open(filename, "rt") as f:
        for line in f:
            line = line.strip()

            if line.startswith(">"):
                if sequence:

                    # Check if sequence is valid
                    if is_valid_sequence(sequence):
                        # Split the sequence into codons
                        codons = split_into_codons(sequence)

                        for codon in codons:
                            # Stop if we reach maximum allowed codons
                            if max_codons is None or total_codons < max_codons:
                                # Increase the count for the codon and the total number of codons
                                codon_counts[codon] += 1
                                total_codons += 1
                            else:
                                break
                sequence = ""
            else:
                sequence += line.upper()
        
        # Process the last sequence
        if sequence:
            codons = split_into_codons(sequence)
            for codon in codons:
                if max_codons is None or total_codons < max_codons:
                    codon_counts[codon] += 1
                    total_codons += 1
                else:
                    break
    
    return codon_counts
    