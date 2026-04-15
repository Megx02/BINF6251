import gzip
import random


def is_valid_sequence(seq: str) -> tuple[str, bool]:
    """ Function that checks if a DNA sequence is valid and replaces ambiguous bases.
     
    Replaces IUPAC ambiguity characters with randomly selected valid bases and verifies that 
    the resulting sequence is not empty.
       
    Args:
        seq: the input DNA sequence.
    
    Returns:
        A tuple with the cleaned sequence and a boolean indicating validity.

    Examples:
        >>> is_valid_sequence("ATGN")
        ("ATGA", True)

        >>> is_valid_sequence("")
        ("", False)
    """

    # IUPAC ambiguity code replacements
    iupac = {
        'R': ['A', 'G'],
        'Y': ['C', 'T'],
        'S': ['G', 'C'],
        'W': ['A', 'T'],
        'K': ['G', 'T'],
        'M': ['A', 'C'],
        'B': ['C', 'G', 'T'],
        'D': ['A', 'G', 'T'],
        'H': ['A', 'C', 'T'],
        'V': ['A', 'C', 'G'],
        'N': ['A', 'C', 'G', 'T']
    }
    
    # Replace ambiguous characters with random valid bases
    cleaned = ''.join(random.choice(iupac[b]) if b in iupac else b for b in seq)
    
    # Check if the sequence is empty and return False if it is
    if len(cleaned) == 0:
        return seq, False
    
    return cleaned, True


def split_into_codons(sequence: str) -> list[str]:
    """ Function to split a DNA sequence into codons. 
    
    Iterates through the sequence in steps of three to split the sequence into codons.

    Args:
        sequence: The DNA sequence to split.

    Returns:
        A list of codons.

    Examples:
        >>> split_into_codons("ATGCCG")
        ["ATG", "CCG"]
    """

    # Initialize empty list to store codons
    codons = []

    # Loop through the sequence 3 bases at a time
    for i in range(0, len(sequence)-2, 3):
        codons.append(sequence[i:i+3])

    return codons


def generate_all_codons() -> list[str]:
    """ Function to generate all possible codons. 
    
    Generates all combinations of the bases A, T, G and C to produce a list of the 64 codons.

    Args:
        No args

    Retruns:
        A list of the 64 codons,
    """

    bases = ["A", "C", "G", "T"]
    codons = []

    # Generate all combinations of three bases
    for i in bases:
        for j in bases:
            for k in bases:
                codons.append(i+j+k)

    return codons


def open_file(filename: str):
    """ Function to open a file, supporting both plain text and gzip files.
    
    Args:
        filename: Path to the file.

    Returns:
        An opened file in read mode.
    """

    # Check if the file is a gzip file and open it appropriately with gzip
    if filename.endswith(".gz"):
        return gzip.open(filename, "rt")
    # Open file normally if not gzip
    else:
        return open(filename, "r")


def load_fasta_dict(filename: str) -> dict[str, str]:
    """ Function to load sequences from a file into a dictionary.

    Parses a file and stores valid sequences and their corresponding IDs.

    Args:
        filename: Path to file.

    Returns:
        A dictionary mapping sequence IDs to their corresponding DNA sequences.    
    """

    data = {}           # Dictionary to store sequences with their IDs
    current_ID = None   # Tracks current sequence ID
    current_seq = ""    # Accumulates sequence from lines 


    # Open and read the FASTA file
    with open_file(filename) as f:
        for line in f:
            line = line.strip()

            # Check if line is a header line
            if line.startswith(">"):
                if current_ID is not None:

                    # Save sequence if it is valid
                    current_seq, valid = is_valid_sequence(current_seq)

                    if valid:
                        if len(current_seq) % 3 == 0:
                            data[current_ID] = current_seq
                        else:
                            print(f"INVALID: {current_ID}, length: {len(current_seq)}")
                    else:
                        print(f"INVALID: {current_ID}, presence of invalid characters.")

                # Update sequence and ID
                line = line.split()
                current_ID = line[0][1:] # Gets the first part of the header and removes '>'
                current_seq = ""
            
            else:
                # Add seqeunce lines together and convert all the characters to uppercase
                current_seq += line.upper()
        
        # Add the last sequence
        if current_ID is not None and current_seq:
                current_seq, valid = is_valid_sequence(current_seq)
                if valid:
                    if len(current_seq) % 3 == 0:
                        data[current_ID] = current_seq
                    else:
                        print(f"INVALID: {current_ID}, length: {len(current_seq)}")
                else:
                    print(f"INVALID: {current_ID}, presence of invalid characters.")
    
    return data


def count_codons_from_fasta(filename: str, max_codons: int) -> dict[str, int]:
    """ Function to count codon frequencies from a file.
    
    Reads sequences from a file, validates them and counts frequency of each codon up 
    to a specified maximum number of total codons.

    Args:
        filename: Path to file.
        max_codons: Maximum number of codons to count.

    Returns:
        A dictionary mapping each codon to its frequency.
    """

    # Generate all 64 codons
    all_codons = generate_all_codons()
    # Initialize counts to 0 for each codon
    codon_counts = {codon: 0 for codon in all_codons}

    # Track total number of codons
    total_codons = 0
    seq = ""

    with open_file(filename) as f:
        for line in f:
            line = line.strip()

            # Reset sequence at header line
            if line.startswith(">"):
                seq = ""
                continue

            # Check if sequence is valid
            cleaned, valid = is_valid_sequence(line.upper())
            if not valid:
                continue
            
            # Append the cleaned sequence
            seq += cleaned

            i = 0
            # Process the sequence as codons
            while len(seq) - i >= 3:
                codon = seq[i:i+3]
                i += 3

                if len(codon) != 3:
                        break
                
                codon_counts[codon] += 1
                total_codons += 1

                # Stop counting if maximum number of codons has been reached
                if max_codons and total_codons >= max_codons:
                    return codon_counts
            
            # Keep the leftover bases for the next iteration
            seq = seq[i:]
    
    return codon_counts
