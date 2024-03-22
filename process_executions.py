import json
from collections import Counter

def process_executions(json_file, txt_file):
    # Load the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Create a string for each execution path
    execution_paths = [' => '.join(execution[1:-1]) for execution in data]

    # Count the occurrences of each execution path
    execution_counts = Counter(execution_paths)

    # Write the counts and the execution paths to a text file
    with open(txt_file, 'w') as f:
        f.write(f"{len(data)} times\n")
        for path, count in execution_counts.items():
            f.write(f"{count} executions: {path}\n")