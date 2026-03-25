import argparse
import subprocess
import os
import re
import sys

def run_das_query(query):
    """
    Run DAS query and return non-empty output lines.
    """
    cmd = ["dasgoclient", f"--query={query}"]
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR while running DAS query:")
        print(result.stderr.strip())
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]

def parse_tag(tag):
    """
    Parse tags like: Muon2025C, EGamma2024I etc etc
    Returns: primary_base, run_tag
    """
    match = re.fullmatch(r"([A-Za-z]+)(\d{4}[A-Z])", tag)
    if not match:
        raise ValueError(f"Invalid '{tag}' tag! Use format like <Dataset><year><era> (i.e. Muon2025C)!")
    primary_base, run_tag = match.groups()

    return primary_base, run_tag

def extract_primary_dataset(dataset):
    """
    From a DAS dataset path like: /Muon0/Run2025C-PromptReco-v1/NANOAOD
    Return:Muon0
    """
    parts = dataset.strip().split("/")
    if len(parts) < 2 or not parts[1]:
        return None
    return parts[1]

def exclude(primary_name, primary_base):
    """
    Keep only primary datasets of the form:
      Muon, Muon0, Muon1, ...
      EGamma, EGamma0, EGamma1, ...
    This excludes e.g. MuonEG when primary_base == "Muon".
    """
    pattern = rf"{re.escape(primary_base)}\d*"
    return re.fullmatch(pattern, primary_name) is not None


def filter_datasets(datasets, primary_base):
    """
    Filter datasets based on the primary dataset name.
    """
    filtered = []
    for ds in datasets:
        primary_name = extract_primary_dataset(ds)
        if primary_name and exclude(primary_name, primary_base):
            filtered.append(ds)
        else:
            print(f"Skipping dataset: {ds}")
    return sorted(set(filtered))

def get_matching_datasets(tag, reco="PromptReco", data_tier="NANOAOD"):
    """
    Build a DAS pattern like:
      /Muon*/Run2025C-PromptReco-v*/NANOAOD
      /EGamma*/Run2024I-PromptReco-v*/NANOAOD
    Then filter the matched datasets to avoid unwanted matches
    """
    primary_base, run_tag = parse_tag(tag)

    dataset_pattern = f"/{primary_base}*/Run{run_tag}-{reco}-v*/{data_tier}"
    query = f"dataset dataset={dataset_pattern}"

    datasets = run_das_query(query)
    datasets = filter_datasets(datasets, primary_base)

    return datasets


def get_files_for_dataset(dataset):
    """
    Return all files in a DAS dataset.
    """
    query = f"file dataset={dataset}"
    return run_das_query(query)

def save_list_to_txt(file_list, output_path):
    """
    Save file list to txt.
    """
    outdir = os.path.dirname(output_path)
    if outdir:
        os.makedirs(outdir, exist_ok=True)

    with open(output_path, "w") as f:
        for item in file_list:
            f.write(f"{item}\n")

    print(f"\nSaved file list to: {output_path}")
    print(f"Total files written: {len(file_list)}")


def main():
    parser = argparse.ArgumentParser(description="Generate a file list from DAS starting from a single tag")
    parser.add_argument("--tag", required=True, help="Tag: Muon2025C, EGamma2024I, Muon2026B")
    parser.add_argument("--reco", default="PromptReco", help="Reco campaign label")
    parser.add_argument("--dataTier", default="NANOAOD", help="Data tier (default: NANOAOD)")
    parser.add_argument("--output", default=None, help="Output txt file. Default: input/<tag>.txt")
    args = parser.parse_args()

    try:
        datasets = get_matching_datasets(tag=args.tag, reco=args.reco, data_tier=args.dataTier)
    except ValueError as e:
        print(e)
        sys.exit(1)

    if not datasets:
        print(f"No datasets found for tag {args.tag}")
        sys.exit(1)

    print("\nMatched datasets:")
    for ds in datasets:
        print("  ", ds)

    all_files = []
    for dataset in datasets:
        files = get_files_for_dataset(dataset)
        print(f"  -> {dataset}: {len(files)} files")
        all_files.extend(files)

    all_files = sorted(set(all_files))

    output_file = args.output if args.output else f"input/{args.tag}.txt"
    save_list_to_txt(all_files, output_file)


if __name__ == "__main__":
    main()