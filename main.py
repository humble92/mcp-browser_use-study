import argparse
import sys  # Need sys to exit cleanly
from src.uc1_local_hf.uc1 import uc1
from src.uc2_gpt4all.uc2 import uc2
from src.uc3_ollama.uc3 import uc3


def main():
    parser = argparse.ArgumentParser(description="Run a specific use case for mcp-browser-use-study.")
    parser.add_argument(
        "use_case",
        choices=["uc1", "uc2", "uc3"],
        help="The use case to run (uc1, uc2, or uc3)",
        nargs='?',  # Keep it optional to print help if missing
        default=None
    )
    # parse_known_args() splits arguments into known (for this parser)
    # and unknown (remaining_args)
    args, remaining_args = parser.parse_known_args()

    if args.use_case is None:
        parser.print_help()
        sys.exit(0)

    print(f"Hello from mcp-browser-use-study! Selected use case: {args.use_case}")
    print(f"Remaining arguments passed to use case: {remaining_args}") # For debugging

    # Pass the remaining arguments to the selected use case function
    if args.use_case == "uc1":
        uc1(remaining_args) # Pass the list of remaining args
    elif args.use_case == "uc2":
        uc2(remaining_args) # Pass the list of remaining args
    elif args.use_case == "uc3":
        uc3(remaining_args) # Pass the list of remaining args


if __name__ == "__main__":
    main()
