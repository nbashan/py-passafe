import argparse
from typing import List

def main() -> None:
    main_parser = argparse.ArgumentParser(description="local password manager")
    main_parser.add_argument("--vault", dest="vault", required=True, metavar="PATH", help="path to the vault")
    args = main_parser.parse_args()
    
    print(args)
    print(args.get_password)

if __name__ == "__main__":
    main()
