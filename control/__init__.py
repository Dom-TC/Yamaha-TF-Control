from arguments import build_argparse


def main():
    # Build command line interface
    arg_parser = build_argparse()

    # Process args
    args = arg_parser.parse_args()


if __name__ == "__main__":
    main()
