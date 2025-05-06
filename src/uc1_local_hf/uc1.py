import argparse # Re-import argparse
import sys
from .run_hf import main as run_hf_main
from .run_ctransformers import main as run_ctransformers_main # Re-import ctransformers
from .run_llama_cpp import main as run_llama_cpp_main # Import the new runner

# uc1 function now accepts a list of arguments to parse
def uc1(argv=None):
    # Create a new parser specific for uc1's arguments
    prog_name = f"{sys.argv[0]} uc1"
    uc1_parser = argparse.ArgumentParser(
        description='UC1 Runner Selection',
        prog=prog_name  # Use the calculated name
    )
    uc1_parser.add_argument(
        'runner',
        choices=['hf', 'ctransformers', 'llama_cpp'],
        help='Specify which runner to execute within UC1: "hf", "ctransformers", or "llama_cpp"'
    )

    try:
        args = uc1_parser.parse_args(argv)
    except SystemExit:
        # Catch SystemExit on parse error (e.g., missing required 'runner' arg)
        # to avoid exiting the main.py script.
        if argv is not None: # Check remains, though always true when called via main.py
            print("Error parsing arguments for uc1.")
            uc1_parser.print_help() # Print help for the uc1 sub-command
            return # Exit uc1 function but not the main script
        else:
            # This path should not be reachable if uc1.py isn't run directly
            raise

    if args.runner == 'hf':
        print("UC1: Running run_hf.main()...")
        run_hf_main()
    elif args.runner == 'ctransformers':
        print("UC1: Running run_ctransformers.main()...")
        run_ctransformers_main()
    elif args.runner == 'llama_cpp':
        print("UC1: Running run_llama_cpp.main()...")
        run_llama_cpp_main()

