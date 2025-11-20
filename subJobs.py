import os
import argparse
import usefulFunc as uf

def parse_args():
    parser = argparse.ArgumentParser(description="Submit Condor jobs for HLT efficiency")
    parser.add_argument("--tag", required=True, help="Dataset tag name, e.g. Muon2025C, EGamma2024I")
    parser.add_argument("--user", choices=["victor", "cristina", "hhua"], default="cristina", help="User identity for output paths")
    parser.add_argument("--ifHadronic", action="store_true", help="Flag to process hadronic selection")
    parser.add_argument("--jobVersion", required=True, help="Job version label, e.g. v1ForMuon2024I")
    parser.add_argument('--hltJSON', type=str, default='./ownershipJson.json', help='Path to JSON of HLT menu (owners, online)')
    return parser.parse_args()

def extract_era(tag):
    return ''.join(filter(str.isdigit, tag)) + tag[-1]  #  "Muon2025C" to "2025C"

def make_out_dir(era, jobVersion, user):
    base_map = {
        "victor": "/eos/user/v/vshang/forTopHLT/",
        "cristina": "/eos/user/c/cgiordan/forTopHLT/",
        "huiling": "/eos/user/h/hhua/forTopHLT/"
    }
    outBase = base_map[user]
    outDir = os.path.join(outBase, era, jobVersion)+'/'
    print(outDir)
    uf.checkMakeDir(outDir)
    return outDir

def get_list_from_txt(inFile):
    with open(inFile, 'r') as file:
        return [line.strip() for line in file]

def get_name_from_path(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def write_job_script(jobName, inFile, outDir, ifHadronic, hltJSON):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hltJSON_abs = os.path.abspath(hltJSON)
    lines = [
        "#!/bin/bash",
        f"cd {current_dir}",
        f"lines=(`cat {current_dir}/{inFile}`)",
        "echo ${lines[$1]}",
        f"python3 skimNano.py --input ${{lines[$1]}} --outDir {outDir} --ifHadronic {ifHadronic} --ifTest False --hltJSON {hltJSON_abs}"
    ]
    write_list_to_file(lines, jobName)

def write_sub_file(subName, jobDir, fileNum, user):
    user_map = {
        "victor": "v/vshang",
        "cristina": "c/cgiordan",
        "hhua": "h/hhua"
    }
    proxyDir = user_map[user]
    lines = [
        "arguments               = $(Process)",
        f"executable              = {jobDir}/singleJob.sh",
        f"output                  = {jobDir}/logs/$(Process).out",
        f"error                   = {jobDir}/logs/$(Process).err",
        f"log                     = {jobDir}/logs/log.log",
        '+JobFlavour             = "workday"',
        f'x509userproxy           = /afs/cern.ch/user/{proxyDir}/.x509up_u142167',
        "use_x509userproxy       = True",
        "should_transfer_files   = YES",
        "when_to_transfer_output = ON_EXIT",
        f"queue {fileNum}"
    ]
    write_list_to_file(lines, subName)

def write_list_to_file(lines, file_path):
    with open(file_path, 'w') as f:
        for line in lines:
            f.write(line + '\n')
    print(f"[✓] Written to {file_path}")

def sub_htcondor(subScript):
    uf.runCommand(f"condor_submit {subScript}")

def main():
    args = parse_args()

    tag = args.tag
    era = extract_era(tag)
    inputList = f"input/{tag}.txt"
    outDir = make_out_dir(era, args.jobVersion, args.user)
    
    inList = get_list_from_txt(inputList)
    fileNum = len(inList)
    print(f"[✓] Number of input files: {fileNum}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    jobDir = os.path.join(current_dir, "jobs", tag, args.jobVersion)
    logDir = os.path.join(jobDir, "logs")
    uf.checkMakeDir(jobDir)
    uf.checkMakeDir(logDir)

    write_job_script(os.path.join(jobDir, "singleJob.sh"), inputList, outDir, args.ifHadronic, args.hltJSON)
    write_sub_file(os.path.join(jobDir, "subList.sub"), jobDir, fileNum, args.user)
    sub_htcondor(os.path.join(jobDir, "subList.sub"))

if __name__ == "__main__":
    main()
