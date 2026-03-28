import argparse

def main():
    parser = argparse.ArgumentParser(description="Web Crawler POC")
    
    # Add your arguments here
    parser.add_argument("url", help="The root URL to start crawling")
    parser.add_argument("-d", "--depth", type=int, default=2, help="Crawling depth (default: 2)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

    args = parser.parse_args()

    # Access your args
    print(f"Crawling: {args.url} with depth {args.depth}")
    if args.verbose:
        print("Verbose mode enabled!")

if __name__ == "__main__":
    main()
