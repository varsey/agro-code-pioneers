import argparse


def args_parse() -> tuple:
    parser = argparse.ArgumentParser(description="App for jobs clustering.")

    parser.add_argument('--sample_size', type=int, help='The size of the sample.')
    parser.add_argument('--shorts', action='store_true', help='A boolean flag if to include short jobstreams.')
    parser.add_argument('--rule', action='store_true', help='A boolean flag if apply custom rule.')

    args = parser.parse_args()

    print("Sample Size: ", args.sample_size)
    print("Shorts: ", args.shorts)
    print("Rule: ", args.rule)

    # Default sample size
    sample_size = 250
    if args.sample_size:
        sample_size = args.sample_size
    shorts_included = args.shorts
    use_rule = args.rule

    return sample_size, shorts_included, use_rule
