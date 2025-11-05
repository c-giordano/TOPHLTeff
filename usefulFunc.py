import subprocess
import os
import re


def getEra(inputDir):
    era = ''
    if '2023B' in inputDir:
        era = '2023B'
    elif '2023C' in inputDir:
        era = '2023C'
    elif '2023D' in inputDir:
        era = '2023D'
    elif '2022' in inputDir:
        era = '2022'    
    elif '2024C' in inputDir:
        era = '2024C'
    elif '2024D' in inputDir:
        era = '2024D'
    elif '2024E' in inputDir:
        era = '2024E'
    return era    

def getEraNano(url):
    match = re.search(r'Run(\d{4}[A-Z])', url)

    if match:
        era_string = match.group(1)
        return era_string
    else:
        print("Era string not found")

def extract_era_from_path(path):
    """
    Extracts the era pattern (e.g., "2024F") from the given directory path.

    Args:
    path (str): The directory path from which to extract the era pattern.

    Returns:
    str: The extracted era pattern, or None if no pattern is found.
    """
    # Regular expression pattern for the era, e.g., "2024F"
    pattern = re.compile(r'\b\d{4}[A-Z]\b')
    
    # Search for the pattern in the path
    match = pattern.search(path)
    
    if match:
        return match.group()
    return None    
   
 

def checkMakeDir( folder ):
    if not os.path.exists( folder ):
        os.makedirs( folder, exist_ok=True)
        
# def getPath()

def runCommand(command):
    print('runing command: ', command)
    process = subprocess.run( command, shell=True ) 
    output = process.stdout
    print(output)
    print('Done running command\n\n')
    
    
    