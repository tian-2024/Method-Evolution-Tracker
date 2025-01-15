import argparse


class MethodComparison:
    def __init__(self, verbose=False, compute_transitive=False):
        # Initialize a dictionary to store which methods are defeated by others
        self.defeated_by = {}
        # Initialize a dictionary to store which methods defeat others
        self.defeats = {}
        self.verbose = verbose
        self.compute_transitive = compute_transitive

    def load_from_markdown(self, md_path):
        """
        Load comparison data from a markdown file.
        Format:
        Method1>baseline1,baseline2,...
        Method2>baseline1,baseline2,...
        """
        try:
            # Clear previous data
            self.defeated_by = {}
            self.defeats = {}

            with open(md_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Process each non-empty line
            data_lines = [line.strip() for line in lines if line.strip()]

            # Process each data line
            for line in data_lines:
                method, baselines_str = line.split(">")
                method = method.strip()
                baselines = [b.strip() for b in baselines_str.split(",")]

                if self.verbose:
                    print(f"Processing method {method}, which defeats: {baselines}")

                if baselines:
                    self.defeats[method] = set(baselines)
                    for baseline in baselines:
                        if baseline not in self.defeated_by:
                            self.defeated_by[baseline] = set()
                        self.defeated_by[baseline].add(method)

            # Ensure every method is recorded in defeated_by dictionary
            for method in self.defeats:
                if method not in self.defeated_by:
                    self.defeated_by[method] = set()

            if self.verbose:
                print("\nInitial relationships:")
                for method in self.defeated_by:
                    print(
                        f"{method} is defeated by: {sorted(self.defeated_by[method])}"
                    )

            return True
        except Exception as e:
            print(f"Error loading markdown file: {str(e)}")
            return False

    def compute_transitive_closure(self):
        """
        Compute the transitive closure: If A defeats B, and B defeats C, then A defeats C.
        """
        if self.verbose:
            print("\nComputing transitive closure...")
        changed = True
        while changed:
            changed = False
            for method in self.defeated_by:
                # Save the current size of better methods for comparison
                before_size = len(self.defeated_by[method])
                # Copy better methods to avoid modifying during iteration
                better_methods = self.defeated_by[method].copy()
                for better_method in list(better_methods):
                    # Check if there are methods better than the current better_method
                    if better_method in self.defeated_by:
                        for even_better in self.defeated_by[better_method]:
                            # Add new relationships if found
                            if even_better not in self.defeated_by[method]:
                                self.defeated_by[method].add(even_better)
                                changed = True
                                # Update the defeats relationship
                                if even_better not in self.defeats:
                                    self.defeats[even_better] = set()
                                self.defeats[even_better].add(method)

                # Debugging print statement for updated better methods
                if len(self.defeated_by[method]) > before_size:
                    if self.verbose:
                        print(
                            f"Updated better methods for {method}: {sorted(self.defeated_by[method])}"
                        )

    def export_to_markdown(self, output_path):
        """
        Export results to a markdown file with a table format.
        Format: | Method | Better Methods |
        """
        if self.compute_transitive:
            self.compute_transitive_closure()

        with open(output_path, "w", encoding="utf-8") as f:
            # Write table header
            f.write("| Method | Better Methods |\n")
            f.write("|--------|----------------|\n")

            # Write data rows
            for method in sorted(self.defeated_by.keys()):
                better_methods = sorted(self.defeated_by.get(method, []))
                better_methods_str = (
                    ", ".join(better_methods) if better_methods else "-"
                )
                f.write(f"| {method} | {better_methods_str} |\n")


# Example usage of the script
if __name__ == "__main__":
    # Define command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=str, default="input.md", help="Path to input markdown file"
    )
    parser.add_argument(
        "--output", type=str, default="output.md", help="Path to output markdown file"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="whether to output detailed information"
    )
    parser.add_argument(
        "--transitive",
        action="store_true",
        help="whether to compute transitive closure",
    )
    args = parser.parse_args()

    # Create an instance of the MethodComparison class
    comparisons = MethodComparison(
        verbose=args.verbose, compute_transitive=args.transitive
    )

    # Load data from input CSV and export results to markdown
    if comparisons.load_from_markdown(args.input):
        comparisons.export_to_markdown(args.output)
        print(f"Results saved to {args.output}")
    else:
        print(f"Error processing {args.input}")
