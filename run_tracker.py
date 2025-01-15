# Import pandas library for data manipulation
import pandas as pd
import csv

# Import argparse library for handling command-line arguments
import argparse


# Define a class for method comparison
class MethodComparison:
    def __init__(self, verbose=False, compute_transitive=False):
        # Initialize a dictionary to store which methods are defeated by others
        self.defeated_by = {}
        # Initialize a dictionary to store which methods defeat others
        self.defeats = {}
        self.verbose = verbose
        self.compute_transitive = compute_transitive

    def load_from_csv(self, csv_path):
        """
        Load comparison data from a CSV file.
        CSV format: The first column is the method, subsequent columns are the baselines it defeats.
        """
        try:
            # Clear previous data
            self.defeated_by = {}
            self.defeats = {}

            # Determine the maximum number of columns in the CSV file
            with open(csv_path, "r") as f:
                max_cols = 0
                for line in f:
                    cols = len(line.strip().split(","))
                    max_cols = max(max_cols, cols)

            # Read the CSV file with determined column count
            df = pd.read_csv(
                csv_path, header=None, on_bad_lines="skip", names=range(max_cols)
            )

            # Iterate over rows in the dataframe, skipping the first row
            for idx, row in df.iterrows():
                if idx == 0:  # Skip the header row
                    continue

                # The first column represents the method
                method = row[0]
                # Retrieve all non-empty values in the row (excluding the first column)
                baselines = [x.strip() for x in row[1:] if pd.notna(x) and x.strip()]

                if self.verbose:
                    print(f"Processing method {method}, which defeats: {baselines}")

                # Record the baselines that the method defeats
                if baselines:
                    self.defeats[method] = set(baselines)

                    # Record that each baseline is defeated by the current method
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
            # Handle and print errors during CSV loading
            print(f"Error loading CSV file: {str(e)}")
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

    def export_to_csv(self, output_path):
        """
        Export results to a CSV file.
        Format: The first column is the method, subsequent columns are its better methods.
        """
        if self.compute_transitive:
            self.compute_transitive_closure()

        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            # Write header with only two columns
            writer.writerow(["method", "better methods"])
            # Write data rows with only actual better methods
            for method in sorted(self.defeated_by.keys()):
                better_methods = sorted(self.defeated_by.get(method, []))
                writer.writerow([method] + better_methods)


# Example usage of the script
if __name__ == "__main__":

    # Define command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=str, default="baselines.csv", help="Path to input CSV file"
    )
    parser.add_argument(
        "--output", type=str, default="evolutions.csv", help="Path to output CSV file"
    )
    parser.add_argument("--verbose", action="store_true", help="是否输出详细信息")
    parser.add_argument("--transitive", action="store_true", help="是否计算传递逻辑")
    args = parser.parse_args()

    # Create an instance of the MethodComparison class
    comparisons = MethodComparison(verbose=args.verbose, compute_transitive=args.transitive)

    # Load data from input CSV and export results to output CSV
    if comparisons.load_from_csv(args.input):
        comparisons.export_to_csv(args.output)
        print(f"Results saved to {args.output}")
    else:
        print(f"Error processing {args.input}")
