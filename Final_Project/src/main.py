import argparse
import pickle

from src.hmm import HMM
from src.analysis import analyze_genes, write_genes_ranked_in_order
from src.utils import load_fasta_dict

def save_results(results: dict[str, dict], filename: str) -> None:
    """ Function to write analysis results to a file.
    
    Args:
        results: The analysis results after running viterbi and computing adaptation scores.
        filename: Path to output file.

    Returns:
        None
    """

    with open(filename, "w") as f:
        for gene_id, data in results.items():
            f.write(f"Gene: {gene_id}\n")
            f.write(f"Average adaptation score: {data['avg_adaptation_score']}\n")

            for i, p in enumerate(data["paths"], start=1):
                f.write(f"Path {i}: {p['path']}\n")
                f.write(f"Adaptation score: {p['adaptation_score']}\n")
                f.write(f"Viterbi log-score: {p['viterbi_log_score']}\n")

            f.write("\n")

def main():

    parser = argparse.ArgumentParser(description="HMM Viterbi Tool")
    subparsers = parser.add_subparsers(dest="command")

    
    # Train subcommand
    train_parser = subparsers.add_parser("train",
                                         help="Train HMM")
    
    train_parser.add_argument("--train_data",
                              type=str,
                              default="data/GCF_000001405.40_GRCh38.p14_cds_from_genomic.fna.gz",
                              help="Path to host sequence data file")
    train_parser.add_argument("--max-codons",
                              type=int,
                              default=None,
                              help="Maximum number of codons to train on")
    
    
    # Analyze subcommand
    analyze_parser = subparsers.add_parser("analyze",
                                           help="Load and analyze viral gene data")
    
    analyze_parser.add_argument("--analysis_data",
                                type=str,
                                default="data/influenza_A_genes.txt",
                                help="Path to viral gene sequence data file")
    analyze_parser.add_argument("--num-paths",
                                type=int,
                                default=2,
                                help="Number of Viterbi paths to output")
    analyze_parser.add_argument("--output-file",
                                type=str,
                                default="results/results.txt",
                                help="Path to file to store results")



    args = parser.parse_args()

    if args.command == "train":
        print("Training HMM...")

        # Initialize and train HMM model
        hmm = HMM()
        hmm.initialize_parameters()
        hmm.train_emission_probs_from_fasta(args.train_data, args.max_codons)

        # Save trained model using pickle to avoid retraining for the same host data
        with open("hmm_model.pkl", "wb") as f:
            pickle.dump(hmm, f)

        print("Training done.")
        print("HMM model saved to hmm_model.pkl.")
        print("You can now run 'analyze' multiple times on different input data without retraining.")
        print("To retrain on new host data, run the 'train' command again.")

    elif args.command == "analyze":  
        print("Loading viral gene data...")

        # Load gene sequences from input file
        data = load_fasta_dict(args.analysis_data)

        print("Loading trained HMM...")
        # Load previously trained model
        with open("hmm_model.pkl", "rb") as f:
            hmm = pickle.load(f)

        print("Analyzing viral genes...")
        # Run Viterbi and adapptation score calculation
        results = analyze_genes(data, hmm, args.num_paths)
        
        print("Saving results to output file...")
        # Store results to output file
        save_results(results, args.output_file)

        print(f"Scoring results saved to {args.output_file}")

        # Rank genes a write results to file
        write_genes_ranked_in_order(results, "results/ranked_genes.txt")
        print("Ranked gene results saved to results/ranked_genes.txt")
        
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

