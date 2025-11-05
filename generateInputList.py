import argparse
import subprocess
import os

DATASETS = {
    "Muon2024I": [
        '/Muon1/Run2024I-PromptReco-v1/NANOAOD',
        '/Muon0/Run2024I-PromptReco-v1/NANOAOD',
        '/Muon1/Run2024I-PromptReco-v2/NANOAOD',
        '/Muon0/Run2024I-PromptReco-v2/NANOAOD',
    ],
    "Muon2025B": [
        "/Muon0/Run2025B-PromptReco-v1/NANOAOD",
        "/Muon1/Run2025B-PromptReco-v1/NANOAOD"
    ],
    "Muon2025C": [
        "/Muon0/Run2025C-PromptReco-v1/NANOAOD",
        "/Muon1/Run2025C-PromptReco-v1/NANOAOD"
    ],
    "Muon2025D": [
        "/Muon0/Run2025D-PromptReco-v1/NANOAOD",
        "/Muon1/Run2025D-PromptReco-v1/NANOAOD"
    ],
    "Muon2025E": [
        "/Muon0/Run2025E-PromptReco-v1/NANOAOD",
        "/Muon1/Run2025E-PromptReco-v1/NANOAOD"
    ],
    "Muon2025F": [
        "/Muon0/Run2025F-PromptReco-v1/NANOAOD",
        "/Muon1/Run2025F-PromptReco-v1/NANOAOD"

    ],
    "Muon2025G": [
        "/Muon0/Run2025G-PromptReco-v1/NANOAOD",
        "/Muon1/Run2025G-PromptReco-v1/NANOAOD"
    ],
    "EGamma2025F": [
        "/EGamma0/Run2025F-PromptReco-v1/NANOAOD",
        "/EGamma1/Run2025F-PromptReco-v1/NANOAOD",
        "/EGamma2/Run2025F-PromptReco-v1/NANOAOD",
        "/EGamma3/Run2025F-PromptReco-v1/NANOAOD"
    ],
    "EGamma2025G": [
        "/EGamma0/Run2025G-PromptReco-v1/NANOAOD",
        "/EGamma1/Run2025G-PromptReco-v1/NANOAOD",
        "/EGamma2/Run2025G-PromptReco-v1/NANOAOD",
        "/EGamma3/Run2025G-PromptReco-v1/NANOAOD"
    ],
    "EGamma2024I": [
        '/EGamma0/Run2024I-PromptReco-v1/NANOAOD',
        '/EGamma0/Run2024I-PromptReco-v2/NANOAOD',
        '/EGamma1/Run2024I-PromptReco-v1/NANOAOD',
        '/EGamma1/Run2024I-PromptReco-v2/NANOAOD',
    ],
    "EGamma2025C": [
        "/EGamma0/Run2025C-PromptReco-v1/NANOAOD",
        "/EGamma1/Run2025C-PromptReco-v1/NANOAOD",
        "/EGamma2/Run2025C-PromptReco-v1/NANOAOD",
        "/EGamma3/Run2025C-PromptReco-v1/NANOAOD"
    ],
    "EGamma2025D": [
        "/EGamma0/Run2025D-PromptReco-v1/NANOAOD",
        "/EGamma1/Run2025D-PromptReco-v1/NANOAOD",
        "/EGamma2/Run2025D-PromptReco-v1/NANOAOD",
        "/EGamma3/Run2025D-PromptReco-v1/NANOAOD"
    ],
    "EGamma2025E": [
        "/EGamma0/Run2025E-PromptReco-v1/NANOAOD",
        "/EGamma1/Run2025E-PromptReco-v1/NANOAOD",
        "/EGamma2/Run2025E-PromptReco-v1/NANOAOD",
        "/EGamma3/Run2025E-PromptReco-v1/NANOAOD"
    ],
    
    # add the others when needed!
    # next improvement: authomatize the search with wildcards 
    #(e.g. æ/EGamma*/Run<tag>-PromptReco-v*/NANOAOD")
}


def get_files(dataset):
    command = f'dasgoclient --query="file dataset={dataset}"'
    print("Running command:", command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error fetching files for dataset {dataset}")
        return []
    return result.stdout.strip().splitlines()


def save_list_to_txt(file_list, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        for item in file_list:
            f.write(f"{item}\n")
    print(f"File saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate file list from DAS for selected dataset group.")
    parser.add_argument("--tag", required=True, choices=DATASETS.keys(), help="Dataset tag to use (e.g., Muon2025C)")
    args = parser.parse_args()

    tag = args.tag
    datasets = DATASETS[tag]
    all_files = []

    for dataset in datasets:
        file_list = get_files(dataset)
        all_files.extend(file_list)

    output_file = f"input/{tag}.txt"
    save_list_to_txt(all_files, output_file)


if __name__ == "__main__":
    main()
