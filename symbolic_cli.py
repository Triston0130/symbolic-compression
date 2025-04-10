import sys
import argparse
from symbolic_core import RecursiveFunctionCompressor, recurrence_rules, MultiZoneSymbolicCompressor
from symbolic_io import (
    save_recursive_to_sym,
    load_recursive_from_sym,
    save_collapse_to_sym,
    load_collapse_from_sym
)

# Set the max number of digits for integer string conversion
sys.set_int_max_str_digits(1000000)  # Adjust this number as needed

def run_cli():
    parser = argparse.ArgumentParser(description="Symbolic Compression CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Compress command
    compress_parser = subparsers.add_parser("compress", help="Compress a symbolic recursive sequence")
    compress_parser.add_argument("rule", choices=recurrence_rules.keys(), help="Recurrence rule name (e.g. fibonacci)")
    compress_parser.add_argument("--length", type=int, required=True, help="Number of values to generate")
    compress_parser.add_argument("--output", type=str, required=True, help="Output .sym file")

    # Decompress command
    decompress_parser = subparsers.add_parser("decompress", help="Decompress a .sym file into text or terminal")
    decompress_parser.add_argument("file", help="Path to .sym file")
    decompress_parser.add_argument("--output", type=str, help="Optional output .txt file")

    # Collapse-based multi-zone compression command
    collapse_parser = subparsers.add_parser("collapse", help="Compress a symbolic sequence into multi-zone collapse format")
    collapse_parser.add_argument("--output", type=str, required=True, help="Output .sym file")
    collapse_parser.add_argument("--segment-length", type=int, default=20, help="Segment length for zone compression")

    # Predict (regenerate) a sequence from a multi-zone .sym file
    predict_parser = subparsers.add_parser("predict", help="Regenerate a symbolic sequence from .sym rules")
    predict_parser.add_argument("file", help="Path to .sym file")
    predict_parser.add_argument("--output", type=str, help="Optional output file for predicted sequence")

    args = parser.parse_args()

    if args.command == "compress":
        rule_fn, init_vals = recurrence_rules[args.rule]
        print(f"Attempting to compress using rule '{args.rule}' and saving to {args.output}...")
        save_recursive_to_sym(
            rule_name=args.rule,
            initial_values=init_vals,
            N=args.length,
            rule_expr=f"{args.rule}(n)",
            filename=args.output
        )
        print(f"[✓] Compressed '{args.rule}' into {args.output} with N={args.length}")

    elif args.command == "decompress":
        rule_id, init_vals, N = load_recursive_from_sym(args.file)
        rule_fn, _ = recurrence_rules[rule_id]
        rfc = RecursiveFunctionCompressor(init_vals, rule_fn, N)
        output_sequence = rfc.decompress()

        if args.output:
            with open(args.output, "w") as f:
                for val in output_sequence:
                    f.write(f"{val}\n")
            print(f"[✓] Decompressed {args.file} → {args.output}")
        else:
            print(output_sequence)

    elif args.command == "collapse":
        print(f"Compressing symbolic sequence into multi-zone file: {args.output}")
        sequence = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
        compressor = MultiZoneSymbolicCompressor(segment_length=args.segment_length)
        segments = compressor.compress(sequence)
        save_collapse_to_sym(segments, args.output)
        print(f"[✓] Saved {len(segments)} symbolic zones to {args.output}")

    elif args.command == "predict":
        print(f"Loading .sym file: {args.file}")
        segments = load_collapse_from_sym(args.file)
        
        from symbolic_core import SymbolicCompressor
        sequence = []

        for rule in segments:
            sc = SymbolicCompressor(
                x0=rule["x0"],
                delta0=rule["delta0"],
                kappa=rule["kappa"],
                N=rule["N"]
            )
            segment = sc.decompress()
            sequence.extend(segment)

        if args.output:
            with open(args.output, "w") as f:
                for val in sequence:
                    f.write(f"{val}\n")
            print(f"[✓] Regenerated sequence saved to {args.output}")
        else:
            print(sequence)

if __name__ == "__main__":
    run_cli()
