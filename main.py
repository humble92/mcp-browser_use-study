import argparse
import sys  # Need sys to exit cleanly
import asyncio # Import asyncio
from src.conf1.conf1 import dump_cookies # browser cookies configuration
from src.uc1_local_hf.uc1 import uc1
from src.uc2_gpt4all.uc2 import uc2
from src.uc3_ollama.uc3 import uc3
from src.uc4_google_login.uc4 import uc4


def main():
    parser = argparse.ArgumentParser(description="Run MCP Browser Use Study Use Cases.")
    subparsers = parser.add_subparsers(dest="use_case", help='Select the use case to run')

    # --- Use Case 1: Local HF/CTransformers/LlamaCpp --- #
    parser_uc1 = subparsers.add_parser('uc1', help='Run Use Case 1 (Local HF/CT/LlamaCpp)')
    # Add subparsers for uc1 runners, allowing arguments like 'hf', 'ctransformers', 'llama_cpp'
    # We don't define specific args here; uc1 handles them with parse_known_args

    # --- Use Case 2: GPT4All with Agent --- #
    parser_uc2 = subparsers.add_parser('uc2', help='Run Use Case 2 (GPT4All with Agent)')

    # --- Use Case 3: Ollama with Agent --- #
    parser_uc3 = subparsers.add_parser('uc3', help='Run Use Case 3 (Ollama with Agent, cdp_browser)')

    # --- Use Case 4: Google Login with Agent --- # Added uc4 parser
    parser_uc4 = subparsers.add_parser('uc4', help='Run Use Case 4 (Ollama: Google Login with Agent\'s senstive_data)')

    # Use parse_known_args for uc1 to allow passthrough arguments
    # For others, just parse args normally
    if sys.argv[1:2] == ['uc1']:
        args, unknown_args = parser.parse_known_args()
    else:
        args = parser.parse_args()
        unknown_args = [] # Ensure unknown_args is defined for other cases

    if args.use_case == "conf1":
        asyncio.run(dump_cookies())
    elif args.use_case == "uc1":
        # Pass the remaining arguments (like 'hf', 'ctransformers', etc.) to uc1
        uc1(unknown_args)
    elif args.use_case == "uc2":
        asyncio.run(uc2())
    elif args.use_case == "uc3":
        asyncio.run(uc3())
    elif args.use_case == "uc4": # Added condition for uc4
        asyncio.run(uc4())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
